import ollama
import json
import os

MEMORY_FILE = "memory.json"

# Load structured memory
if os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "r") as f:
        memory = json.load(f)
else:
    memory = {"tasks_completed": [], "tasks_pending": []}

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    system_prompt = f"""
    You are a personal assistant.
    Completed tasks: {memory['tasks_completed']}
    Pending tasks: {memory['tasks_pending']}
    """

    response = ollama.chat(
        model='llama3.2:latest',  # faster model
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
    )

    ai_reply = response['message']['content']
    print("AI:", ai_reply)

    memory['conversation_history']['question_asked'].append(user_input)
    memory['conversation_history']['response'].append(ai_reply)

    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)
