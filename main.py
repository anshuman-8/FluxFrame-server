from typing import Union, List
from fastapi import FastAPI, Body
from pydantic import BaseModel, Field
import uuid
from dotenv import dotenv_values
from pymongo import MongoClient, collection, database
from contextlib import asynccontextmanager
from bson.json_util import dumps, loads

config = dotenv_values(".env")
db_client = None
db: database.Database = None
db_collection: collection.Collection = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global db_client, db, db_collection
    db_client = MongoClient(config["ATLAS_URI"])
    db = db_client[config["DB_NAME"]]
    db_collection = db[config["COLLECTION_NAME"]]
    yield
    db_client.close()

class Prompt(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    prompt_text: str = Field(...)
    generation: Union[str, None] = Field(None)

class Project(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    prompts: List[Prompt] = Field(...)
    name: str = Field(...)

class NewProject(BaseModel):
    project_name: str = Field(...)
    prompt_text: str = Field(...)

def get_prediction(prompt: str):
    return "This is a test"

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/new_project")
async def new_project(new_project: NewProject):
    prompt_generation = get_prediction(new_project.prompt_text)
    prompt = Prompt(prompt_text=new_project.prompt_text, generation=prompt_generation)
    project = Project(name=new_project.project_name, prompts=[prompt])
    db_collection.insert_one(project.model_dump(by_alias=True))
    return project.model_dump()

@app.get("/get_project/{project_id}")
async def get_project(project_id: str):
    project = db_collection.find_one({"_id": project_id})
    return project

@app.get("/get_projects")
async def get_projects():
    projects = db_collection.find({})
    
    projects_list = loads(dumps(projects))
    return {"projects": projects_list}

