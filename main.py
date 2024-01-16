from typing import Union, List
from fastapi import FastAPI, Body
import datetime
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uuid
from dotenv import dotenv_values
from pymongo import MongoClient, collection, database
from contextlib import asynccontextmanager
from bson.json_util import dumps, loads
from model import generate, init_gpt_api
import logging

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s)"
)



config = dotenv_values(".env")
db_client = None
db: database.Database = None
db_collection: collection.Collection = None
openai_client = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global db_client, db, db_collection, model, tokenizer, device, openai_client
    db_client = MongoClient(config["ATLAS_URI"])
    db = db_client[config["DB_NAME"]]
    db_collection = db[config["COLLECTION_NAME"]]
    openai_client = init_gpt_api(config["OPENAI_API_KEY"])
    yield
    db_client.close()


class Prompt(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    prompt_text: str = Field(...)
    element: Union[str, None] = Field(default=None)
    generation: Union[str, None] = Field(None)


class Project(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    prompts: List[Prompt] = Field(...)
    name: str = Field(...)


class NewProject(BaseModel):
    project_name: str = Field(...)
    prompt_text: str = Field(...)
    date: str = datetime.datetime.now().strftime("%Y-%m-%d")


class NewPrompt(BaseModel):
    project_id: str = Field(...)
    prompt_text: str = Field(...)
    element: Union[str, None] = Field(default=None)


def get_prediction(prompt: str, prev_prompt= None, element= None, openai_client=None):
    # return f"This is a test for the prompt \"{prompt}\". \n Previous prompt: \"{prev_prompt['prompt_text']}\""
    return generate(prompt, prev_prompt, element, openai_client)


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/new_project")
async def new_project(new_project: NewProject):
    logging.info(f"New project: {new_project}")
    code_generation = get_prediction(new_project.prompt_text,openai_client=openai_client )
    prompt = Prompt(prompt_text=new_project.prompt_text, generation=code_generation)
    project = Project(name=new_project.project_name, prompts=[prompt])
    project_json = jsonable_encoder(project)
    db_collection.insert_one(project_json)

    return project_json


@app.post("/new_prompt")
async def new_prompt(new_prompt: NewPrompt):
    prev_prompt = db_collection.find_one({"_id": new_prompt.project_id})["prompts"][-1]
    # prev_prompt = Prompt(**prev_prompt)
    prompt_generation = get_prediction(new_prompt.prompt_text, prev_prompt, new_prompt.element, openai_client=openai_client)
    prompt = Prompt(
        prompt_text=new_prompt.prompt_text,
        generation=prompt_generation,
        element=new_prompt.element,
    )
    prompt_json = jsonable_encoder(prompt)
    db_collection.update_one(
        {"_id": new_prompt.project_id}, {"$push": {"prompts": prompt_json}}
    )

    return prompt_json


@app.get("/get_project/{project_id}")
async def get_project(project_id: str):
    project = db_collection.find_one({"_id": project_id})
    return project


@app.get("/get_projects")
async def get_projects():
    projects = db_collection.find({})

    projects_list = loads(dumps(projects))
    return {"projects": projects_list}
