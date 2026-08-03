import streamlit as st
import json
import requests
import pandas as pd
import os
import re
from dotenv import load_dotenv

# Silently load environment variables / Streamlit secrets (Zero API key UI display)
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_AI_STUDIO_API_KEY") or st.secrets.get("GEMINI_API_KEY", "")

# Robust helper function to clean inline HTML strings
def clean_html(html_str):
    lines = [line.strip() for line in html_str.splitlines() if line.strip()]
    return " ".join(lines)

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Blinkit Quick Commerce | Mobile App MVP",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for System Auto Theme Detection (prefers-color-scheme: dark & light)
st.markdown(clean_html("""
<style>
:root {
    --app-bg: #F4F6FB;
    --card-bg: #FFFFFF;
    --text-primary: #111827;
    --text-secondary: #475569;
    --border-color: #E2E8F0;
    --status-bar-bg: #FFFFFF;
    --rationale-bg: #F8FAFC;
    --pill-bg: #F0FDF4;
    --pill-border: #BBF7D0;
    --pill-text: #0C831F;
    --home-indicator: #CBD5E1;
}

@media (prefers-color-scheme: dark) {
    :root {
        --app-bg: #0F172A;
        --card-bg: #1E293B;
        --text-primary: #F8FAFC;
        --text-secondary: #CBD5E1;
        --border-color: #334155;
        --status-bar-bg: #1E293B;
        --rationale-bg: #0F172A;
        --pill-bg: #064E3B;
        --pill-border: #059669;
        --pill-text: #34D399;
        --home-indicator: #475569;
    }
}

/* Force Streamlit Body & Container Theme Adaptability */
.main { background-color: var(--app-bg) !important; padding: 10px 0; transition: background 0.3s ease; }
.stApp { background-color: var(--app-bg) !important; color: var(--text-primary) !important; font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', Roboto, sans-serif; }

/* Hide default streamlit headers/footers */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }

/* Streamlit Inputs & Dropdowns Theme Customization */
.stTextInput input, .stSelectbox select, div[data-baseweb="select"] > div {
    background-color: var(--card-bg) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border-color) !important;
}

/* iOS Top Status Bar & Dynamic Island */
.ios-status-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 16px 4px 16px;
    font-size: 12px;
    font-weight: 700;
    color: var(--text-primary);
    background-color: var(--status-bar-bg);
    border-top-left-radius: 20px;
    border-top-right-radius: 20px;
    border-bottom: 1px solid var(--border-color);
}

.dynamic-island-pill {
    width: 110px;
    height: 24px;
    background-color: #000000;
    border-radius: 20px;
}

.blinkit-logo-badge {
    background-color: #F7C200;
    color: #000000;
    font-weight: 900;
    padding: 6px 14px;
    border-radius: 8px;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    font-size: 20px;
    display: inline-block;
    letter-spacing: -0.5px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
}

.delivery-pill {
    background-color: var(--pill-bg);
    border: 1.5px solid var(--pill-border);
    color: var(--pill-text);
    font-weight: 800;
    font-size: 11px;
    padding: 4px 12px;
    border-radius: 20px;
    display: inline-block;
    text-align: center;
}

.nudge-card {
    background: var(--card-bg);
    border: 1.5px solid #10B981;
    border-radius: 16px;
    padding: 16px;
    margin-top: 14px;
    margin-bottom: 14px;
    box-shadow: 0 4px 15px rgba(16, 185, 129, 0.12);
    color: var(--text-primary);
}

.nudge-tag {
    background-color: #0C831F;
    color: #FFFFFF;
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 10px;
    font-weight: 800;
    text-transform: uppercase;
}

.scenario-badge {
    background-color: #F7C200;
    color: #000000;
    font-weight: 800;
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 11px;
    display: inline-block;
}

.rationale-box {
    background-color: var(--rationale-bg) !important;
    border: 1.5px solid #10B981 !important;
    border-radius: 12px;
    padding: 12px;
    margin-top: 10px;
    margin-bottom: 12px;
    color: var(--text-primary) !important;
}

.shield-badge {
    background-color: #FEF08A;
    color: #854D0E;
    font-weight: 700;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 11px;
}

/* Primary Green CTA Button (Checkout & Catalog Add) */
.stButton > button {
    background-color: #0C831F !important;
    color: #FFFFFF !important;
    font-weight: 800 !important;
    border-radius: 10px !important;
    border: none !important;
    padding: 8px 14px !important;
    font-size: 13px !important;
    width: 100% !important;
    box-shadow: 0 2px 4px rgba(12, 131, 31, 0.2) !important;
}
.stButton > button:hover {
    background-color: #096818 !important;
    color: #FFFFFF !important;
}

/* Secondary CTA (Nudge Add-on Button): Distinct Blinkit Gold (#F7C200) with dark text */
.nudge-btn-wrapper .stButton > button {
    background-color: #F7C200 !important;
    color: #111827 !important;
    border: 1.5px solid #0C831F !important;
    font-weight: 800 !important;
    box-shadow: 0 2px 6px rgba(247, 194, 0, 0.3) !important;
}
.nudge-btn-wrapper .stButton > button:hover {
    background-color: #E5B200 !important;
    color: #000000 !important;
}

/* iOS Bottom Tab Bar */
.ios-tab-bar {
    display: flex;
    justify-content: space-around;
    align-items: center;
    background-color: var(--status-bar-bg);
    border-top: 1px solid var(--border-color);
    padding: 10px 0 6px 0;
    margin-top: 20px;
    border-radius: 16px;
    box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
}

.ios-tab-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    font-size: 10px;
    font-weight: 600;
    color: var(--text-secondary);
}

.ios-tab-item.active {
    color: #0C831F;
    font-weight: 800;
}

.ios-home-indicator {
    width: 134px;
    height: 5px;
    background-color: var(--home-indicator);
    border-radius: 100px;
    margin: 10px auto 4px auto;
}
</style>
"""), unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# iOS DYNAMIC ISLAND & STATUS BAR
# -----------------------------------------------------------------------------
ios_status_html = clean_html("""
<div class="ios-status-bar">
    <span>9:41</span>
    <div class="dynamic-island-pill"></div>
    <span>📶 🛜 🔋 100%</span>
</div>
""")
st.markdown(ios_status_html, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# DYNAMIC BLINKIT CATALOG LOADING
# -----------------------------------------------------------------------------
@st.cache_data
def load_blinkit_catalog():
    if os.path.exists("blinkit_catalog.csv"):
        df = pd.read_csv("blinkit_catalog.csv")
        return df.to_dict(orient="records")
    else:
        from scrape_blinkit_catalog import BLINKIT_CATALOG_DATA
        return BLINKIT_CATALOG_DATA

CATALOG_LIST = load_blinkit_catalog()
CATALOG_DF = pd.DataFrame(CATALOG_LIST)

# -----------------------------------------------------------------------------
# BLINKSMART AI ENGINE (COMPLETE 19-CATEGORY MATRIX & DYNAMIC LATEST-ITEM ROUTING)
# -----------------------------------------------------------------------------
ROUTING_MATRIX = [
    # 1. Dairy, Bread & Eggs
    {
        "categories": ["dairy, bread & eggs"],
        "keywords": ["milk", "butter", "bread", "egg", "yogurt", "paneer", "amul", "eggoz", "harvest", "epigamia", "mother dairy"],
        "primary": {
            "title": "Electric Stainless Steel Milk Frother & Foamer",
            "mrp": 799, "price": 399, "emoji": "⚡", "sku": "301",
            "scenario_badge": "☕ 15-Sec Micro-Foam & Whisk",
            "why_suggested": "Whisk egg batters, Greek yogurt smoothies, or hot milk coffee to velvety perfection.",
            "cobuying_utility": "Whisk egg batters, Greek yogurt smoothies, or hot milk coffee to velvety perfection in 15 seconds.",
            "social_proof": "👥 63 dairy & breakfast buyers in DLF Phase 3 bought this this week"
        },
        "secondary": {
            "title": "Portronics Digital Kitchen Weight Scale (1g to 10kg)",
            "mrp": 999, "price": 399, "emoji": "⚖️", "sku": "602",
            "scenario_badge": "⚖️ Exact Ingredient Precision",
            "why_suggested": "Accurately measure baking flour, protein, and recipe proportions.",
            "cobuying_utility": "Accurately measure baking flour, protein, and recipe proportions for health tracking.",
            "social_proof": "👥 31 home cooks nearby bought this this week"
        }
    },
    # 2. Fruits & Vegetables
    {
        "categories": ["fruits & vegetables"],
        "keywords": ["avocado", "tomatoes", "onions", "potatoes", "bananas", "apples", "coriander", "lemons", "fresh"],
        "primary": {
            "title": "Portronics Digital Kitchen Weight Scale (1g to 10kg)",
            "mrp": 999, "price": 399, "emoji": "⚖️", "sku": "602",
            "scenario_badge": "⚖️ Produce & Macro Precision",
            "why_suggested": "Accurately measure smoothie portions, avocado macros, and salad ingredients.",
            "cobuying_utility": "Accurately measure smoothie portions, avocado macros, and salad ingredients, or clean hands after prepping.",
            "social_proof": "👥 42 fitness & salad lovers nearby added this this week"
        },
        "secondary": {
            "title": "Pure Water Refreshing Wet Wipes (Pack of 15)",
            "mrp": 99, "price": 49, "emoji": "🧼", "sku": "001",
            "scenario_badge": "🧼 Instant Food Prep Cleanup",
            "why_suggested": "Quickly sanitize hands after handling raw produce or peeling vegetables.",
            "cobuying_utility": "Instantly wipes away dirt, sticky juices, and residue from hands during food prep.",
            "social_proof": "👥 48 grocery buyers in your neighborhood added this this week"
        }
    },
    # 3. Grocery & Staples
    {
        "categories": ["grocery & staples"],
        "keywords": ["atta", "oil", "rice", "dal", "salt", "turmeric", "haldi", "mirch", "chilli", "aashirvaad", "fortune", "daawat", "tata"],
        "primary": {
            "title": "Pigeon 1.5L Stainless Steel Electric Kettle",
            "mrp": 1195, "price": 649, "emoji": "🫖", "sku": "603",
            "scenario_badge": "⚡ Instant Hot Water Prep",
            "why_suggested": "Instant boiling water to speed up rice, dal, and atta dough prep times in the kitchen.",
            "cobuying_utility": "Instant boiling water to speed up rice, dal, and atta dough prep times in the kitchen.",
            "social_proof": "👥 54 kitchen users in Gurgaon Sector 43 bought this this week"
        },
        "secondary": {
            "title": "Portronics Digital Kitchen Weight Scale (1g to 10kg)",
            "mrp": 999, "price": 399, "emoji": "⚖️", "sku": "602",
            "scenario_badge": "⚖️ Staple Portion Scale",
            "why_suggested": "Measure exact grain and dal portions for daily family meals.",
            "cobuying_utility": "Accurately weigh grain, pulse, and flour portions for meal prep.",
            "social_proof": "👥 29 home chefs added this this week"
        }
    },
    # 4. Munchies & Snacks
    {
        "categories": ["munchies & snacks"],
        "keywords": ["doritos", "chips", "lays", "bhujia", "popcorn", "kurkure", "pringles", "nachos", "snack"],
        "primary": {
            "title": "Pure Water Refreshing Wet Wipes (Pack of 15)",
            "mrp": 99, "price": 49, "emoji": "🧼", "sku": "001",
            "scenario_badge": "🧼 Finger & Masala Cleanup",
            "why_suggested": "Essential cleanup utility for snack time.",
            "cobuying_utility": "Instantly wipes away masala grease, seasoning, and oil from fingers without leaving sticky residue.",
            "social_proof": "👥 48 snack buyers in your neighborhood added this this week"
        }
    },
    # 5. Beverages & Cold Drinks
    {
        "categories": ["beverages & cold drinks"],
        "keywords": ["red bull", "coke", "coca-cola", "thums up", "juice", "water", "bisleri", "soda", "drink"],
        "primary": {
            "title": "Insulated Neoprene Cold Can Cooler Sleeve",
            "mrp": 199, "price": 99, "emoji": "🥤", "sku": "002",
            "scenario_badge": "❄️ Sub-Zero Can Thermal Chill",
            "why_suggested": "Keeps chilled cans, juices, and energy drinks cold 2x longer without messy condensation.",
            "cobuying_utility": "Keeps chilled cans, juices, and energy drinks cold 2x longer without messy condensation.",
            "social_proof": "👥 19 beverage buyers nearby added this this week"
        }
    },
    # 6. Tea, Coffee & Health Drinks
    {
        "categories": ["tea, coffee & health drinks"],
        "keywords": ["coffee", "tokai", "nescafe", "tea", "tetley", "green tea", "bournvita", "chai", "espresso"],
        "primary": {
            "title": "Electric Stainless Steel Milk Frother & Foamer",
            "mrp": 799, "price": 399, "emoji": "⚡", "sku": "301",
            "scenario_badge": "☕ 15-Second Cafe Micro-Foam",
            "why_suggested": "Create rich, cafe-style micro-foam for cappuccinos, lattes, green teas, and health drinks right at home.",
            "cobuying_utility": "Create rich, cafe-style micro-foam for cappuccinos, lattes, green teas, and health drinks right at home.",
            "social_proof": "👥 63 coffee lovers in DLF Phase 3 bought this this week"
        }
    },
    # 7. Instant & Frozen Food
    {
        "categories": ["instant & frozen food"],
        "keywords": ["maggi", "oats", "french fries", "mccain", "corn flakes", "yippee", "noodles"],
        "primary": {
            "title": "Pigeon 1.5L Stainless Steel Electric Kettle",
            "mrp": 1195, "price": 649, "emoji": "🫖", "sku": "603",
            "scenario_badge": "⚡ 2-Min Rapid Hot Water",
            "why_suggested": "Boil water in under 2 minutes for lightning-fast instant noodles, oatmeal, and hot snacks.",
            "cobuying_utility": "Boil water in under 2 minutes for lightning-fast instant noodles, oatmeal, and hot snacks.",
            "social_proof": "👥 51 quick meal buyers bought this this week"
        },
        "secondary": {
            "title": "Pure Water Refreshing Wet Wipes (Pack of 15)",
            "mrp": 99, "price": 49, "emoji": "🧼", "sku": "001",
            "scenario_badge": "🧼 Instant Meal Cleanup",
            "why_suggested": "Clean hands instantly after eating hot fries or noodles.",
            "cobuying_utility": "Wipes away sauce and grease after instant snacks.",
            "social_proof": "👥 38 buyers added this this week"
        }
    },
    # 8. Sweet Tooth, Chocolates & Bakery
    {
        "categories": ["sweet tooth, chocolates & bakery"],
        "keywords": ["silk", "cadbury", "nutella", "ferrero", "ice cream", "kwality", "chocolate", "dessert"],
        "primary": {
            "title": "Pure Water Refreshing Wet Wipes (Pack of 15)",
            "mrp": 99, "price": 49, "emoji": "🧼", "sku": "001",
            "scenario_badge": "🧼 Sticky Dessert Cleanup",
            "why_suggested": "Wipe chocolate residue clean off hands or keep ice cream containers insulated.",
            "cobuying_utility": "Wipe chocolate residue clean off hands or keep ice cream containers insulated.",
            "social_proof": "👥 44 dessert lovers added this this week"
        },
        "secondary": {
            "title": "Insulated Neoprene Cold Can Cooler Sleeve",
            "mrp": 199, "price": 99, "emoji": "🍦", "sku": "002",
            "scenario_badge": "❄️ Thermal Ice Cream Insulation",
            "why_suggested": "Keep ice cream tubs and desserts cold while eating.",
            "cobuying_utility": "Insulates dessert tubs for longer enjoyment.",
            "social_proof": "👥 18 sweet lovers bought this"
        }
    },
    # 9. Beauty & Cosmetics
    {
        "categories": ["beauty & cosmetics"],
        "keywords": ["derma", "sunscreen", "minimalist", "serum", "garnier", "micellar", "maybelline", "mascara"],
        "primary": {
            "title": "Jade Facial Roller & Gua Sha Massager Set",
            "mrp": 999, "price": 499, "emoji": "💎", "sku": "101",
            "scenario_badge": "✨ Facial Sculpt & Glow Massage",
            "why_suggested": "Massage skin after applying serums or sunscreen to boost absorption, drainage, and natural glow.",
            "cobuying_utility": "Massage skin after applying serums or sunscreen to boost absorption, drainage, and natural glow.",
            "social_proof": "👥 28 skincare users in DLF Phase 3 bought this this week"
        }
    },
    # 10. Bath, Body & Personal Care
    {
        "categories": ["bath, body & personal care"],
        "keywords": ["cetaphil", "colgate", "dettol", "dove", "shampoo", "nivea", "lotion", "cleanser", "soap"],
        "primary": {
            "title": "Jade Facial Roller & Gua Sha Massager Set",
            "mrp": 999, "price": 499, "emoji": "💎", "sku": "101",
            "scenario_badge": "✨ Post-Cleansing Skin Massage",
            "why_suggested": "Enhance daily skincare absorption and facial relaxation right after cleansing and moisturizing.",
            "cobuying_utility": "Enhance daily skincare absorption and facial relaxation right after cleansing and moisturizing.",
            "social_proof": "👥 35 personal care buyers bought this this week"
        },
        "secondary": {
            "title": "Garnier Skin Naturals Micellar Cleansing Water 125ml",
            "mrp": 225, "price": 199, "emoji": "🧼", "sku": "103",
            "scenario_badge": "🧼 Gentle Pore Cleansing",
            "why_suggested": "Deep clean makeup and impurities after daily bathing routines.",
            "cobuying_utility": "Effortlessly dissolves makeup and dirt.",
            "social_proof": "👥 22 users bought this this week"
        }
    },
    # 11. Electronics & Tech Accessories
    {
        "categories": ["electronics & tech accessories"],
        "keywords": ["spigen", "charger", "boat", "airdopes", "portronics", "cable", "power bank", "mi"],
        "primary": {
            "title": "Portronics Multi-Angle Desktop Phone Stand",
            "mrp": 699, "price": 249, "emoji": "📱", "sku": "604",
            "scenario_badge": "📱 Hands-Free Workstation View",
            "why_suggested": "Enjoy an ergonomic hands-free viewing angle while fast-charging or listening to audio on your desk.",
            "cobuying_utility": "Enjoy an ergonomic hands-free viewing angle while fast-charging or listening to audio on your desk.",
            "social_proof": "👥 49 tech users in Gurgaon Sector 43 bought this this week"
        },
        "secondary": {
            "title": "Spigen 20W Fast Type-C Wall Charger Adapter",
            "mrp": 1499, "price": 899, "emoji": "🔌", "sku": "201",
            "scenario_badge": "⚡ 20W Fast Power Backup",
            "why_suggested": "Essential fast charging plug for your mobile gear.",
            "cobuying_utility": "Fast charge devices 50% in 25 mins.",
            "social_proof": "👥 34 tech buyers added this this week"
        }
    },
    # 12. Home & Kitchen Utilities
    {
        "categories": ["home & kitchen utilities"],
        "keywords": ["frother", "scale", "kettle", "phone stand", "borosil", "bowl", "utility"],
        "primary": {
            "title": "Portronics Multi-Angle Desktop Phone Stand",
            "mrp": 699, "price": 249, "emoji": "📱", "sku": "604",
            "scenario_badge": "📱 Recipe Video Phone Stand",
            "why_suggested": "Keep recipes and video guides clearly visible on your screen hands-free while cooking.",
            "cobuying_utility": "Keep recipes and video guides clearly visible on your screen hands-free while cooking.",
            "social_proof": "👥 39 home cooks bought this this week"
        }
    },
    # 13. Cleaning & Household Essentials
    {
        "categories": ["cleaning & household essentials"],
        "keywords": ["surf excel", "colin", "vim", "origami", "tissue", "cleaner", "washing"],
        "primary": {
            "title": "Origami 2-Ply Facial Tissue Box (200 Sheets)",
            "mrp": 110, "price": 95, "emoji": "🧻", "sku": "1301",
            "scenario_badge": "🧻 Quick Counter Spill Absorb",
            "why_suggested": "Quick-absorb tissues and wipes for accidental countertop spills and instant surface dusting.",
            "cobuying_utility": "Quick-absorb tissues and wipes for accidental countertop spills and instant surface dusting.",
            "social_proof": "👥 61 household buyers added this this week"
        },
        "secondary": {
            "title": "Pure Water Refreshing Wet Wipes (Pack of 15)",
            "mrp": 99, "price": 49, "emoji": "🧼", "sku": "001",
            "scenario_badge": "🧼 Multi-Surface Hand Wipe",
            "why_suggested": "Wipe hands clean after household chores.",
            "cobuying_utility": "Quick sanitizing hand wipe after cleaning.",
            "social_proof": "👥 40 users bought this"
        }
    },
    # 14. Baby Care
    {
        "categories": ["baby care"],
        "keywords": ["pampers", "wipes", "diapers", "sebamed", "lotion", "baby"],
        "primary": {
            "title": "Pampers Fresh Clean Baby Wipes (80 Sheets)",
            "mrp": 225, "price": 185, "emoji": "👶", "sku": "1401",
            "scenario_badge": "👶 Pure Water Rash Shield",
            "why_suggested": "Ultra-gentle 99% pure water wipes for rash-free, hypoallergenic cleanup during diaper changes.",
            "cobuying_utility": "Ultra-gentle 99% pure water wipes for rash-free, hypoallergenic cleanup during diaper changes.",
            "social_proof": "👥 38 young parents in DLF Phase 3 bought this this week"
        }
    },
    # 15. Pet Care
    {
        "categories": ["pet care"],
        "keywords": ["pedigree", "dog", "whiskas", "cat", "pet"],
        "primary": {
            "title": "Pure Water Refreshing Wet Wipes (Pack of 15)",
            "mrp": 99, "price": 49, "emoji": "🧼", "sku": "001",
            "scenario_badge": "🐾 Paw & Snout Meal Wipe",
            "why_suggested": "Quickly clean muddy paws, snouts, and feeding bowl spills instantly after mealtime.",
            "cobuying_utility": "Quickly clean muddy paws, snouts, and feeding bowl spills instantly after mealtime.",
            "social_proof": "👥 27 pet parents in your neighborhood bought this this week"
        }
    },
    # 16. Health, Pharma & Wellness
    {
        "categories": ["health, pharma & wellness"],
        "keywords": ["ors", "enerzal", "volini", "dettol", "bandages", "spray", "pain"],
        "primary": {
            "title": "Pure Water Refreshing Wet Wipes (Pack of 15)",
            "mrp": 99, "price": 49, "emoji": "🧼", "sku": "001",
            "scenario_badge": "🩹 Antiseptic Skin Prep Wipe",
            "why_suggested": "Hygienically clean skin before applying pain sprays or antiseptic adhesive bandages.",
            "cobuying_utility": "Hygienically clean skin before applying pain sprays or antiseptic adhesive bandages.",
            "social_proof": "👥 32 health buyers added this this week"
        }
    },
    # 17. Stationery, Books & Games
    {
        "categories": ["stationery, books & games"],
        "keywords": ["classmate", "notebook", "parker", "pen", "uno", "cards", "book"],
        "primary": {
            "title": "Portronics Multi-Angle Desktop Phone Stand",
            "mrp": 699, "price": 249, "emoji": "📱", "sku": "604",
            "scenario_badge": "📱 Ergonomic Desk Study Stand",
            "why_suggested": "Keep your study tools organized and devices fast-charged during late-night study or gaming sessions.",
            "cobuying_utility": "Keep your study tools organized and devices fast-charged during late-night study or gaming sessions.",
            "social_proof": "👥 29 students & gamers bought this this week"
        }
    },
    # 18. Paan & Party Essentials
    {
        "categories": ["paan & party essentials"],
        "keywords": ["orbit", "gum", "soda", "catch", "party"],
        "primary": {
            "title": "Insulated Neoprene Cold Can Cooler Sleeve",
            "mrp": 199, "price": 99, "emoji": "🥤", "sku": "002",
            "scenario_badge": "❄️ Party Chill Can Lock",
            "why_suggested": "Keep party mixers and sodas ice-cold 2x longer during gatherings.",
            "cobuying_utility": "Keep party mixers and sodas ice-cold 2x longer during gatherings.",
            "social_proof": "👥 21 party hosts added this this week"
        }
    },
    # 19. Meat, Fish & Eggs
    {
        "categories": ["meat, fish & eggs"],
        "keywords": ["chicken", "breast", "meat", "fish", "licious"],
        "primary": {
            "title": "Portronics Digital Kitchen Weight Scale (1g to 10kg)",
            "mrp": 999, "price": 399, "emoji": "⚖️", "sku": "602",
            "scenario_badge": "⚖️ Protein Macro Weighing",
            "why_suggested": "Accurately weigh protein meal portions and sanitize hands instantly after handling raw meat.",
            "cobuying_utility": "Accurately weigh protein meal portions and sanitize hands instantly after handling raw meat.",
            "social_proof": "👥 37 fitness enthusiasts bought this this week"
        },
        "secondary": {
            "title": "Pure Water Refreshing Wet Wipes (Pack of 15)",
            "mrp": 99, "price": 49, "emoji": "🧼", "sku": "001",
            "scenario_badge": "🧼 Raw Meat Hand Sanitizer",
            "why_suggested": "Sanitize hands after handling raw poultry.",
            "cobuying_utility": "Quick hygienic cleanup for hands.",
            "social_proof": "👥 45 buyers added this"
        }
    }
]

# -----------------------------------------------------------------------------
# SESSION STATE INITIALIZATION
# -----------------------------------------------------------------------------
if "cart" not in st.session_state:
    st.session_state.cart = []

if "nudge_added" not in st.session_state:
    st.session_state.nudge_added = False

if "order_placed" not in st.session_state:
    st.session_state.order_placed = False

if "exchange_triggered" not in st.session_state:
    st.session_state.exchange_triggered = False

def create_nudge_payload(anchor_name, prod_dict):
    return {
        "should_nudge": True,
        "anchor_item": anchor_name or "Basket Item",
        "nudge_badge": "✨ BLINKSMART CONTEXTUAL NUDGE",
        "category_pill": prod_dict["scenario_badge"],
        "why_suggested": prod_dict["why_suggested"],
        "cobuying_utility": prod_dict["cobuying_utility"],
        "product": {
            "title": prod_dict["title"],
            "mrp": prod_dict["mrp"],
            "offer_price": prod_dict["price"],
            "authenticity_badge": "🔰 100% Brand Authenticity Seal",
            "shield_badge": "🔰 1st Trial Shield Active"
        },
        "social_proof": prod_dict["social_proof"],
        "emoji": prod_dict["emoji"]
    }

def get_blinksmart_recommendation(cart_items):
    # 1. SILENT COLLAPSE: Return false if cart is empty
    if not cart_items:
        return {"should_nudge": False}

    cart_subtotal = sum(item.get("price", 0) for item in cart_items)

    # 2. PRICE RATIO & BASKET PROTECTION: Max price is 3x cart value
    max_allowed_price = cart_subtotal * 3

    # RULE 1: LATEST ITEM PRIORITY (Evaluate cart_items[-1] first)
    last_item = cart_items[-1]
    anchor_name = last_item.get("name", "Basket Item")
    item_name_lower = anchor_name.lower()
    item_cat_lower = last_item.get("category", "").lower()
    full_text = f"{item_name_lower} {item_cat_lower}"

    # Search for matching category route in ROUTING_MATRIX
    for route in ROUTING_MATRIX:
        cat_match = any(c in item_cat_lower for c in route["categories"])
        kw_match = any(kw in full_text for kw in route["keywords"])

        if cat_match or kw_match:
            # Try primary recommendation first
            prim = route["primary"]
            if cart_subtotal < 100 and prim["price"] > 150:
                # Check low-cost secondary if present
                if "secondary" in route and route["secondary"]["price"] <= max_allowed_price:
                    return create_nudge_payload(anchor_name, route["secondary"])
                elif ROUTING_MATRIX[3]["primary"]["price"] <= max_allowed_price: # ₹49 Wipes
                    return create_nudge_payload(anchor_name, ROUTING_MATRIX[3]["primary"])
            elif prim["price"] <= max_allowed_price:
                return create_nudge_payload(anchor_name, prim)
            elif "secondary" in route and route["secondary"]["price"] <= max_allowed_price:
                return create_nudge_payload(anchor_name, route["secondary"])

    # Fallback to low-cost utility (SKU 001 Wipes @ ₹49) if price ratio allows
    wipes = ROUTING_MATRIX[3]["primary"]
    if wipes["price"] <= max_allowed_price:
        return create_nudge_payload(anchor_name, wipes)

    # 3. SILENT COLLAPSE: If no candidate satisfies the price ratio constraint
    return {"should_nudge": False}

# -----------------------------------------------------------------------------
# TOP APP HEADER (LOGO, LOCATION & RESET)
# -----------------------------------------------------------------------------
col_logo, col_info, col_reset = st.columns([1, 2, 1])
with col_logo:
    st.markdown(clean_html("""
    <div style='display:flex; align-items:center; justify-content:flex-start;'>
        <span class="blinkit-logo-badge">blinkit</span>
    </div>
    """), unsafe_allow_html=True)

with col_info:
    st.markdown(clean_html("""
    <div style='text-align:center; display:flex; flex-direction:column; align-items:center; justify-content:center;'>
        <div style='font-size:12px; font-weight:800; color:var(--text-primary); margin-bottom:3px;'>📍 DLF Phase 3, Gurgaon</div>
        <div class='delivery-pill'>⚡ 10 MINS Delivery</div>
    </div>
    """), unsafe_allow_html=True)

with col_reset:
    if st.button("🔄 Reset", key="top_reset_btn"):
        st.session_state.cart = []
        st.session_state.nudge_added = False
        st.session_state.order_placed = False
        st.session_state.exchange_triggered = False
        st.rerun()

# -----------------------------------------------------------------------------
# SCREEN 1: ORDER PLACED & 10-MIN EXCHANGE SIMULATOR
# -----------------------------------------------------------------------------
if st.session_state.order_placed:
    st.balloons()
    st.success("🎉 Order Placed Successfully in 8 Minutes!")
    st.caption("Fulfillment Dark Store: Gurgaon Sector 43 Hub | Rider Assigned: Ramesh Kumar")
    st.divider()

    order_success_html = clean_html("""
<div style='background-color:var(--pill-bg); border: 1.5px solid var(--pill-border); border-radius:12px; padding:16px; margin-bottom:16px;'>
<div style='display:flex; justify-content:space-between; align-items:center;'>
<span style='color:var(--pill-text); font-weight:800; font-size:14px;'>🔰 First-Trial Safety Net Active</span>
<span style='background-color:#f7c200; color:#000000; font-family:monospace; font-weight:bold; padding:2px 8px; border-radius:4px;'>09:59 MINS</span>
</div>
<p style='font-size:12px; color:var(--text-primary); margin-top:8px;'>
Your trial item is covered under the 10-Minute Doorstep Exchange Guarantee. Inspect the unit upon arrival!
</p>
</div>
""")
    st.markdown(order_success_html, unsafe_allow_html=True)

    if not st.session_state.exchange_triggered:
        if st.button("🧪 Test 10-Minute Doorstep Rider Exchange Request"):
            st.session_state.exchange_triggered = True
            st.rerun()
    else:
        st.warning("⚡ Doorstep Exchange Dispatched!")
        exchange_log_html = clean_html("""
<div style='background-color:var(--card-bg); border:1px solid var(--border-color); border-radius:10px; padding:12px; font-size:12px; box-shadow:0 1px 3px rgba(0,0,0,0.05);'>
<div style='font-weight:bold; color:var(--text-primary); margin-bottom:4px;'>🛵 Live Exchange Status Log:</div>
<div style='color:#0c831f;'>• Exchange request logged via automated chatbot.</div>
<div style='color:var(--text-secondary);'>• Rider Ramesh Kumar dispatched with fresh sealed unit from dark store.</div>
<div style='color:var(--text-secondary);'>• Estimated Doorstep Swap Time: <strong>7 Minutes</strong>.</div>
</div>
""")
        st.markdown(exchange_log_html, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# SCREEN 2: CART-FIRST RE-ORDERED INFORMATION ARCHITECTURE
# -----------------------------------------------------------------------------
else:
    # -------------------------------------------------------------------------
    # 1. SEARCH & CATEGORY PRODUCT BROWSING
    # -------------------------------------------------------------------------
    st.markdown("""<div style='font-weight:800; font-size:15px; color:var(--text-primary);'>🔍 Search & Browse Grocery Items</div>""", unsafe_allow_html=True)

    search_query = st.text_input(
        "Search Catalog",
        placeholder="🔍 Type 'milk, 20W charger, doritos, sunscreen...'",
        label_visibility="collapsed"
    )

    category_mapping = {
        "All Categories 🛒": "All Categories",
        "Dairy, Bread & Eggs 🥛": "Dairy, Bread & Eggs",
        "Fruits & Vegetables 🥑": "Fruits & Vegetables",
        "Grocery & Staples 🌾": "Grocery & Staples",
        "Munchies & Snacks 🧀": "Munchies & Snacks",
        "Beverages & Cold Drinks 🥤": "Beverages & Cold Drinks",
        "Tea, Coffee & Health Drinks ☕": "Tea, Coffee & Health Drinks",
        "Instant & Frozen Food 🍜": "Instant & Frozen Food",
        "Sweet Tooth, Chocolates & Bakery 🍫": "Sweet Tooth, Chocolates & Bakery",
        "Beauty & Cosmetics 🧴": "Beauty & Cosmetics",
        "Bath, Body & Personal Care 🧼": "Bath, Body & Personal Care",
        "Electronics & Tech Accessories ⚡": "Electronics & Tech Accessories",
        "Home & Kitchen Utilities ⚖️": "Home & Kitchen Utilities",
        "Cleaning & Household Essentials 🧺": "Cleaning & Household Essentials",
        "Baby Care 👶": "Baby Care",
        "Pet Care 🐶": "Pet Care",
        "Health, Pharma & Wellness 💊": "Health, Pharma & Wellness",
        "Stationery, Books & Games 📓": "Stationery, Books & Games",
        "Paan & Party Essentials 🍬": "Paan & Party Essentials",
        "Meat, Fish & Eggs 🍗": "Meat, Fish & Eggs"
    }

    selected_pill = st.selectbox("Category:", list(category_mapping.keys()), label_visibility="collapsed")
    target_category = category_mapping[selected_pill]

    # Filter catalog dataset by category & search query
    filtered_df = CATALOG_DF
    if target_category != "All Categories":
        filtered_df = filtered_df[filtered_df["category"] == target_category]

    if search_query and search_query.strip() not in ["", "-"]:
        filtered_df = filtered_df[filtered_df["name"].str.contains(search_query, case=False, na=False)]

    product_map = {f"{row.get('emoji', '🛒')} {row['name']} — ₹{row['price']}": row for _, row in filtered_df.iterrows()}

    if product_map:
        placeholder = "-- Choose a Product from Catalog --"
        options = [placeholder] + list(product_map.keys())
        selected_item_key = st.selectbox("Select Product to Add:", options)
        if st.button("+ Add Item to Grocery Basket", use_container_width=True, key="add_catalog_item_btn"):
            if selected_item_key == placeholder:
                st.warning("⚠️ Please select a product from the list above first.")
            else:
                item_to_add = product_map[selected_item_key]
                st.session_state.cart.append(item_to_add)
                st.rerun()
    else:
        if search_query and search_query.strip() not in ["", "-"]:
            st.info("🔍 No products match your search query. Try searching for milk, sunscreen, chips, or oats.")
        else:
            st.info("📦 No products found in this category.")

    st.markdown("---")

    # -------------------------------------------------------------------------
    # 2. ACTIVE GROCERY BASKET (RENDERS FIRST BELOW CATALOG)
    # -------------------------------------------------------------------------
    st.markdown("""<div style='font-weight:800; font-size:15px; color:var(--text-primary);'>🧺 Active Grocery Basket</div>""", unsafe_allow_html=True)
    
    if not st.session_state.cart:
        st.info("🛒 Your basket is empty. Select an item above to add!")
    else:
        subtotal = 0
        for idx, item in enumerate(st.session_state.cart):
            subtotal += item["price"]
            col_item, col_del = st.columns([4.5, 0.8])
            with col_item:
                cart_item_html = clean_html(f"""
                <div style='display:flex; justify-content:space-between; align-items:center; background-color:var(--card-bg); border:1px solid var(--border-color); border-radius:10px; padding:8px 12px; margin-bottom:6px;'>
                    <div>
                        <span style='font-size:16px;'>{item.get('emoji', '🛒')}</span>
                        <strong style='font-size:13px; color:var(--text-primary); margin-left:6px;'>{item['name']}</strong>
                    </div>
                    <span style='font-weight:bold; font-size:13px; color:var(--text-primary);'>₹{item['price']}</span>
                </div>
                """)
                st.markdown(cart_item_html, unsafe_allow_html=True)
            with col_del:
                if st.button("❌", key=f"del_cart_{idx}"):
                    st.session_state.cart.pop(idx)
                    st.rerun()

    st.markdown("---")

    # -------------------------------------------------------------------------
    # 3. BLINKSMART CONTEXTUAL NUDGE CARD (DYNAMIC RECENT-ITEM ROUTING)
    # -------------------------------------------------------------------------
    rec = get_blinksmart_recommendation(st.session_state.cart)

    if rec.get("should_nudge", False):
        prod = rec["product"]

        nudge_card_html = clean_html(f"""
<div class="nudge-card">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
        <span class="nudge-tag">{rec['nudge_badge']}</span>
        <span class="scenario-badge">{rec['category_pill']}</span>
    </div>
    <div class="rationale-box">
        <div style="font-size:11px; color:#0C831F; font-weight:800; margin-bottom:2px;">🎯 WHY SUGGESTED:</div>
        <div style="font-size:12px; color:var(--text-primary); margin-bottom:4px;">{rec['why_suggested']}</div>
        <div style="font-size:11px; color:#D97706; font-weight:800; margin-bottom:2px;">🤝 CO-BUYING UTILITY:</div>
        <div style="font-size:12px; color:var(--text-secondary); line-height:1.4;">"{rec['cobuying_utility']}"</div>
    </div>
    <div style="background-color:var(--card-bg); border:1px solid var(--border-color); border-radius:12px; padding:10px; display:flex; justify-content:space-between; align-items:center;">
        <div>
            <div style="font-size:15px; font-weight:700; color:var(--text-primary);">{rec.get('emoji', '✨')} {prod['title']}</div>
            <div style="font-size:11px; color:#0C831F; font-weight:600;">{prod['authenticity_badge']}</div>
            <div style="margin-top:4px;">
                <span style="font-size:14px; font-weight:800; color:#0C831F;">₹{prod['offer_price']}</span>
                <span style="font-size:11px; color:#9CA3AF; text-decoration:line-through; margin-left:4px;">₹{prod['mrp']}</span>
            </div>
        </div>
    </div>
    <div style="margin-top:8px; font-size:11px; color:var(--text-secondary); display:flex; justify-content:space-between; align-items:center;">
        <span>{rec['social_proof']}</span>
        <span class="shield-badge">{prod['shield_badge']}</span>
    </div>
</div>
""")
        st.markdown(nudge_card_html, unsafe_allow_html=True)

        # Differentiated Secondary CTA button styling (Blinkit Gold #F7C200)
        if not st.session_state.nudge_added:
            st.markdown('<div class="nudge-btn-wrapper">', unsafe_allow_html=True)
            if st.button(f"+ Add {prod['title']} to Order (₹15 Fee Waived)", key="add_nudge_btn"):
                st.session_state.nudge_added = True
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.success(f"✓ {prod['title']} Added to Basket with First-Trial Shield!")

        st.markdown("---")

    # -------------------------------------------------------------------------
    # 4. BILL SUMMARY & PRIMARY CHECKOUT CTA (RENDERS THIRD)
    # -------------------------------------------------------------------------
    if st.session_state.cart:
        if st.session_state.nudge_added and rec.get("should_nudge", False):
            subtotal += prod['offer_price']

        st.markdown("""<div style='font-weight:800; font-size:14px; color:var(--text-primary); margin-top:10px;'>📄 Bill Summary</div>""", unsafe_allow_html=True)
        handling_fee = 0 if st.session_state.nudge_added else 15
        grand_total = subtotal + handling_fee

        col_label, col_val = st.columns([3, 1])
        with col_label:
            st.write("Item Subtotal")
            st.write("Delivery Fee (⚡ 10 Mins)")
            st.write("Handling Fee")
            if st.session_state.nudge_added:
                st.write("First-Trial Shield Fee Waiver")
            st.markdown("**Grand Total**")
        with col_val:
            st.write(f"₹{subtotal}")
            st.write("FREE")
            st.write(f"₹{handling_fee}")
            if st.session_state.nudge_added:
                st.write("-₹15")
            st.markdown(f"**₹{grand_total}**")

        st.divider()

        # Dominant Primary CTA (Solid Blinkit Dark Green #0C831F)
        if st.button(f"Pay ₹{grand_total} via Face ID / UPI (<15s) ➔", key="checkout_btn"):
            st.session_state.order_placed = True
            st.rerun()

# -----------------------------------------------------------------------------
# iOS BOTTOM TAB BAR & HOME INDICATOR
# -----------------------------------------------------------------------------
ios_tab_html = clean_html("""
<div class="ios-tab-bar">
    <div class="ios-tab-item active">
        <span style="font-size:18px;">🏠</span>
        <span>Home</span>
    </div>
    <div class="ios-tab-item">
        <span style="font-size:18px;">🏷️</span>
        <span>Categories</span>
    </div>
    <div class="ios-tab-item">
        <span style="font-size:18px;">⚡</span>
        <span>BlinkSmart</span>
    </div>
    <div class="ios-tab-item">
        <span style="font-size:18px;">🧺</span>
        <span>Basket</span>
    </div>
    <div class="ios-tab-item">
        <span style="font-size:18px;">👤</span>
        <span>Account</span>
    </div>
</div>
<div class="ios-home-indicator"></div>
""")
st.markdown(ios_tab_html, unsafe_allow_html=True)
