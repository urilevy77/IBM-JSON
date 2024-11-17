# Use a pipeline as a high-level helper
from transformers import pipeline,AutoTokenizer, AutoModelForCausalLM
model_id = "mistralai/Mixtral-8x7B-Instruct-v0.1"
pipe = pipeline("text-generation", model="mistralai/Mixtral-8x7B-Instruct-v0.1")
pipe(messages)

# Load model directly


tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id,device_map="auto")

messages = [
    {"role": "user", "content": "What is your favourite condiment?"},
    {"role": "assistant", "content": "Well, I'm quite partial to a good squeeze of fresh lemon juice. It adds just the right amount of zesty flavour to whatever I'm cooking up in the kitchen!"},
    {"role": "user", "content": "Do you have mayonnaise recipes?"}
]

inputs = tokenizer.apply_chat_template(messages, return_tensors="pt").to("cuda")
