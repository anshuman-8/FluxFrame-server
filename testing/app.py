import os
import torch
import transformers
import logging as log
# from dotenv import load_dotenv

# load_dotenv()

MAX_INPUT_TOKEN_LENGTH = 4000
MAX_TOKEN = 2048
log.basicConfig(level=log.INFO, format=" %(levelname)s %(message)s")

SYSTEM_PROMPT = """
You are a helpful code writer with a deep knowledge of HTML, CSS, Web-development and software design. Follow all the instructions provided, but can also give more features.\nDo not give multiple answers or repeat things. Make beautiful designs using CSS based on your creativity.\nPlease don't provide wrong code. \n Give a complete solution with maximum number of feature. Code practice: Give all the CSS inside <style> tag mapped with class names and id. Do not link any files to head link tag. You may also write necessary correct javascript by creating functions inside <script> tag, use buttons calling function and don't use form. Always check if all the components are correctly written and mapped.\
"""

PROMPT = "Design a website that takes two input from user and display the sum of two numbers in a box."

def get_prompt(message: str,system_prompt: str) -> str:
    texts = [f'<s>[INST] <<SYS>>\n{system_prompt}\n<</SYS>>\n\n{message}:\n\n<!DOCTYPE html> <html><FILL_ME></html>[/INST]']
    
    log.info(f'Prompt: {texts}')
    return ''.join(texts)


def write_to_html(filename, content):
    with open(filename, 'w') as file:
        file.write(content)
        file.close()

def generate(prompt, model, device):
    tokenizer = transformers.CodeLlamaTokenizer.from_pretrained(
        "codellama/CodeLlama-13b-Instruct-hf"
    )
    processed_prompt = get_prompt(prompt,SYSTEM_PROMPT)
    input_ids = tokenizer(processed_prompt, return_tensors="pt", device=device)["input_ids"]
    generated_ids = model.generate(input_ids.to(device), max_new_tokens=MAX_TOKEN)
    filling = tokenizer.batch_decode(generated_ids[:, input_ids.shape[1] :], skip_special_tokens=True)[0]
    # gen_code = prompt.replace(" <FILL_ME>", filling)
    gen_code = f'<!DOCTYPE html>\n<html>\n{filling}</html>'
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
