from transformers import pipeline
from fastapi import FastAPI

# -----------------------------
# LOAD MODEL
# -----------------------------
print("🔥 Loading model...")
llm = pipeline("text-generation", model="gpt2")
# -----------------------------
# SIMPLE MEMORY (NO LANGCHAIN)
# -----------------------------
chat_history = []

def ask_llm(prompt):
    response = llm(
        prompt,
        max_new_tokens=50,
        do_sample=False,
        pad_token_id=50256   # avoids other warnings too
    )
    return response[0]["generated_text"]

def chat_with_memory(user_input):
    # Convert history list → text
    history_text = "\n".join(chat_history)

    prompt = f"""
Conversation so far:
{history_text}

User: {user_input}
AI:
"""

    response = ask_llm(prompt)

    # Save conversation
    chat_history.append(f"User: {user_input}")
    chat_history.append(f"AI: {response}")

    return response

# -----------------------------
# CALCULATOR TOOL
# -----------------------------
def calculator_tool(text):
    try:
        return str(eval(text))
    except:
        return "Cannot calculate"

# -----------------------------
# AGENT (DECISION MAKER)
# -----------------------------
def agent(user_input):
    if "calculate" in user_input.lower():
        expression = user_input.lower().replace("calculate", "").strip()
        return calculator_tool(expression)
    else:
        return chat_with_memory(user_input)

# -----------------------------
# FASTAPI
# -----------------------------
app = FastAPI()

@app.get("/")
def home():
    return {"message": "API working 🚀"}

@app.get("/chat")
def chat(message: str):
    reply = agent(message)
    return {"response": reply}