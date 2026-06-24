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
        model="qwen2.5:1.5b",
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
    get_low_stock_products,
    get_total_users,
    get_total_products,
    get_average_order_value,
    get_recent_sales
)

def build_analytics_context(db):

    revenue = get_total_revenue(db)
    sales = get_total_sales(db)
    top_products = get_top_products(db)
    low_stock = get_low_stock_products(db)

    users = get_total_users(db)
    products = get_total_products(db)
    avg_order = get_average_order_value(db)

    recent_sales = get_recent_sales(db)

    context = f"""
Business Statistics

Total Revenue: {revenue}
Total Sales: {sales}
Total Users: {users}
Total Products: {products}
Average Order Value: {avg_order}

Top Products:
"""

    for product in top_products[:5]:

        try:
            context += (
                f"\n{product.name} - "
                f"{product.sales_count} sales"
            )

        except AttributeError:
            context += (
                f"\n{product[0]} - "
                f"{product[1]} sales"
            )

    context += "\n\nLow Stock Products:"

    if low_stock:

        for product in low_stock:

            context += (
                f"\n{product.name} "
                f"(stock={product.stock})"
            )

    else:
        context += "\nNo low stock products"

    context += "\n\nRecent Sales:"

    if recent_sales:

        for sale in recent_sales:

            context += (
                f"\nSale ID: {sale.id}"
                f" | Product ID: {sale.product_id}"
                f" | Quantity: {sale.quantity}"
                f" | Price: {sale.total_price}"
            )

    else:
        context += "\nNo sales found"

    return context

