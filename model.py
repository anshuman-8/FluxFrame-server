import os
from dotenv import dotenv_values

config = dotenv_values(".env")
os.environ["TRANSFORMERS_CACHE"] = config["TRANSFORMERS_CACHE_DIR"]

import torch
import transformers
import logging as log
import re

MAX_INPUT_TOKEN_LENGTH = 4000
MAX_TOKEN = 3840
log.basicConfig(level=log.INFO, format=" %(levelname)s %(message)s")
history = []

SYSTEM_PROMPT = """
You are a helpful experienced web developer and designer with a deep knowledge of React, TailwindCSS, JavaScript, Web-development and Software UI design. Follow all the instructions provided, but can also give more features.\nDo not give multiple answers or repeat things. Make beautiful designs using TailwindCSS based on your creativity.\nPlease don't provide wrong code. \n Give a complete solution with maximum number of features. 
Code practice: Give only the JSX code, using tailwindCSS in its className. Do not give globals.css CSS code,just give tailwindCSS class in className. You may also write necessary correct javascript by creating functions inside <script> tag, use buttons calling function and don't use form tag. Always check if all the components are correctly written and mapped.\
"""


def init_model():
    bnb_config = transformers.BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
        bnb_4bit_compute_dtype=torch.bfloat16,
    )

    model = transformers.AutoModelForCausalLM.from_pretrained(
        "codellama/CodeLlama-13b-Instruct-hf",
        # "/home/anshuman/.cache/huggingface/hub/models--codellama--CodeLlama-13b-Instruct-hf",
        trust_remote_code=True,
        quantization_config=bnb_config,
        device_map="auto",
        # load_in_8bit_fp32_cpu_offload=True
    ).eval()

    tokenizer = transformers.CodeLlamaTokenizer.from_pretrained(
        "codellama/CodeLlama-13b-Instruct-hf"
        # "/home/anshuman/.cache/huggingface/hub/models--codellama--CodeLlama-13b-Instruct-hf"
    )

    device = "cuda" if torch.cuda.is_available() else "cpu"

    return model, tokenizer, device

def generate(prompt, model, tokenizer, device):

    processed_prompt = get_prompt(prompt,SYSTEM_PROMPT)
    input_ids = tokenizer(processed_prompt, return_tensors="pt", device=device)["input_ids"]
    generated_ids = model.generate(input_ids.to(device), max_new_tokens=MAX_TOKEN)
    filling = tokenizer.batch_decode(generated_ids[:, input_ids.shape[1] :], skip_special_tokens=True)[0]

    log.info(f'Filling: {filling}')
    # gen_code = f'{prepare_react_code(filling)}'
    gen_code = filling
    return gen_code

def get_prompt(message: str,system_prompt: str, history_code: str = "<></>", infilling=False) -> str:
    # texts = [f'<s><<SYS>>\n{system_prompt}\n<</SYS>>\n\n[INST]{message}\n[/INST]\n<!DOCTYPE html> <html><FILL_ME></html></s>']
    texts =  f"<<SYS>>\n{system_prompt}\n<</SYS>>\n[INST]{message}\n[/INST]\n" 
    texts+="import React from 'react';\nimport '../styles/globals.css';\n\nfunction Component(){\n<FILL_ME> \n}\nexport default Component;"
    
    log.info(f'Prompt: {texts}')
    history = texts
    return ''.join(texts)

def get_html_block(filling):
    html_pattern = r'<html>(.*?)</html>'
    matches = re.findall(html_pattern, filling, re.DOTALL)
    
    if matches:
        return matches[0]
    else:
        return filling

def prepare_react_code(filling):
    start_marker = 'function Component(){'
    end_marker = 'export default Component;'
    
    start_index = filling.find(start_marker)
    end_index = filling.find(end_marker, start_index)

    print(start_index, end_index)

    if start_index != -1 and end_index != -1 and end_index > start_index:
        content = filling[start_index + len(start_marker):end_index].strip()
        filling =  content
    else:
        filling = 'return() '
        
    code = '''
        import React from "react";
        import '../styles/globals.css'
             
          function Component(){
          
          '''+filling+'''
          
          export default Component;
        '''
    return code