import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

torch.random.manual_seed(0)

model_id = "microsoft/Phi-3.5-mini-instruct"

# Prefer Apple GPU if available
device = "mps" if torch.backends.mps.is_available() else "cpu"
print(torch.backends.cuda)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map='auto',
    torch_dtype="auto",
)
model.to(device)

tokenizer = AutoTokenizer.from_pretrained(model_id)

pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
)

messages = [
    {"role": "system", "content": "You are a helpful AI assistant."},
    {"role": "user", "content": "Can you provide ways to eat combinations of bananas and dragonfruits?"},
    {"role": "assistant", "content": "Sure! Here are some ways to eat bananas and dragonfruits together: 1. Banana and dragonfruit smoothie: Blend bananas and dragonfruits together with some milk and honey. 2. Banana and dragonfruit salad: Mix sliced bananas and dragonfruits together with some lemon juice and honey."},
    {"role": "user", "content": "What about solving a 2x + 3 = 7 equation?"},
]

generation_args = {
    "max_new_tokens": 500,      # much smaller for testing
    "return_full_text": False,
    "temperature": 1.0,        # deterministic and lighter
    "do_sample": False,
}

output = pipe(messages, **generation_args)
print(output[0]["generated_text"])