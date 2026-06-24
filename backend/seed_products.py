import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.database import SessionLocal
from app.models.product import Product
from app.services.embedding_service import create_embedding

products_data = [
    ("Oq Paxta Futbolka", "Yozgi oddiy oq paxta futbolka", "Futbolka", "Oq", "Yoz", "S", 45000, 20),
    ("Qora Slim Jins", "Zamonaviy slim fit qora jins", "Shim", "Qora", "Bahor/Kuz", "M", 120000, 15),
    ("Ko'k Denim Jaket", "Klassik ko'k denim jaket", "Jaket", "Ko'k", "Bahor/Kuz", "L", 180000, 10),
    ("Yashil Yozgi Ko'ylak", "Engil yashil yozgi ko'ylak", "Ko'ylak", "Yashil", "Yoz", "M", 75000, 18),
    ("Qizil Hoodie", "Issiq qizil hoodie kofta", "Kofta", "Qizil", "Qish", "L", 150000, 12),
    ("Kulrang Sweatshirt", "Sport kulrang sweatshirt", "Kofta", "Kulrang", "Bahor/Kuz", "XL", 95000, 25),
    ("Sariq Yoz Ko'ylagi", "Gul naqshli sariq ko'ylak", "Ko'ylak", "Sariq", "Yoz", "S", 65000, 30),
    ("Qoʻngʻir Teri Jaket", "Sifatli sun'iy teri jaket", "Jaket", "Qo'ng'ir", "Qish", "M", 350000, 8),
    ("Binafsha Sport Shim", "Qulay binafsha jogger shim", "Shim", "Binafsha", "Bahor", "L", 85000, 22),
    ("To'q Ko'k Polo", "Klassik to'q ko'k polo futbolka", "Futbolka", "To'q Ko'k", "Bahor/Yoz", "M", 70000, 16),
    ("Oq Kelin Ko'ylak", "Nafis oq ko'ylak", "Ko'ylak", "Oq", "Bahor", "S", 210000, 5),
    ("Qora Charm Shimcha", "Zamonaviy qora charm shortlar", "Shim", "Qora", "Yoz", "M", 95000, 14),
    ("Ko'k Yozgi Shirt", "Engil matoli ko'k shirt", "Ko'ylak", "Ko'k", "Yoz", "L", 80000, 20),
    ("Limon Rangli T-shirt", "Yorqin limon rangli futbolka", "Futbolka", "Limon", "Yoz", "S", 40000, 35),
    ("Jigarrang Cardigan", "Yumshoq jigarrang cardigan", "Kofta", "Jigarrang", "Kuz/Qish", "M", 130000, 10),
    ("Zangori Yozgi Shim", "Yengil zangori yozgi shim", "Shim", "Zangori", "Yoz", "L", 90000, 18),
    ("Pushti Ko'ylak", "Nozik pushti ko'ylak", "Ko'ylak", "Pushti", "Bahor", "S", 110000, 12),
    ("Qoʻshimcha Katta Futbolka", "Oversize qora futbolka", "Futbolka", "Qora", "Bahor/Yoz", "XL", 55000, 28),
    ("Tuproq Rangi Chino", "Klassik chino shim", "Shim", "Tuproq", "Bahor/Kuz", "M", 100000, 15),
    ("Moviy Puffer Jaket", "Issiq moviy puffer jaket", "Jaket", "Moviy", "Qish", "L", 280000, 7),
    ("Oq Linen Ko'ylak", "Tabiiy kattan oq ko'ylak", "Ko'ylak", "Oq", "Yoz", "M", 125000, 13),
    ("Qora Turtleneck", "Yumshoq qora bo'g'zi baland kofta", "Kofta", "Qora", "Qish", "M", 115000, 9),
    ("Ko'k Cargo Shim", "Ko'p cho'ntakli cargo shim", "Shim", "Ko'k", "Bahor/Kuz", "L", 145000, 11),
    ("Qizil Bomber Jaket", "Zamonaviy qizil bomber jaket", "Jaket", "Qizil", "Kuz", "M", 200000, 6),
    ("Oq Paxta Shim", "Qulay oq paxta shim", "Shim", "Oq", "Yoz", "S", 75000, 20),
    ("Kulrang Polo", "Oddiy kulrang polo futbolka", "Futbolka", "Kulrang", "Bahor/Yoz", "M", 65000, 25),
    ("Yashil Army Jaket", "Harbiy uslubdagi yashil jaket", "Jaket", "Yashil", "Kuz", "L", 240000, 8),
    ("Qoʻngʻir Turtle Kofta", "Issiq jigarrang turtleneck", "Kofta", "Qo'ng'ir", "Qish", "M", 120000, 14),
    ("Binafsha Futbolka", "Oddiy binafsha futbolka", "Futbolka", "Binafsha", "Yoz", "S", 42000, 30),
    ("Kulrang Jogger Shim", "Sport kulrang jogger", "Shim", "Kulrang", "Bahor", "L", 88000, 22),
    ("Sariq Bomber", "Yorqin sariq bomber jaket", "Jaket", "Sariq", "Kuz", "M", 190000, 7),
    ("Ko'k Angora Kofta", "Yumshoq ko'k angora kofta", "Kofta", "Ko'k", "Qish", "S", 160000, 10),
    ("Qoʻngʻir Denim Shim", "Klassik jigarrang denim", "Shim", "Qo'ng'ir", "Bahor/Kuz", "M", 130000, 16),
    ("Oq Oversize Ko'ylak", "Keng oq ko'ylak", "Ko'ylak", "Oq", "Bahor/Yoz", "L", 95000, 20),
    ("Qizil Zip Kofta", "Zamokli qizil kofta", "Kofta", "Qizil", "Kuz", "M", 105000, 12),
    ("Zangori Denim Shim", "Klassik zangori denim", "Shim", "Zangori", "Bahor/Kuz", "M", 115000, 18),
    ("Qora Blazer", "Rasmiy qora blazer", "Jaket", "Qora", "Bahor/Kuz", "L", 320000, 5),
    ("Yashil Hoodie", "Katta kapyushonli yashil kofta", "Kofta", "Yashil", "Qish", "XL", 145000, 15),
    ("Pushti Futbolka", "Oddiy pushti futbolka", "Futbolka", "Pushti", "Yoz", "S", 38000, 35),
    ("Kulrang Chino Shim", "Qulay kulrang chino", "Shim", "Kulrang", "Bahor", "M", 98000, 18),
    ("Ko'k Paxta Futbolka", "Oddiy ko'k paxta futbolka", "Futbolka", "Ko'k", "Yoz", "L", 44000, 28),
    ("Oq Blazer", "Rasmiy oq blazer", "Jaket", "Oq", "Bahor/Yoz", "M", 300000, 6),
    ("Qora Sport Shim", "Qulay qora sport shim", "Shim", "Qora", "Bahor", "L", 80000, 20),
    ("Tuproq Hoodie", "Qulay tuproq rangi hoodie", "Kofta", "Tuproq", "Kuz/Qish", "M", 135000, 13),
    ("Ko'k Linen Shim", "Yozgi ko'k kattan shim", "Shim", "Ko'k", "Yoz", "M", 95000, 16),
    ("Qizil Polo Futbolka", "Klassik qizil polo", "Futbolka", "Qizil", "Bahor/Yoz", "L", 68000, 22),
    ("Jigarrang Bomber", "Issiq jigarrang bomber", "Jaket", "Jigarrang", "Kuz/Qish", "M", 220000, 8),
    ("Oq Triko Ko'ylak", "Nafis triko ko'ylak", "Ko'ylak", "Oq", "Bahor", "S", 140000, 10),
    ("Kulrang Turtleneck", "Issiq kulrang bo'g'zi baland", "Kofta", "Kulrang", "Qish", "M", 110000, 14),
    ("Sariq Cargo Shim", "Ko'p cho'ntakli sariq cargo", "Shim", "Sariq", "Kuz", "L", 155000, 9),
    ("Yashil Polo Futbolka", "Klassik yashil polo", "Futbolka", "Yashil", "Bahor/Yoz", "M", 65000, 25),
    ("Moviy Cardigan", "Yumshoq moviy cardigan", "Kofta", "Moviy", "Kuz", "S", 125000, 11),
    ("Qora Denim Jaket", "Klassik qora denim jaket", "Jaket", "Qora", "Bahor/Kuz", "L", 185000, 9),
    ("Pushti Chino Shim", "Qulay pushti chino", "Shim", "Pushti", "Bahor/Yoz", "M", 92000, 17),
    ("Ko'k Hoodie", "Katta ko'k hoodie", "Kofta", "Ko'k", "Qish", "XL", 148000, 12),
    ("Oq Cargo Shim", "Funksional oq cargo shim", "Shim", "Oq", "Yoz", "L", 138000, 10),
    ("Qizil Futbolka", "Oddiy qizil futbolka", "Futbolka", "Qizil", "Yoz", "S", 40000, 30),
    ("Jigarrang Cardigan", "Issiq jigarrang cardigan kofta", "Kofta", "Jigarrang", "Kuz/Qish", "M", 132000, 13),
    ("Kulrang Bomber Jaket", "Zamonaviy kulrang bomber", "Jaket", "Kulrang", "Kuz", "L", 195000, 7),
    ("Binafsha Chino", "Zamonaviy binafsha chino", "Shim", "Binafsha", "Bahor", "M", 96000, 14),
    ("Oq Polo Futbolka", "Klassik oq polo", "Futbolka", "Oq", "Yoz", "M", 66000, 25),
    ("Yashil Puffer Jaket", "Engil yashil puffer", "Jaket", "Yashil", "Qish", "M", 275000, 8),
    ("Qora Ko'ylak", "Rasmiy qora ko'ylak", "Ko'ylak", "Qora", "Bahor/Kuz", "L", 145000, 10),
    ("Ko'k Triko Kofta", "Yumshoq ko'k triko kofta", "Kofta", "Ko'k", "Kuz", "S", 118000, 14),
    ("Sariq Futbolka", "Yorqin sariq futbolka", "Futbolka", "Sariq", "Yoz", "M", 43000, 28),
    ("Qoʻngʻir Cargo Shim", "Jigarrang cargo shim", "Shim", "Qo'ng'ir", "Kuz", "L", 150000, 11),
    ("Oq Denim Jaket", "Yozgi oq denim jaket", "Jaket", "Oq", "Bahor/Yoz", "M", 175000, 9),
    ("Pushti Hoodie", "Yumshoq pushti hoodie", "Kofta", "Pushti", "Kuz/Qish", "S", 140000, 15),
    ("Kulrang Futbolka", "Oddiy kulrang futbolka", "Futbolka", "Kulrang", "Bahor/Yoz", "L", 42000, 32),
    ("Ko'k Chino Shim", "Zamonaviy ko'k chino", "Shim", "Ko'k", "Bahor", "M", 99000, 16),
    ("Qizil Blazer", "Yorqin qizil blazer", "Jaket", "Qizil", "Bahor/Kuz", "M", 310000, 5),
    ("Yashil Futbolka", "Oddiy yashil futbolka", "Futbolka", "Yashil", "Yoz", "S", 41000, 30),
    ("Limon Hoodie", "Yorqin limon rangi hoodie", "Kofta", "Limon", "Kuz", "L", 142000, 12),
    ("Qora Angora Kofta", "Yumshoq qora angora", "Kofta", "Qora", "Qish", "M", 165000, 9),
    ("Zangori Polo", "Klassik zangori polo", "Futbolka", "Zangori", "Yoz", "M", 67000, 20),
    ("Jigarrang Slim Jins", "Slim fit jigarrang jins", "Shim", "Jigarrang", "Bahor/Kuz", "L", 122000, 14),
    ("Oq Zip Kofta", "Zamokli oq sport kofta", "Kofta", "Oq", "Bahor", "M", 108000, 11),
    ("Moviy Futbolka", "Oddiy moviy futbolka", "Futbolka", "Moviy", "Yoz", "S", 39000, 33),
    ("Kulrang Puffer Jaket", "Issiq kulrang puffer jaket", "Jaket", "Kulrang", "Qish", "L", 265000, 7),
    ("Pushti Cardigan", "Nozik pushti cardigan", "Kofta", "Pushti", "Bahor/Kuz", "S", 128000, 13),
    ("Ko'k Oversize Futbolka", "Oversize ko'k futbolka", "Futbolka", "Ko'k", "Yoz", "XL", 52000, 25),
    ("Qoʻngʻir Hoodie", "Issiq jigarrang hoodie", "Kofta", "Qo'ng'ir", "Qish", "M", 145000, 11),
    ("Sariq Linen Ko'ylak", "Yozgi sariq kattan ko'ylak", "Ko'ylak", "Sariq", "Yoz", "S", 115000, 14),
    ("Qora Zip Jaket", "Zamokli qora jaket", "Jaket", "Qora", "Kuz", "L", 230000, 8),
    ("Yashil Chino Shim", "Qulay yashil chino", "Shim", "Yashil", "Bahor", "M", 94000, 17),
    ("Oq Angora Kofta", "Yumshoq oq angora kofta", "Kofta", "Oq", "Qish", "S", 168000, 8),
    ("Ko'k Blazer", "Rasmiy ko'k blazer", "Jaket", "Ko'k", "Bahor/Kuz", "M", 315000, 5),
    ("Qizil Cardigan", "Yorqin qizil cardigan", "Kofta", "Qizil", "Kuz", "L", 127000, 12),
    ("Zangori Cargo Shim", "Funksional zangori cargo", "Shim", "Zangori", "Kuz", "M", 148000, 10),
    ("Pushti Polo", "Nozik pushti polo futbolka", "Futbolka", "Pushti", "Yoz", "S", 63000, 22),
    ("Kulrang Ko'ylak", "Rasmiy kulrang ko'ylak", "Ko'ylak", "Kulrang", "Bahor/Kuz", "L", 135000, 9),
    ("Binafsha Hoodie", "Issiq binafsha hoodie", "Kofta", "Binafsha", "Qish", "M", 143000, 12),
    ("Sariq Denim Jaket", "Yozgi sariq denim jaket", "Jaket", "Sariq", "Yoz", "S", 170000, 8),
    ("Ko'k Sport Shim", "Sport ko'k jogger", "Shim", "Ko'k", "Bahor", "L", 82000, 20),
    ("Oq Turtleneck", "Klassik oq turtleneck", "Kofta", "Oq", "Qish", "M", 112000, 13),
    ("Qizil Linen Ko'ylak", "Yozgi qizil kattan ko'ylak", "Ko'ylak", "Qizil", "Yoz", "M", 118000, 11),
    ("Yashil Angora Kofta", "Yumshoq yashil angora kofta", "Kofta", "Yashil", "Qish", "S", 162000, 9),
    ("Qoʻngʻir Blazer", "Klassik jigarrang blazer", "Jaket", "Qo'ng'ir", "Bahor/Kuz", "L", 305000, 5),
    ("Moviy Hoodie", "Qulay moviy hoodie", "Kofta", "Moviy", "Kuz/Qish", "M", 139000, 14),
    ("Kulrang Polo Futbolka", "Sport kulrang polo", "Futbolka", "Kulrang", "Bahor/Yoz", "L", 64000, 24),
    ("Sariq Sport Shim", "Yorqin sariq sport shim", "Shim", "Sariq", "Yoz", "S", 78000, 19),
    ("Oq Summer Ko'ylak", "Engil oq yozgi ko'ylak", "Ko'ylak", "Oq", "Yoz", "M", 102000, 15),
]


def seed():
    db = SessionLocal()
    count = db.query(Product).count()
    if count >= 100:
        print(f"Already {count} products in DB. Skipping.")
        db.close()
        return

    print(f"Adding {len(products_data)} products...")
    for i, (name, desc, category, color, season, size, price, stock) in enumerate(products_data):
        print(f"[{i+1}/{len(products_data)}] {name}...")
        text = f"{name} {desc}"
        embedding = create_embedding(text)
        product = Product(
            name=name,
            description=desc,
            category=category,
            color=color,
            season=season,
            size=size,
            price=price,
            stock=stock,
            embedding=embedding
        )
        db.add(product)
        db.commit()

    print("Done! 100 products added.")
    db.close()


if __name__ == "__main__":
    seed()
