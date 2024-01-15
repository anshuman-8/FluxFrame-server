from openai import AsyncOpenAI, OpenAI
import logging
import re

model = "gpt-3.5-turbo"
sys_init_message = {
    "role": "system",
    "content": """You have good knowledge of React, TailwindCSS, Web-development 
    and Software UI design. Follow all the instructions provided, but can also 
    give more features. Make beautiful designs using TailwindCSS based on your creativity. 
    Design the whole component in a modern design and make it look beautiful.
    Give only the react function, Do not give any explanation, comments and do not enclose it in code blocks. 
    Give code only of the Component function. Define react component function as: `const Component = () =>{` ...
    DO NOT export or return the component.
    Always name the function/component as `Component`.

    import React from "react";
    import '../styles/globals.css'

    // Write code form here"""
    ,
}

sys_followup_message = {
    "role": "system",
    "content": """You will be given the code for a React file that 
    contains a component. Modify just the element code in the whole Component code.
    Return the whole Component code after modification. Do not modify any other part of the code.
    The response should only contain the modified component code.
    The component code provided will be delimited by <<Component>> and <</Component>>.
    The element code to modify will be delimited by <<Element>> and <</Element>>.
    Return the whole modified Component code. Do not modify any other part of the code.
    The response should only contain the modified component code without any delimiters.
    The returned code should be a valid React component code and should not contain any syntax errors.""",
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
            {"role": "user", "content": f"Modification to make: {message}"},
            {"role": "user", "content": f"<<Component>>\n{prev_prompt['generation']}\n<</Component>>"},
        ]
        if element is not None and element != "":
            user_followup_messages.append(
                {"role": "user", "content": f"<<Element>>\n{element}\n<</Element>>"}
            )
        else:
            user_followup_messages.append(
                {"role": "user", "content": f"<<Element>>\n{prev_prompt['generation']}\n<</Element>>"}
            )
        messages = [sys_followup_message] + user_followup_messages
    # messages = [sys_init_message] + [{"role": "user", "content": message}]

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

    delimiters = ["<<Component>>", "<</Component>>", "<<Element>>", "<</Element>>"]
    for delimiter in delimiters:
        filling = filling.replace(delimiter, "")

    start_index = filling.find(start_marker)

    print(start_index)

    if start_index != -1:
        filling = filling[start_index :].strip()

    end_index = filling.find(end_marker) 
    if end_index != -1:
        filling = filling[:end_index].strip()

    with open("filling.js", "w") as f:
        f.write(filling)

    code =  filling
    return code
