from ollama import chat

GENERAL_CHAT_TEMPLATES = {
    "salom": "Salom! Men AI savdo yordamchisiman. Sizga qanday kiyim tanlashda yordam bera olaman? 😊",
    "assalom": "Assalomu alaykum! Sizga qanday kiyim tanlashda yordam bera olaman? 😊",
    "qalay": "Rahmat, men doim yordam berishga tayyorman! 😊 Siz qanday kiyim qidiryapsiz?",
    "qanday": "Rahmat, men doim yordam berishga tayyorman! 😊 Siz qanday kiyim qidiryapsiz?",
    "yaxshimi": "Rahmat, yaxshiman! 😊 Sizga qanday kiyim kerak?",
    "rahmat": "Sizga ham rahmat! Yana qanday kiyim kerak bo'lsa, bemalol murojaat qiling. 😊",
    "tashakkur": "Arzimaydi! Yana qanday kiyim kerak bo'lsa, yordam berishga tayyorman. 😊",
    "isming": "Mening ismim Moda. Men sizga mos va chiroyli kiyimlar topishda yordam beruvchi AI yordamchiman! ✨",
    "kimsan": "Men sizga kiyim tanlashda yordam beruvchi AI savdo yordamchisiman. 😊",
    "nima gap": "Hamma narsa a'lo! 😊 Do'konimizdagi kiyimlarni ko'rishni xohlaysizmi?",
    "hayr": "Xayr! Yaxshi kun tilayman. 😊",
    "xayr": "Salomat bo'ling! Yana kutib qolamiz. 😊",
}

def ask_general_chat(message: str) -> str:
    """Oddiy gaplashish (salomlashish, hol-ahvol so'rash) uchun shablonlar va model"""
    msg_lower = message.lower()
    
    # Avval shablonlarni tekshiramiz
    for kw, template in GENERAL_CHAT_TEMPLATES.items():
        if kw in msg_lower:
            return template

    # Agar shablon topilmasa, model bilan harakat qilamiz
    SYSTEM_PROMPT = """Sen "AI Clothing Store" do'konining o'zbek tilida gapiruvchi yordamchisisan.
Javobingni 1 ta qisqa gap qilib yoz (maksimum 10 so'z).
Hech qachon ruscha yoki qozoqcha so'zlarni ishlatma."""

    try:
        response = chat(
            model="qwen2.5:1.5b",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f'Mijoz aytdi: "{message}". Unga qisqa, do\'stona o\'zbek tilida javob ber.'}
            ],
            options={
                "temperature": 0.4,
                "top_p": 0.8,
                "repeat_penalty": 1.2,
                "num_predict": 30
            },
            think=False
        )
        msg = response["message"]["content"]
        if "</think>" in msg:
            msg = msg.split("</think>")[-1].strip()
        msg = msg.strip('"').strip("'").strip()
        
        # Validatsiya
        words = msg.split()
        if not msg or len(words) < 2 or len(words) > 15:
            return "Tushunmadim, lekin sizga qanday kiyim kerakligini aytsangiz yordam beraman! 😊"
            
        has_cyrillic = any('\u0400' <= c <= '\u04ff' for c in msg)
        if has_cyrillic or ":" in msg or "-" in msg:
            return "Salom! Sizga qanday kiyim topishda yordam bera olaman? 😊"
            
        return msg
    except Exception:
        return "Salom! Men AI savdo yordamchisiman. Qanday kiyim qidiryapsiz? 😊"
