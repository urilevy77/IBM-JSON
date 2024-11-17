from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

# Load the tokenizer and model
model_id = "mistralai/Mixtral-8x7B-Instruct-v0.1"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id, device_map="auto", torch_dtype="auto")

# Create a text generation pipeline
text_gen_pipeline = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_length=512,
    temperature=0.7,  # Adjust for randomness in responses
    top_p=0.95,       # Adjust for nucleus sampling
)

# Define a simple prompt
prompt = "You are a helpful assistant. Answer the following question:\nWhat is your favorite programming language and why?"

# Generate a response
response = text_gen_pipeline(prompt, max_new_tokens=100)

# Print the response
print("Response from Mixtral model:")
print(response[0]['generated_text'])
