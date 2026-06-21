from ollama import chat

def ask_ai(message: str, products_text: str):

    prompt = f"""
Siz kiyim do'koni AI sotuvchisiz.

Bizdagi mahsulotlar:

{products_text}

Mijoz savoli:
{message}

Faqat mavjud mahsulotlarga asoslanib javob bering.
"""

    response = chat(
        model="qwen3:4b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]