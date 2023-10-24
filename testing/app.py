import os
import torch
import re
import transformers
import logging as log
# from dotenv import load_dotenv

# load_dotenv()

MAX_INPUT_TOKEN_LENGTH = 4000
MAX_TOKEN = 3584
log.basicConfig(level=log.INFO, format=" %(levelname)s %(message)s")
history = []

SYSTEM_PROMPT = """
You are a helpful experienced web developer and designer with a deep knowledge of HTML, CSS, Web-development and software UI design. Follow all the instructions provided, but can also give more features.\nDo not give multiple answers or repeat things. Make beautiful designs using CSS based on your creativity.\nPlease don't provide wrong code. \n Give a complete solution with maximum number of features. Code practice: Give all the CSS inside <style> tag mapped with class names and id. Do not link any files to head link tag. You may also write necessary correct javascript by creating functions inside <script> tag, use buttons calling function and don't use form tag. Always check if all the components are correctly written and mapped.\
"""

PROMPT = "A personal portfolio with a navbar with big text of 'About' and 'Blog' in center The page should be divided into 2 parts vertically, left side should have a profile pic and right side should have a short description about the person. The page should have a footer with social media icons."

def get_prompt(message: str,system_prompt: str, history_code: str = "<></>", infilling=False) -> str:
    texts = [f'<s><<SYS>>\n{system_prompt}\n<</SYS>>\n\n[INST]{message}\n[/INST]\n<!DOCTYPE html> <html><FILL_ME></html></s>']

    
    log.info(f'Prompt: {texts}')
    history = texts
    return ''.join(texts)


def write_to_html(filename, content):
    with open(filename, 'w') as file:
        file.write(content)
        file.close()

def get_html_block(filling):
    html_pattern = r'<html>(.*?)</html>'
    matches = re.findall(html_pattern, filling, re.DOTALL)
    
    if matches:
        return matches[0]
    else:
        return filling


def generate(prompt, model, device):
    tokenizer = transformers.CodeLlamaTokenizer.from_pretrained(
        "codellama/CodeLlama-13b-Instruct-hf"
    )
    processed_prompt = get_prompt(prompt,SYSTEM_PROMPT)
    input_ids = tokenizer(processed_prompt, return_tensors="pt", device=device)["input_ids"]
    generated_ids = model.generate(input_ids.to(device), max_new_tokens=MAX_TOKEN)
    filling = tokenizer.batch_decode(generated_ids[:, input_ids.shape[1] :], skip_special_tokens=True)[0]
    # gen_code = prompt.replace(" <FILL_ME>", filling)
    print(filling)
    gen_code = f'<!DOCTYPE html>\n<html>\n{get_html_block(filling)}</html>'
    write_to_html('./testing/index.html', gen_code)
    return gen_code



def main():
    bnb_config = transformers.BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
        bnb_4bit_compute_dtype=torch.bfloat16,
    )

    model = transformers.AutoModelForCausalLM.from_pretrained(
        "codellama/CodeLlama-13b-Instruct-hf",
        trust_remote_code=True,
        quantization_config=bnb_config,
        device_map="auto",
    )
    model.eval()

    output = generate(PROMPT, model, device='cuda')

    print(output)


if __name__ == "__main__":
    main()
