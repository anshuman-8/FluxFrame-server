from openai import AsyncOpenAI, OpenAI
import logging
import re

model = "gpt-3.5-turbo-1106"
sys_init_message = {
    "role": "system",
    "content": """You have good knowledge of React, TailwindCSS, Web-development 
    and Software UI design. Follow all the instructions provided, but can also 
    give more features. Make modern beautiful designs using TailwindCSS based on your creativity and Prompt given below. 
    Design the whole component in a modern UI/UX design and make it look beautiful.
    Give only the react function, Give explanation and comments.
    Use https://via.placeholder.com/ for images, by passing dimensions example- /50, also fill component with dummy string data content. 
    But DO NOT use svg for icon in code, just use text instead.
    Give code only of the Component function. Define react component function as: `const Component = () =>{` ...
    DO NOT export or return the component. Never use svg. Fill empty div with dummy content.
    Always name the function/component as `Component`.
    Return the code as string, and do NOT give code inside any code block.

    import React from "react";
    import '../styles/globals.css'

    // Write code form here"""
    ,
}

sys_followup_message = {
    "role": "system",
    "content": """You will be given the main code for a React file that contains a element. 
    Modify just the element code (its in HTML convert to React) in the whole main Component code.
    Return the whole main code after modification. Do not modify any other part of the maincode.
    The response should contain the whole code after modification.
    Do not modify any other part of the code. Do NOT use svg.
    The response should only contain the modified Component code.
    The returned code should be a valid React Component code and should not contain any syntax errors.
    Always name the function/component as `Component`. Define react component function as: `const Component = () =>{` ...
    Return the code as string, and NOT inside any code block. 
    """,
}

history = []


def init_gpt_api(key: str):
    client = OpenAI(api_key=key)
    logging.info("GPT-3 API initialized")
    return client


def generate(prompt, prev_prompt= None, element= None, openai_client=None):
    code = get_code_generation(prompt, prev_prompt, element, openai_client)
    code = prepare_react_code(code)

    with open("content.js", "w") as f:
        f.write(code)

    return code


def get_code_generation(message: str, prev_prompt= None, element= None, openai_client=None) -> str:
    if prev_prompt is None:
        messages = [sys_init_message] + [{"role": "user", "content": f"Prompt :{message}"}]
    else:
        user_followup_messages = [
            {"role": "user", "content": f"Main Code: {prev_prompt['generation']}"},
            {"role": "user", "content": f"Modification to make: {message}"},
        ]
        if element is not None and element != "":
            user_followup_messages.append(
                {"role": "user", "content": f"Element to modify in main code:\n{element}\n\nFull modified code:"}
            )
        messages = [sys_followup_message] + user_followup_messages

    logging.info(f"Sending API request: {messages}")
    completion = openai_client.chat.completions.create(
        model=model,
        messages=messages,
    )
    logging.info(f"Received API response: {completion}")
    content = completion.choices[0].message.content

    # content = replace_escape_characters(content)
    return content


def replace_escape_characters(code):
    code = code.replace("\\n", "\n")
    code = code.replace("\\t", "\t")
    code = code.replace('\\"', '"')
    code = code.replace("\\'", "'")
    return code


def prepare_react_code(filling):
    start_marker = "const"
    end_marker = "export"
    code_end_marker = ");\n}"
    
    start_index = filling.find(start_marker)

    print(start_index)

    if start_index != -1:
        filling = filling[start_index :].strip()

    end_index = filling.find(end_marker) 
    if end_index != -1:
        filling = filling[:end_index].strip()
    
    code_end_index = filling.find(code_end_marker) + 4
    if code_end_index != -1:
        filling = filling[:code_end_index].strip()

    with open("filling.js", "w") as f:
        f.write(filling)

    code =  filling
    return code
