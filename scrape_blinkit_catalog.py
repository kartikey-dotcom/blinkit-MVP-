"""
scrape_blinkit_catalog.py
Script to generate the Blinkit Product Catalog CSV and JSON dataset for BlinkSmart MVP.
"""

import pandas as pd
import json

# Comprehensive Blinkit Product Catalog across 19 Official Platform Categories
BLINKIT_CATALOG_DATA = [
    # 1. Dairy, Bread & Eggs
    {"id": "amul_milk_1l", "name": "Amul Taaza T-Special Milk 1L", "category": "Dairy, Bread & Eggs", "price": 72, "mrp": 75, "emoji": "🥛"},
    {"id": "amul_butter_100g", "name": "Amul Pasteurised Salted Butter 100g", "category": "Dairy, Bread & Eggs", "price": 60, "mrp": 62, "emoji": "🧈"},
    {"id": "harvest_bread_white", "name": "Harvest Gold White Bread 400g", "category": "Dairy, Bread & Eggs", "price": 40, "mrp": 40, "emoji": "🍞"},
    {"id": "harvest_brown_bread", "name": "Harvest Gold 100% Whole Wheat Brown Bread 400g", "category": "Dairy, Bread & Eggs", "price": 50, "mrp": 50, "emoji": "🍞"},
    {"id": "eggoz_white_6", "name": "Eggoz Farm Fresh White Eggs (6 pcs)", "category": "Dairy, Bread & Eggs", "price": 65, "mrp": 70, "emoji": "🥚"},
    {"id": "eggoz_brown_10", "name": "Eggoz Organic Brown Eggs (10 pcs)", "category": "Dairy, Bread & Eggs", "price": 135, "mrp": 150, "emoji": "🥚"},
    {"id": "epigamia_greek_yogurt", "name": "Epigamia Greek Yogurt Mango 100g", "category": "Dairy, Bread & Eggs", "price": 60, "mrp": 65, "emoji": "🥭"},
    {"id": "mother_dairy_paneer", "name": "Mother Dairy Fresh Paneer 200g", "category": "Dairy, Bread & Eggs", "price": 92, "mrp": 95, "emoji": "🧀"},

    # 2. Fruits & Vegetables
    {"id": "fresh_avocado_2", "name": "Fresh Imported Hass Avocado (2 pcs)", "category": "Fruits & Vegetables", "price": 299, "mrp": 350, "emoji": "🥑"},
    {"id": "fresh_tomatoes_500g", "name": "Fresh Hybrid Tomatoes 500g", "category": "Fruits & Vegetables", "price": 28, "mrp": 35, "emoji": "🍅"},
    {"id": "fresh_onions_1kg", "name": "Fresh Red Onions 1kg", "category": "Fruits & Vegetables", "price": 42, "mrp": 50, "emoji": "🧅"},
    {"id": "fresh_potatoes_1kg", "name": "Fresh New Crop Potatoes 1kg", "category": "Fruits & Vegetables", "price": 38, "mrp": 45, "emoji": "🥔"},
    {"id": "fresh_bananas_6", "name": "Fresh Robusta Bananas (6 pcs)", "category": "Fruits & Vegetables", "price": 45, "mrp": 50, "emoji": "🍌"},
    {"id": "fresh_apples_4", "name": "Fresh Royal Gala Apples (4 pcs)", "category": "Fruits & Vegetables", "price": 180, "mrp": 220, "emoji": "🍎"},
    {"id": "fresh_coriander", "name": "Fresh Green Coriander Bunch 100g", "category": "Fruits & Vegetables", "price": 15, "mrp": 20, "emoji": "🌿"},
    {"id": "fresh_lemon_200g", "name": "Fresh Juicy Yellow Lemons (200g)", "category": "Fruits & Vegetables", "price": 35, "mrp": 40, "emoji": "🍋"},

    # 3. Grocery & Staples
    {"id": "aashirvaad_atta_5kg", "name": "Aashirvaad Shuddh Chakki Atta 5kg", "category": "Grocery & Staples", "price": 245, "mrp": 270, "emoji": "🌾"},
    {"id": "fortune_sunflower_oil", "name": "Fortune Sunlite Sunflower Oil 1L", "category": "Grocery & Staples", "price": 145, "mrp": 160, "emoji": "🛢️"},
    {"id": "daawat_basmati_rice", "name": "Daawat Rozana Super Basmati Rice 5kg", "category": "Grocery & Staples", "price": 380, "mrp": 450, "emoji": "🍚"},
    {"id": "tata_sampann_toor_dal", "name": "Tata Sampann Unpolished Toor Dal 1kg", "category": "Grocery & Staples", "price": 175, "mrp": 195, "emoji": "🍲"},
    {"id": "tata_salt_1kg", "name": "Tata Salt Vacuum Evaporated Iodized Salt 1kg", "category": "Grocery & Staples", "price": 28, "mrp": 28, "emoji": "🧂"},
    {"id": "catch_turmeric_powder", "name": "Catch Turmeric Powder (Haldi) 200g", "category": "Grocery & Staples", "price": 52, "mrp": 58, "emoji": "🟡"},
    {"id": "mdh_deggi_mirch", "name": "MDH Deggi Mirch Red Chilli Powder 100g", "category": "Grocery & Staples", "price": 88, "mrp": 95, "emoji": "🌶️"},

    # 4. Munchies & Snacks
    {"id": "doritos_nacho_150g", "name": "Doritos Nacho Cheese Chips 150g", "category": "Munchies & Snacks", "price": 60, "mrp": 60, "emoji": "🧀"},
    {"id": "lays_magic_masala", "name": "Lay's India's Magic Masala Chips 50g", "category": "Munchies & Snacks", "price": 20, "mrp": 20, "emoji": "🥔"},
    {"id": "haldiram_bhujia_400g", "name": "Haldiram's Plain Bhujia Sev 400g", "category": "Munchies & Snacks", "price": 120, "mrp": 130, "emoji": "🥨"},
    {"id": "act2_popcorn_butter", "name": "Act II Instant Butter Popcorn 150g", "category": "Munchies & Snacks", "price": 50, "mrp": 55, "emoji": "🍿"},
    {"id": "kurkure_masala_munch", "name": "Kurkure Masala Munch Crunchy Snack 90g", "category": "Munchies & Snacks", "price": 20, "mrp": 20, "emoji": "🔥"},
    {"id": "pringles_sour_cream", "name": "Pringles Sour Cream & Onion Potato Chips 107g", "category": "Munchies & Snacks", "price": 115, "mrp": 135, "emoji": "🥫"},

    # 5. Beverages & Cold Drinks
    {"id": "red_bull_250ml", "name": "Red Bull Energy Drink 250ml", "category": "Beverages & Cold Drinks", "price": 125, "mrp": 125, "emoji": "⚡"},
    {"id": "coke_zero_300ml", "name": "Coca-Cola Zero Sugar 300ml Can", "category": "Beverages & Cold Drinks", "price": 40, "mrp": 40, "emoji": "🥤"},
    {"id": "thums_up_750ml", "name": "Thums Up Soft Drink 750ml Bottle", "category": "Beverages & Cold Drinks", "price": 40, "mrp": 40, "emoji": "🍾"},
    {"id": "real_mixed_fruit", "name": "Real Fruit Power Mixed Fruit Juice 1L", "category": "Beverages & Cold Drinks", "price": 110, "mrp": 130, "emoji": "🧃"},
    {"id": "bisleri_water_5l", "name": "Bisleri Packaged Drinking Water Jar 5L", "category": "Beverages & Cold Drinks", "price": 70, "mrp": 75, "emoji": "💧"},

    # 6. Tea, Coffee & Health Drinks
    {"id": "blue_tokai_dark_roast", "name": "Blue Tokai Dark Roast Coffee Beans 250g", "category": "Tea, Coffee & Health Drinks", "price": 490, "mrp": 550, "emoji": "☕"},
    {"id": "nescafe_classic_100g", "name": "Nescafe Classic Instant Coffee Powder 100g", "category": "Tea, Coffee & Health Drinks", "price": 340, "mrp": 375, "emoji": "☕"},
    {"id": "tata_tea_gold_500g", "name": "Tata Tea Gold Premium Black Tea 500g", "category": "Tea, Coffee & Health Drinks", "price": 310, "mrp": 350, "emoji": "🍃"},
    {"id": "tetley_green_tea", "name": "Tetley Green Tea Lemon & Honey (25 Bags)", "category": "Tea, Coffee & Health Drinks", "price": 180, "mrp": 210, "emoji": "🍵"},
    {"id": "bournvita_500g", "name": "Cadbury Bournvita Chocolate Health Drink 500g", "category": "Tea, Coffee & Health Drinks", "price": 240, "mrp": 265, "emoji": "🍫"},

    # 7. Instant & Frozen Food
    {"id": "maggi_2min_noodles", "name": "Maggi 2-Minute Masala Instant Noodles (4 Pack)", "category": "Instant & Frozen Food", "price": 56, "mrp": 60, "emoji": "🍜"},
    {"id": "quaker_oats_1kg", "name": "Quaker Rolled Whole Oats 1kg", "category": "Instant & Frozen Food", "price": 190, "mrp": 225, "emoji": "🥣"},
    {"id": "mccain_french_fries", "name": "McCain Crispy French Fries 420g", "category": "Instant & Frozen Food", "price": 125, "mrp": 140, "emoji": "🍟"},
    {"id": "kellogg_corn_flakes", "name": "Kellogg's Real Almond & Honey Corn Flakes 300g", "category": "Instant & Frozen Food", "price": 210, "mrp": 235, "emoji": "🥣"},
    {"id": "yippee_noodles_pack", "name": "Sunfeast YiPPee! Magic Masala Noodles (4 Pack)", "category": "Instant & Frozen Food", "price": 52, "mrp": 56, "emoji": "🍜"},

    # 8. Sweet Tooth, Chocolates & Bakery
    {"id": "cadbury_silk_150g", "name": "Cadbury Dairy Milk Silk Chocolate 150g", "category": "Sweet Tooth, Chocolates & Bakery", "price": 175, "mrp": 180, "emoji": "🍫"},
    {"id": "nutella_spread_350g", "name": "Nutella Hazelnut Cocoa Spread 350g", "category": "Sweet Tooth, Chocolates & Bakery", "price": 395, "mrp": 420, "emoji": "🍫"},
    {"id": "ferrero_rocher_16", "name": "Ferrero Rocher Premium Chocolates (16 Pack)", "category": "Sweet Tooth, Chocolates & Bakery", "price": 625, "mrp": 699, "emoji": "🍬"},
    {"id": "kwality_vanilla_brick", "name": "Kwality Wall's Vanilla Ice Cream Tub 700ml", "category": "Sweet Tooth, Chocolates & Bakery", "price": 160, "mrp": 180, "emoji": "🍨"},

    # 9. Beauty & Cosmetics
    {"id": "derma_co_sunscreen", "name": "The Derma Co 1% Hyaluronic Sunscreen Aqua Gel 50g", "category": "Beauty & Cosmetics", "price": 449, "mrp": 499, "emoji": "☀️"},
    {"id": "minimalist_vit_c", "name": "Minimalist 10% Vitamin C Face Serum 30ml", "category": "Beauty & Cosmetics", "price": 664, "mrp": 699, "emoji": "🧴"},
    {"id": "garnier_micellar_water", "name": "Garnier Skin Naturals Micellar Cleansing Water 125ml", "category": "Beauty & Cosmetics", "price": 199, "mrp": 225, "emoji": "🧼"},
    {"id": "maybelline_mascara", "name": "Maybelline New York Hypercurl Waterproof Mascara", "category": "Beauty & Cosmetics", "price": 349, "mrp": 399, "emoji": "💄"},

    # 10. Bath, Body & Personal Care
    {"id": "cetaphil_cleanser_125ml", "name": "Cetaphil Gentle Skin Cleanser 125ml", "category": "Bath, Body & Personal Care", "price": 335, "mrp": 375, "emoji": "🧴"},
    {"id": "colgate_maxfresh_150g", "name": "Colgate MaxFresh Red Gel Toothpaste 150g", "category": "Bath, Body & Personal Care", "price": 115, "mrp": 130, "emoji": "🪥"},
    {"id": "dettol_soap_3pack", "name": "Dettol Original Germ Protection Bathing Soap (3 Pack)", "category": "Bath, Body & Personal Care", "price": 140, "mrp": 155, "emoji": "🧼"},
    {"id": "dove_shampoo_340ml", "name": "Dove Intense Repair Hair Shampoo 340ml", "category": "Bath, Body & Personal Care", "price": 280, "mrp": 325, "emoji": "🧴"},
    {"id": "nivea_body_lotion", "name": "Nivea Nourishing Body Milk Lotion 200ml", "category": "Bath, Body & Personal Care", "price": 240, "mrp": 275, "emoji": "🧴"},

    # 11. Electronics & Tech Accessories
    {"id": "spigen_20w_charger", "name": "Spigen 20W Fast Type-C Wall Charger Adapter", "category": "Electronics & Tech Accessories", "price": 899, "mrp": 1499, "emoji": "🔌"},
    {"id": "boat_airdopes_141", "name": "boAt Airdopes 141 True Wireless Earbuds", "category": "Electronics & Tech Accessories", "price": 1299, "mrp": 4490, "emoji": "🎧"},
    {"id": "portronics_type_c_cable", "name": "Portronics Konnect L 3A Type-C Fast Charging Cable 1.2m", "category": "Electronics & Tech Accessories", "price": 199, "mrp": 499, "emoji": "⚡"},
    {"id": "mi_10000mah_powerbank", "name": "Mi Power Bank 3i 10000mAh 18W Fast Charging", "category": "Electronics & Tech Accessories", "price": 1299, "mrp": 2199, "emoji": "🔋"},

    # 12. Home & Kitchen Utilities
    {"id": "instacuppa_frother", "name": "InstaCuppa Electric Milk Frother & Hand Mixer", "category": "Home & Kitchen Utilities", "price": 799, "mrp": 1200, "emoji": "⚡"},
    {"id": "portronics_kitchen_scale", "name": "Portronics Digital Kitchen Weight Scale (1g to 10kg)", "category": "Home & Kitchen Utilities", "price": 399, "mrp": 999, "emoji": "⚖️"},
    {"id": "pigeon_electric_kettle", "name": "Pigeon 1.5L Stainless Steel Electric Kettle", "category": "Home & Kitchen Utilities", "price": 649, "mrp": 1195, "emoji": "🫖"},
    {"id": "portronics_phone_stand", "name": "Portronics Multi-Angle Desktop Phone Stand", "category": "Home & Kitchen Utilities", "price": 249, "mrp": 699, "emoji": "📱"},
    {"id": "borosil_fondue_bowl", "name": "Borosil Microwave Safe Glass Dessert & Fondue Bowl", "category": "Home & Kitchen Utilities", "price": 299, "mrp": 499, "emoji": "🥣"},

    # 13. Cleaning & Household Essentials
    {"id": "surf_excel_matic_top", "name": "Surf Excel Matic Top Load Washing Powder 1kg", "category": "Cleaning & Household Essentials", "price": 215, "mrp": 235, "emoji": "🧺"},
    {"id": "colin_surface_cleaner", "name": "Colin Glass and Surface Cleaner Spray 500ml", "category": "Cleaning & Household Essentials", "price": 105, "mrp": 120, "emoji": "🧹"},
    {"id": "vim_dishwash_liquid", "name": "Vim Gel Lemon Dishwash Liquid Bottle 500ml", "category": "Cleaning & Household Essentials", "price": 125, "mrp": 140, "emoji": "🧽"},
    {"id": "origami_tissue_box", "name": "Origami 2-Ply Facial Tissue Box (200 Sheets)", "category": "Cleaning & Household Essentials", "price": 95, "mrp": 110, "emoji": "🧻"},

    # 14. Baby Care
    {"id": "pampers_baby_wipes", "name": "Pampers Fresh Clean Baby Wipes (80 Sheets)", "category": "Baby Care", "price": 185, "mrp": 225, "emoji": "👶"},
    {"id": "pampers_diapers_m", "name": "Pampers All-in-One Pants Diapers Medium (30 Count)", "category": "Baby Care", "price": 540, "mrp": 649, "emoji": "👶"},
    {"id": "sebamed_baby_lotion", "name": "Sebamed Baby Gentle Body Lotion 200ml", "category": "Baby Care", "price": 540, "mrp": 600, "emoji": "🍼"},

    # 15. Pet Care
    {"id": "pedigree_dog_food_1kg", "name": "Pedigree Adult Dry Dog Food Chicken & Vegetables 1.2kg", "category": "Pet Care", "price": 380, "mrp": 410, "emoji": "🐶"},
    {"id": "whiskas_cat_wet_food", "name": "Whiskas Wet Cat Food Ocean Fish (4 Pack x 85g)", "category": "Pet Care", "price": 195, "mrp": 220, "emoji": "🐱"},

    # 16. Health, Pharma & Wellness
    {"id": "ors_apple_drink", "name": "Enerzal ORS Apple Electrolyte Drink 200ml", "category": "Health, Pharma & Wellness", "price": 32, "mrp": 35, "emoji": "🧃"},
    {"id": "volini_spray_50g", "name": "Volini Pain Relief Spray 50g", "category": "Health, Pharma & Wellness", "price": 165, "mrp": 185, "emoji": "💊"},
    {"id": "dettol_plaster_strips", "name": "Dettol Adhesive Antiseptic Bandages (10 Strips)", "category": "Health, Pharma & Wellness", "price": 30, "mrp": 35, "emoji": "🩹"},

    # 17. Stationery, Books & Games
    {"id": "classmate_notebook", "name": "Classmate Pulse Long Spiral Notebook (200 Pages)", "category": "Stationery, Books & Games", "price": 90, "mrp": 100, "emoji": "📓"},
    {"id": "parker_gel_pen", "name": "Parker Vector Stainless Steel Gel Pen", "category": "Stationery, Books & Games", "price": 275, "mrp": 300, "emoji": "🖊️"},
    {"id": "uno_cards_classic", "name": "Mattel UNO Classic Card Game", "category": "Stationery, Books & Games", "price": 149, "mrp": 199, "emoji": "🃏"},

    # 18. Paan & Party Essentials
    {"id": "orbit_spearmint_gum", "name": "Orbit Spearmint Sugarfree Chewing Gum 22g", "category": "Paan & Party Essentials", "price": 50, "mrp": 50, "emoji": "🍬"},
    {"id": "catch_club_soda_750ml", "name": "Catch Club Soda 750ml", "category": "Paan & Party Essentials", "price": 20, "mrp": 20, "emoji": "🥤"},

    # 19. Meat, Fish & Eggs
    {"id": "licious_chicken_breast", "name": "Fresh Boneless Chicken Breast 400g", "category": "Meat, Fish & Eggs", "price": 245, "mrp": 275, "emoji": "🍗"}
]

def generate_catalog_files():
    df = pd.DataFrame(BLINKIT_CATALOG_DATA)
    df.to_csv("blinkit_catalog.csv", index=False)
    
    with open("blinkit_catalog.json", "w", encoding="utf-8") as f:
        json.dump(BLINKIT_CATALOG_DATA, f, indent=4)
        
    print(f"Generated Blinkit Product Catalog: {len(df)} SKUs across {len(df['category'].unique())} Categories saved to blinkit_catalog.csv and blinkit_catalog.json")

if __name__ == "__main__":
    generate_catalog_files()
