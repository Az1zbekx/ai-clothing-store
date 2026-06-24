import re

def ask_boss_ai(question: str, analytics: str):
    """
    Boss savollariga tez, aniq va xatosiz o'zbek tilida javob qaytarish tizimi.
    Kichik model o'zbek tilida yaxshi gapira olmagani uchun qat'iy shablonlar qo'llaniladi.
    """
    q = question.lower()
    
    # Intentlarni aniqlaymiz
    if any(word in q for word in ["eng ko'p", "ko'p sotilgan", "mashhur", "top"]):
        # Top products
        match = re.search(r'Top Products:\s*(.*?)\s*Low Stock Products:', analytics, re.DOTALL)
        if match:
            top_prods = [line.strip('- \n') for line in match.group(1).strip().split('\n') if line.strip()]
            if top_prods:
                return f"Eng ko'p sotilgan mahsulotlar:\n" + "\n".join(f"🏆 {p}" for p in top_prods[:3])
        return "Hozircha sotuvlar haqida ma'lumot yo'q."

    elif any(word in q for word in ["kam qolgan", "tugagan", "tugab qolgan", "qolmagan", "past", "zaxira"]):
        # Low stock
        match = re.search(r'Low Stock Products:\s*(.*?)\s*Recent Sales:', analytics, re.DOTALL)
        if match:
            low_stock = [line.strip('- \n') for line in match.group(1).strip().split('\n') if line.strip()]
            if low_stock and low_stock[0] != "No low stock products":
                return f"Zaxirasi kam qolgan mahsulotlar (zudlik bilan olib kelish kerak):\n" + "\n".join(f"⚠️ {p}" for p in low_stock[:5])
        return "Barcha mahsulotlar zaxirasi yetarli darajada! ✅"

    elif any(word in q for word in ["daromad", "foyda", "summa", "pul", "tushum"]):
        match = re.search(r'Total Revenue:\s*([\d\.\,\s]+)', analytics)
        if match:
            rev = match.group(1).strip()
            return f"Umumiy daromad: 💰 {rev} so'm.\nSavdolarni oshirish uchun marketingni kuchaytirishni tavsiya qilaman."
        return "Daromad ma'lumotlari topilmadi."

    elif any(word in q for word in ["savdo", "sotuv", "nechta"]):
        match = re.search(r'Total Sales:\s*(\d+)', analytics)
        if match:
            sales = match.group(1).strip()
            return f"Jami {sales} ta mahsulot sotilgan. 📈"
        return "Hali sotuvlar amalga oshirilmagan."
        
    elif any(word in q for word in ["o'rtacha", "chek", "order"]):
        match = re.search(r'Average Order Value:\s*([\d\.\,\s]+)', analytics)
        if match:
            avg = match.group(1).strip()
            return f"Bitta xaridning o'rtacha qiymati: 🧾 {avg} so'm."
        return "O'rtacha xarid qiymati topilmadi."

    elif any(word in q for word in ["foydalanuvchi", "mijoz", "odam", "user"]):
        match = re.search(r'Total Users:\s*(\d+)', analytics)
        if match:
            users = match.group(1).strip()
            return f"Do'konda jami 👥 {users} ta ro'yxatdan o'tgan mijoz bor."
        return "Mijozlar statistikasi topilmadi."

    elif any(word in q for word in ["salom", "qalay", "yaxshimi"]):
        return "Assalomu alaykum, Boss! 📊 Men sizning AI biznes tahlilchingizman. Qanday ma'lumot kerak?"

    # Agar hech qaysi qolipga tushmasa, umumiy xulosa beramiz:
    rev_match = re.search(r'Total Revenue:\s*([\d\.\,\s]+)', analytics)
    rev = rev_match.group(1).strip() if rev_match else "0"
    
    return (
        f"📊 Qisqacha hisobot:\n"
        f"Jami daromad: {rev} so'm.\n"
        f"Zaxirasi kam qolgan tovarlarni to'ldirishni va reklama byudjetini qayta ko'rib chiqishni tavsiya qilaman. "
        f"Aniqroq ma'lumot uchun 'eng ko'p sotilgan', 'daromad', 'kam qolgan' deb so'rang."
    )


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

