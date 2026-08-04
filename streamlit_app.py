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
    margin-top: 8px;
    margin-bottom: 8px;
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

.social-proof-pill {
    background-color: #ECFDF5;
    border: 1px solid #A7F3D0;
    color: #047857;
    font-weight: 700;
    font-size: 11px;
    padding: 3px 8px;
    border-radius: 6px;
    display: inline-block;
    margin-top: 6px;
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
# BLINKSMART AI ENGINE (MULTI-PRODUCT RECOMMENDATION ARRAY & DEDUPLICATION)
# -----------------------------------------------------------------------------
ROUTING_MATRIX = [
    # 1. Fruits & Vegetables
    {
        "categories": ["fruits & vegetables"],
        "keywords": ["avocado", "tomatoes", "onions", "potatoes", "bananas", "apples", "coriander", "lemons", "fresh"],
        "primary": {
            "title": "Portronics Digital Kitchen Weight Scale (1g to 10kg)",
            "mrp": 999, "price": 399, "emoji": "⚖️", "sku": "602",
            "scenario_badge": "⚖️ Produce & Macro Precision",
            "why_suggested": "Accurately weigh fruit portions, avocado macros, and salad ingredients.",
            "cobuying_utility": "Accurately weigh fruit portions, avocado macros, and salad ingredients.",
            "social_proof": "👥 142 residents in DLF Phase 3 bought this item this week"
        }
    },
    # 2. Munchies, Chips & Sweet Tooth
    {
        "categories": ["munchies & snacks", "sweet tooth, chocolates & bakery"],
        "keywords": ["doritos", "chips", "lays", "bhujia", "popcorn", "kurkure", "pringles", "nachos", "snack", "silk", "cadbury", "nutella", "ferrero", "chocolate", "dessert"],
        "primary": {
            "title": "Pure Water Refreshing Wet Wipes (Pack of 15)",
            "mrp": 99, "price": 49, "emoji": "🧼", "sku": "001",
            "scenario_badge": "🧼 Instant Finger Cleanup",
            "why_suggested": "Instantly wipes away masala grease, chocolate residue, and seasoning from fingers.",
            "cobuying_utility": "Instantly wipes away masala grease, chocolate residue, and seasoning from fingers without drying skin.",
            "social_proof": "👥 389 residents in DLF Phase 3 bought this item this week"
        }
    },
    # 3. Coffee & Tea
    {
        "categories": ["tea, coffee & health drinks"],
        "keywords": ["coffee", "tokai", "nescafe", "tea", "tetley", "green tea", "bournvita", "chai", "espresso"],
        "primary": {
            "title": "Electric Stainless Steel Milk Frother & Foamer",
            "mrp": 799, "price": 399, "emoji": "⚡", "sku": "301",
            "scenario_badge": "☕ 15-Sec Cafe Micro-Foam",
            "why_suggested": "Create rich, cafe-style micro-foam for lattes and teas right at home.",
            "cobuying_utility": "Create rich, cafe-style micro-foam for lattes and teas right at home.",
            "social_proof": "👥 215 coffee lovers in DLF Phase 3 bought this item this week"
        }
    },
    # 4. Beauty & Skincare
    {
        "categories": ["beauty & cosmetics", "bath, body & personal care"],
        "keywords": ["derma", "sunscreen", "minimalist", "serum", "garnier", "micellar", "maybelline", "mascara", "skincare"],
        "primary": {
            "title": "Jade Facial Roller & Gua Sha Massager Set",
            "mrp": 999, "price": 499, "emoji": "💎", "sku": "101",
            "scenario_badge": "✨ Facial Sculpt & Glow Massage",
            "why_suggested": "Massage skin after applying serums or sunscreen to boost absorption.",
            "cobuying_utility": "Massage skin after applying serums or sunscreen to boost absorption.",
            "social_proof": "👥 178 skincare buyers in DLF Phase 3 bought this item this week"
        }
    },
    # 5. Tech & Office Supplies
    {
        "categories": ["electronics & tech accessories", "stationery, books & games"],
        "keywords": ["red bull", "charger", "spigen", "cable", "power bank", "notebook", "office", "desk", "laptop"],
        "primary": {
            "title": "Spigen 20W Fast Type-C Wall Charger Adapter",
            "mrp": 1499, "price": 899, "emoji": "🔌", "sku": "201",
            "scenario_badge": "⚡ 20W Fast Workstation Power",
            "why_suggested": "Fast charge your workstation devices up to 50% in 25 minutes.",
            "cobuying_utility": "Fast charge your workstation devices up to 50% in 25 minutes.",
            "social_proof": "👥 264 tech users in DLF Phase 3 bought this item this week"
        }
    },
    # 6. Beverages & Cold Drinks
    {
        "categories": ["beverages & cold drinks"],
        "keywords": ["coke", "coca-cola", "thums up", "juice", "water", "bisleri", "soda", "drink"],
        "primary": {
            "title": "Insulated Neoprene Cold Can Cooler Sleeve",
            "mrp": 199, "price": 99, "emoji": "🥤", "sku": "002",
            "scenario_badge": "❄️ Sub-Zero Can Thermal Chill",
            "why_suggested": "Keeps chilled cans, juices, and drinks cold 2x longer.",
            "cobuying_utility": "Keeps chilled cans, juices, and drinks cold 2x longer.",
            "social_proof": "👥 195 drink buyers in DLF Phase 3 bought this item this week"
        }
    },
    # 7. Dairy, Bread & Eggs
    {
        "categories": ["dairy, bread & eggs"],
        "keywords": ["milk", "butter", "bread", "egg", "yogurt", "paneer", "amul", "eggoz", "harvest", "epigamia", "mother dairy"],
        "primary": {
            "title": "Electric Stainless Steel Milk Frother & Foamer",
            "mrp": 799, "price": 399, "emoji": "⚡", "sku": "301",
            "scenario_badge": "☕ 15-Sec Micro-Foam & Whisk",
            "why_suggested": "Whisk egg batters, Greek yogurt smoothies, or hot milk coffee.",
            "cobuying_utility": "Whisk egg batters, Greek yogurt smoothies, or hot milk coffee in 15 seconds.",
            "social_proof": "👥 312 breakfast buyers in DLF Phase 3 bought this item this week"
        }
    }
]

# -----------------------------------------------------------------------------
# SESSION STATE INITIALIZATION
# -----------------------------------------------------------------------------
if "cart" not in st.session_state:
    st.session_state.cart = []

if "order_placed" not in st.session_state:
    st.session_state.order_placed = False

if "exchange_triggered" not in st.session_state:
    st.session_state.exchange_triggered = False

def create_nudge_item_payload(anchor_name, prod_dict):
    return {
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
        return {"should_nudge": False, "recommendations": []}

    cart_subtotal = sum(item.get("price", 0) for item in cart_items)
    max_allowed_price = cart_subtotal * 3

    recommendations = []
    used_skus = set()

    # Iterate through unique items/categories in cart (reversed for latest item first)
    for item in reversed(cart_items):
        if len(recommendations) >= 3:
            break

        anchor_name = item.get("name", "Basket Item")
        item_name_lower = anchor_name.lower()
        item_cat_lower = item.get("category", "").lower()
        full_text = f"{item_name_lower} {item_cat_lower}"

        matched_prod = None

        for route in ROUTING_MATRIX:
            cat_match = any(c in item_cat_lower for c in route["categories"])
            kw_match = any(kw in full_text for kw in route["keywords"])

            if cat_match or kw_match:
                prim = route["primary"]
                if prim["sku"] not in used_skus and prim["price"] <= max_allowed_price:
                    matched_prod = prim
                    break

        # Fallback to Wipes (SKU 001) if not already used & within price ratio
        if not matched_prod:
            wipes = ROUTING_MATRIX[1]["primary"] # SKU 001 Wipes @ ₹49
            if wipes["sku"] not in used_skus and wipes["price"] <= max_allowed_price:
                matched_prod = wipes

        if matched_prod:
            used_skus.add(matched_prod["sku"])
            recommendations.append(create_nudge_item_payload(anchor_name, matched_prod))

    if recommendations:
        return {
            "should_nudge": True,
            "recommendations": recommendations
        }

    return {"should_nudge": False, "recommendations": []}

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
    # 3. SINGLE CONSOLIDATED BLINKSMART CONTEXTUAL NUDGE CARD
    # -------------------------------------------------------------------------
    rec = get_blinksmart_recommendation(st.session_state.cart)
    nudge_trial_added = False

    if rec.get("should_nudge", False):
        recommendations = rec.get("recommendations", [])
        
        # Build inner HTML for each recommendation inside the SINGLE consolidated box
        inner_items_html = ""
        for idx, nudge in enumerate(recommendations):
            prod = nudge["product"]
            num_emoji = "1️⃣" if idx == 0 else ("2️⃣" if idx == 1 else "3️⃣")
            
            inner_items_html += clean_html(f"""
            <div class="rationale-box">
                <div style="font-size:11px; font-weight:800; color:#0C831F; margin-bottom:4px;">
                    {num_emoji} FOR: {nudge['anchor_item'].upper()}
                </div>
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                    <div style="font-size:14px; font-weight:700; color:var(--text-primary);">
                        {nudge.get('emoji', '✨')} {prod['title']}
                    </div>
                    <div>
                        <span style="font-size:14px; font-weight:800; color:#0C831F;">₹{prod['offer_price']}</span>
                        <span style="font-size:11px; color:#9CA3AF; text-decoration:line-through; margin-left:4px;">₹{prod['mrp']}</span>
                    </div>
                </div>
                <div style="font-size:12px; color:var(--text-primary); margin-bottom:2px;">🎯 {nudge['why_suggested']}</div>
                <div style="font-size:11px; color:var(--text-secondary); line-height:1.3; margin-bottom:4px;">🤝 "{nudge['cobuying_utility']}"</div>
                <div class="social-proof-pill">{nudge['social_proof']}</div>
            </div>
            """)

        single_box_html = clean_html(f"""
        <div class="nudge-card">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                <span class="nudge-tag">✨ BLINKSMART CONTEXTUAL NUDGES ({len(recommendations)})</span>
                <span class="shield-badge">🔰 1st Trial Shield Active</span>
            </div>
            {inner_items_html}
            <div style="margin-top:10px; font-size:11px; color:var(--text-secondary); display:flex; justify-content:space-between; align-items:center;">
                <span>🔰 100% Brand Authenticity Guarantee</span>
                <span>⚡ 10-Minute Doorstep Rider Exchange</span>
            </div>
        </div>
        """)
        st.markdown(single_box_html, unsafe_allow_html=True)

        # Render Add-on CTA Buttons for each recommendation right below the single consolidated box
        for r_idx, nudge in enumerate(recommendations):
            prod = nudge["product"]
            btn_key = f"add_nudge_btn_{r_idx}_{prod['title'][:8]}"
            nudge_flag_key = f"nudge_added_{r_idx}_{prod['title'][:8]}"
            
            if nudge_flag_key not in st.session_state:
                st.session_state[nudge_flag_key] = False

            if not st.session_state[nudge_flag_key]:
                st.markdown('<div class="nudge-btn-wrapper">', unsafe_allow_html=True)
                if st.button(f"+ Add #{r_idx+1} {prod['title']} to Order (₹15 Fee Waived)", key=btn_key):
                    st.session_state[nudge_flag_key] = True
                    st.session_state.cart.append({
                        "id": f"trial_{r_idx}",
                        "name": prod["title"],
                        "price": prod["offer_price"],
                        "mrp": prod["mrp"],
                        "category": "Trial Product",
                        "emoji": nudge.get("emoji", "✨")
                    })
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                nudge_trial_added = True
                st.success(f"✓ #{r_idx+1} {prod['title']} Added to Basket with First-Trial Shield!")

        st.markdown("---")

    # -------------------------------------------------------------------------
    # 4. BILL SUMMARY & PRIMARY CHECKOUT CTA (RENDERS THIRD)
    # -------------------------------------------------------------------------
    if st.session_state.cart:
        st.markdown("""<div style='font-weight:800; font-size:14px; color:var(--text-primary); margin-top:10px;'>📄 Bill Summary</div>""", unsafe_allow_html=True)
        handling_fee = 0 if nudge_trial_added else 15
        grand_total = subtotal + handling_fee

        col_label, col_val = st.columns([3, 1])
        with col_label:
            st.write("Item Subtotal")
            st.write("Delivery Fee (⚡ 10 Mins)")
            st.write("Handling Fee")
            if nudge_trial_added:
                st.write("First-Trial Shield Fee Waiver")
            st.markdown("**Grand Total**")
        with col_val:
            st.write(f"₹{subtotal}")
            st.write("FREE")
            st.write(f"₹{handling_fee}")
            if nudge_trial_added:
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
