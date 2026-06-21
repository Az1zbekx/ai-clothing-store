from ollama import chat

SYSTEM_PROMPT = """
IMPORTANT:
- Do not show reasoning.
- Do not output <think> tags.
- Output only the final answer.
- If customer writes 'salom', respond in Uzbek.

You are AI Clothing Store virtual sales assistant.

Always answer directly.
Never show reasoning.
Never explain your thinking.
Only output the final answer for the customer.
"""


def ask_ai(message: str, products_text: str):

    user_prompt = f"""
AVAILABLE PRODUCTS:

{products_text}

CUSTOMER MESSAGE:

{message}
"""

    response = chat(
        model="qwen3:4b",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        think=False
    )

    print(response)

    msg = response["message"]["content"]

    if "</think>" in msg:
        msg = msg.split("</think>")[-1].strip()

    return msg