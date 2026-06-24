from ollama import chat

BOSS_SYSTEM_PROMPT = """
You are an AI business analyst.

Analyze sales data and business statistics.

Give short and useful recommendations.

Always answer in Uzbek.

Do not show reasoning.
Do not output think tags.
Only give the final answer.
"""


def ask_boss_ai(question: str, analytics: str):

    prompt = f"""
    Quyidagi biznes ma'lumotlariga asoslanib javob ber.

    {analytics}

    Boss savoli:
    {question}

    Faqat javob ber.
    Promptdagi matnlarni takrorlama.
"""

    response = chat(
        model="qwen3:4b",
        messages=[
            {
                "role": "system",
                "content": BOSS_SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        think=False
    )

    msg = response["message"]["content"]

    if "</think>" in msg:
        msg = msg.split("</think>")[-1].strip()

    return msg


from app.services.boss_analytics_service import (
    get_total_revenue,
    get_total_sales,
    get_top_products,
    get_low_stock_products
)


def build_analytics_context(db):

    revenue = get_total_revenue(db)

    sales = get_total_sales(db)

    top_products = get_top_products(db)

    low_stock = get_low_stock_products(db)

    context = f"""
Total Revenue: {revenue}
Total Sales: {sales}

Top Products:
"""

    for product in top_products[:5]:
        context += (
            f"\n{product.name} - "
            f"{product.sales_count} sales"
        )

    context += "\n\nLow Stock Products:"

    for product in low_stock:
        context += (
            f"\n{product.name} "
            f"(stock={product.stock})"
        )

    return context