from ollama import chat

from ollama import chat

def ask_ai(message: str, products_text: str):

    prompt = f"""
Siz professional kiyim do'koni AI sotuvchisiz.

Mijoz savoli:
{message}

Eng mos mahsulotlar:

{products_text}

Faqat shu mahsulotlarga asoslanib javob bering.
Narx, rang, mavsum va o'lchamlarni ayting.
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