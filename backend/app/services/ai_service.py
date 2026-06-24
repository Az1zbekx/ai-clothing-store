from ollama import chat

SYSTEM_PROMPT = """Sen "AI Clothing Store" do'konining savdo yordamchisisisan.
Faqat O'zbek tilida gapir.
Qisqa va do'stona javob ber — 1-2 jumla.
Mahsulotlar ro'yxatini o'zing sanama, ular UI da ko'rsatiladi.
Faqat "Mana siz uchun topganlarim:" yoki "Albatta, quyidagilarni ko'rib chiqing:" kabi qisqa kirish gapini yoz.
"""


def ask_ai(message: str, products_text: str):
    if products_text.strip():
        user_prompt = f"""Mijoz: {message}

Biz unga quyidagi mahsulotlarni topib berdik:
{products_text}

Mijozga do'stona va qisqa (1-2 jumla) kirish gapi yoz. Mahsulot nomlarini takrorlama, ular alohida ko'rsatiladi."""
    else:
        user_prompt = f"""Mijoz: {message}

Afsuski, bu turdagi mahsulot hozir do'konda yo'q. Buning haqida do'stona va qisqa xabar ber."""

    response = chat(
        model="qwen2.5:1.5b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        think=False
    )

    msg = response["message"]["content"]
    if "</think>" in msg:
        msg = msg.split("</think>")[-1].strip()

    return msg