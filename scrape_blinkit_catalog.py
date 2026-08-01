"""
scrape_blinkit_catalog.py
Script to generate the Blinkit 12-Category Catalog CSV dataset for BlinkSmart MVP.
"""

import pandas as pd

CATALOG_DATA = [
    # 1. Dairy & Breakfast
    {"id": "DB-001", "name": "Amul Taaza Milk 1L", "category": "Dairy & Breakfast", "price": 54, "mrp": 54, "emoji": "🥛"},
    {"id": "DB-002", "name": "Amul Pasteurised Butter 100g", "category": "Dairy & Breakfast", "price": 58, "mrp": 60, "emoji": "🧈"},
    {"id": "DB-003", "name": "Harvest Gold Bread", "category": "Dairy & Breakfast", "price": 45, "mrp": 50, "emoji": "🍞"},
    {"id": "DB-004", "name": "Eggoz Farm Fresh Eggs (6 pcs)", "category": "Dairy & Breakfast", "price": 65, "mrp": 75, "emoji": "🥚"},
    {"id": "DB-005", "name": "Epigamia Greek Yogurt", "category": "Dairy & Breakfast", "price": 50, "mrp": 55, "emoji": "🍨"},

    # 2. Fruits & Vegetables
    {"id": "FV-001", "name": "Fresh Imported Hass Avocado (2 pcs)", "category": "Fruits & Vegetables", "price": 189, "mrp": 220, "emoji": "🥑"},
    {"id": "FV-002", "name": "Fresh Hybrid Tomatoes 500g", "category": "Fruits & Vegetables", "price": 24, "mrp": 35, "emoji": "🍅"},
    {"id": "FV-003", "name": "Bananas (6 pcs)", "category": "Fruits & Vegetables", "price": 48, "mrp": 60, "emoji": "🍌"},

    # 3. Grocery & Staples
    {"id": "GS-001", "name": "Fortune Sunflower Oil 1L", "category": "Grocery & Staples", "price": 145, "mrp": 170, "emoji": "🌻"},
    {"id": "GS-002", "name": "Aashirvaad Atta 5kg", "category": "Grocery & Staples", "price": 235, "mrp": 275, "emoji": "🌾"},

    # 4. Munchies & Snacks
    {"id": "MS-001", "name": "Doritos Nacho Cheese 150g", "category": "Munchies & Snacks", "price": 85, "mrp": 95, "emoji": "📐"},
    {"id": "MS-002", "name": "Lay's Magic Masala 90g", "category": "Munchies & Snacks", "price": 40, "mrp": 45, "emoji": "🍟"},

    # 5. Beverages & Cold Drinks
    {"id": "BC-001", "name": "Red Bull Energy Drink 250ml", "category": "Beverages & Cold Drinks", "price": 115, "mrp": 125, "emoji": "⚡"},
    {"id": "BC-002", "name": "Coca-Cola Zero Sugar 300ml", "category": "Beverages & Cold Drinks", "price": 38, "mrp": 40, "emoji": "🥤"},

    # 6. Gourmet & Specialty
    {"id": "GS-101", "name": "Blue Tokai Dark Roast Coffee Beans 250g", "category": "Gourmet & Specialty", "price": 490, "mrp": 550, "emoji": "☕"},
    {"id": "GS-102", "name": "Nutella Hazelnut Spread 350g", "category": "Gourmet & Specialty", "price": 375, "mrp": 425, "emoji": "🌰"},

    # 7. Sweet Tooth & Bakery
    {"id": "SB-001", "name": "Cadbury Dairy Milk Silk Chocolate 150g", "category": "Sweet Tooth & Bakery", "price": 175, "mrp": 195, "emoji": "🍫"},

    # 8. Electronics & Tech
    {"id": "ET-001", "name": "Spigen 20W Type-C Fast Charger", "category": "Electronics & Tech", "price": 999, "mrp": 1499, "emoji": "🔌"},
    {"id": "ET-002", "name": "boAt Airdopes 141", "category": "Electronics & Tech", "price": 1299, "mrp": 2990, "emoji": "🎧"},
    {"id": "ET-003", "name": "Portronics 6-in-1 Type-C HDMI Hub", "category": "Electronics & Tech", "price": 1499, "mrp": 2499, "emoji": "💻"},

    # 9. Beauty & Personal Care
    {"id": "BP-001", "name": "Minimalist 10% Vitamin C Face Serum 30ml", "category": "Beauty & Personal Care", "price": 664, "mrp": 699, "emoji": "🧴"},
    {"id": "BP-002", "name": "The Derma Co 1% Hyaluronic Sunscreen 50g", "category": "Beauty & Personal Care", "price": 449, "mrp": 499, "emoji": "☀️"},

    # 10. Home & Kitchen
    {"id": "HK-001", "name": "InstaCuppa Electric Coffee Frother", "category": "Home & Kitchen", "price": 999, "mrp": 1499, "emoji": "☕"},
    {"id": "HK-002", "name": "Pigeon 1.5L Electric Kettle", "category": "Home & Kitchen", "price": 699, "mrp": 1195, "emoji": "🫖"},

    # 11. Baby Care
    {"id": "BC-201", "name": "Pampers Fresh Clean Baby Wipes (80 sheets)", "category": "Baby Care", "price": 189, "mrp": 225, "emoji": "👶"},
    {"id": "BC-202", "name": "Sebamed Baby Gentle Lotion 200ml", "category": "Baby Care", "price": 629, "mrp": 699, "emoji": "🍼"},

    # 12. Pet Care
    {"id": "PC-001", "name": "Pedigree Adult Dry Dog Food 1.2kg", "category": "Pet Care", "price": 380, "mrp": 420, "emoji": "🐶"},
    {"id": "PC-002", "name": "Whiskas Wet Cat Food Ocean Fish 85g", "category": "Pet Care", "price": 50, "mrp": 55, "emoji": "🐱"}
]

def generate_catalog():
    df = pd.DataFrame(CATALOG_DATA)
    output_path = "blinkit_catalog.csv"
    df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"Generated {len(df)} SKUs across 12 Blinkit categories in '{output_path}'.")

if __name__ == "__main__":
    generate_catalog()
