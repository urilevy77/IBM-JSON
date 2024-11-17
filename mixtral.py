from transformers import AutoModelForCausalLM, AutoTokenizer

# Load the model and tokenizer
model_id = "mistralai/Mixtral-8x7B-Instruct-v0.1"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id, device_map="auto")

# Define the messages for the conversation
messages = [
    {"role": "user", "content": "What is your favourite condiment?"},
    {"role": "assistant", "content": "Well, I'm quite partial to a good squeeze of fresh lemon juice. It adds just the right amount of zesty flavour to whatever I'm cooking up in the kitchen!"},
    {"role": "user", ''"content": "Do you have mayonnaise recipes?"}
]

# Tokenize the conversation
inputs = tokenizer(messages, return_tensors="pt", padding=True, truncation=True).to("cuda")

# Generate the response
outputs = model.generate(inputs['input_ids'], max_new_tokens=20)

# Decode the response
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
