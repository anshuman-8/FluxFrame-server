from openai import AsyncOpenAI, OpenAI
import logging
import re

model = "gpt-3.5-turbo"
sys_init_message = {
    "role": "system",
    "content": "You are a helpful experienced web developer and designer "
    "with a deep knowledge of React, TailwindCSS, Web-development "
    "and Software UI design. Follow all the instructions provided, but can also "
    "give more features. Do not give multiple answers or repeat things. Make "
    "beautiful designs using TailwindCSS based on your creativity. Don't provide "
    "wrong code. Give a complete solution with maximum number of features. "
    "Give only the JSX code, Do not give any explanation, comments or enclose it "
    "in code blocks. "
    "Code practice: Give only the react JSX code, using tailwindCSS in its className. "
    "Do not give globals.css CSS code,just give tailwindCSS class in className. "
    "Always check if all the components are correctly written and mapped.",
}

sys_followup_message = {
    "role": "system",
    "content": "You are a helpful experienced web developer and designer "
    "with a deep knowledge of React, TailwindCSS, JavaScript, Web-development "
    "and Software UI design. You will be given the code for a React file that "
    "contains a component. You will also be given a prompt that describes a "
    "modification that a certain part of the component needs. You might also be "
    "given the code of the part of the component that needs to be modified. "
    "If the code for the part to be modified is not given, you will have to "
    "infer the part to be modified from the provided prompt or add the code for "
    "the part to be modified. You will have to modify the component to satisfy "
    "the prompt. Return the full code of the modified component and follow the "
    "below code practice. "
    "Code practice: Give only the JSX code, using tailwindCSS in its className. "
    "Do not give globals.css CSS code,just give tailwindCSS class in className. "
    "You may also write necessary correct javascript by creating functions inside "
    "<script> tag, use buttons calling function and don't use form tag. Always "
    "check if all the components are correctly written and mapped.",
}

history = []


def init_gpt_api(key: str):
    client = OpenAI(api_key=key)
    return client
    logging.info("GPT-3 API initialized")


def generate(prompt, prev_prompt= None, element= None, openai_client=None):
    code = get_code_generation(prompt, prev_prompt, element, openai_client)
    code = get_html_block(code)
    code = prepare_react_code(code)

    return code


def get_code_generation(message: str, prev_prompt= None, element= None, openai_client=None) -> str:
    if prev_prompt is None:
        messages = [sys_init_message] + [{"role": "user", "content": message}]
    else:
        user_followup_messages = [
            {"role": "user", "content": message},
            {"role": "user", "content": f"Code:\n{prev_prompt.generation}"},
        ]
        if element is not None:
            user_followup_messages.append(
                {"role": "user", "content": f"Element to modify:\n{element}"}
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

    content = replace_escape_characters(content)
    with open("content.js", "w") as f:
        f.write(content)
    return content


def replace_escape_characters(code):
    code = code.replace("\\n", "\n")
    code = code.replace("\\t", "\t")
    code = code.replace('\\"', '"')
    code = code.replace("\\'", "'")
    return code


def get_html_block(filling):
    html_pattern = r"<html>(.*?)</html>"
    matches = re.findall(html_pattern, filling, re.DOTALL)

    if matches:
        return matches[0]
    else:
        return filling


def prepare_react_code(filling):
    start_marker = "function Component(){"
    end_marker = "export default Component;"

    start_index = filling.find(start_marker)
    end_index = filling.find(end_marker, start_index)

    print(start_index, end_index)

    if start_index != -1 and end_index != -1 and end_index > start_index:
        content = filling[start_index + len(start_marker) : end_index].strip()
        filling = content
    else:
        filling = "return() "

    code = (
        """
        import React from "react";
        import '../styles/globals.css'
             
          function Component(){
          
          """
        + filling
        + """
          
          export default Component;
        """
    )
    return code
