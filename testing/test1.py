from transformers import LlamaForCausalLM, CodeLlamaTokenizer, AutoModelForCausalLM, GPTQConfig
import transformers
import torch
from torch import bfloat16

device =  "cuda" if torch.cuda.is_available() else "cpu"

tokenizer = CodeLlamaTokenizer.from_pretrained("codellama/CodeLlama-13b-Instruct-hf")

bnb_config = transformers.BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type='nf4',
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=bfloat16
)

# gptq_config = GPTQConfig(bits=4, dataset = "c4", tokenizer=tokenizer)
# print(f'gpqt_config{gptq_config}')

model = AutoModelForCausalLM.from_pretrained("codellama/CodeLlama-13b-Instruct-hf",trust_remote_code=True, quantization_config = bnb_config,device_map='auto' )
model.eval()
print(f"Model loaded on {device}")



PROMPT = '''<!DOCTYPE html>
<html>
 <!-- a Website for selling old clothes, with a orange thee black navbar with title 'Omkar' onLeft and a login button on right, also add css in this html as style-->
 <FILL_ME>

</html>
'''

prompt = '''
Make a Website in HTML for selling old clothes, with a orange thee black navbar with title 'Omkar' onLeft and a login button on right, use css in this html as style.
'''

input_ids = tokenizer(PROMPT, return_tensors="pt",device=device)["input_ids"]
print(f'{input_ids=}')
generated_ids = model.generate(input_ids.to(device), max_new_tokens=768)
print("Generated")

filling = tokenizer.batch_decode(generated_ids[:, input_ids.shape[1]:], skip_special_tokens = True)[0]
print(filling)
print("--------------------------------------")
print(PROMPT.replace(" <FILL_ME>", filling))

# input_ids = tokenizer(prompt, return_tensors="pt")["input_ids"]
# generated_ids = model.generate(input_ids, max_new_tokens=256)
# filling = tokenizer.batch_decode(generated_ids[:, input_ids.shape[1]:], skip_special_tokens = True)[0]
# print(filling)