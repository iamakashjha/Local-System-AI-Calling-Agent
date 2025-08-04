import torch
from huggingface_hub import login
from transformers import AutoTokenizer, AutoModelForCausalLM


tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-1_5")
model = AutoModelForCausalLM.from_pretrained("microsoft/phi-1_5")
model.to("cpu") 

with open("call_script_prompt.txt", "r") as f:
    system_prompt = f.read()

def generate_reply(conversation, customer_input):
    prompt = (
        "You are a polite banking agent calling a customer for an overdraft facility. "
        "Stick to the script. Keep responses under 200 words.\n\n"
        + conversation
        + f"Customer: {customer_input}\nAgent:"
    )
    input_text = f"{system_prompt}\n{prompt}"
    inputs = tokenizer(input_text, return_tensors="pt")
    outputs = model.generate(
        **inputs,
        max_new_tokens=1000,
        temperature=0.5,
        pad_token_id=tokenizer.eos_token_id,
        do_sample=True,
    )
    generated = tokenizer.decode(outputs[0], skip_special_tokens=True)
    reply = generated.split("Agent:")[-1].strip()
    return reply

