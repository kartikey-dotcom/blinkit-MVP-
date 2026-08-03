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
# BLINKSMART AI ENGINE (DYNAMIC MULTI-CATEGORY ROUTING & STRICT NO-DEFAULT)
# -----------------------------------------------------------------------------
BLINKSMART_CATALOG = {
    "COFFEE_TEA": [
        {
            "sku": "301",
            "triggers": ["coffee", "beans", "espresso", "davidoff", "nescafe", "tea", "green tea", "chai"],
            "scenario_badge": "☕ 15-Second Cafe Micro-Foam",
            "why_suggested": "Pairs with your gourmet coffee & dairy selection.",
            "cobuying_utility": "Create cafe-grade velvety micro-foam in 15 seconds directly inside your morning coffee cup.",
            "title": "Electric Stainless Steel Milk Frother & Foamer",
            "mrp": 799,
            "price": 399,
            "emoji": "⚡",
            "social_proof": "👥 63 coffee lovers in DLF Phase 3 bought this this week"
        },
        {
            "sku": "302",
            "triggers": ["coffee", "beans", "espresso", "tea"],
            "scenario_badge": "❄️ Hot/Cold Thermal Lock",
            "why_suggested": "Keep your freshly brewed coffee hot on the go.",
            "cobuying_utility": "Double-wall vacuum insulation keeps hot brews warm for 6 hours.",
            "title": "Stainless Steel Insulated Travel Tumbler (500ml)",
            "mrp": 1199,
            "price": 699,
            "emoji": "🥤",
            "social_proof": "👥 22 beverage buyers nearby bought this this week"
        }
    ],
    "SNACKS": [
        {
            "sku": "001",
            "triggers": ["chips", "lays", "doritos", "kurkure", "namkeen", "biscuits", "nachos", "munchies", "snack"],
            "scenario_badge": "🧼 Instant Finger Cleanup",
            "why_suggested": "Essential cleanup utility for snack time.",
            "cobuying_utility": "Instantly wipes away grease and seasoning from fingers without drying your skin.",
            "title": "Pure Water Refreshing Wet Wipes (Pack of 15)",
            "mrp": 99,
            "price": 49,
            "emoji": "🧼",
            "social_proof": "👥 48 snack buyers in your neighborhood added this this week"
        }
    ],
    "BEAUTY": [
        {
            "sku": "101",
            "triggers": ["sunscreen", "serum", "facewash", "face wash", "moisturizer", "derma", "plum", "toner", "skincare"],
            "scenario_badge": "✨ Facial Sculpt & Glow Massage",
            "why_suggested": "Complements your skincare & serum routine.",
            "cobuying_utility": "Massage skin after applying sunscreen or serums to enhance product absorption.",
            "title": "Jade Facial Roller & Gua Sha Massager Set",
            "mrp": 999,
            "price": 499,
            "emoji": "💎",
            "social_proof": "👥 28 skincare users in DLF Phase 3 bought this this week"
        }
    ],
    "TECH": [
        {
            "sku": "201",
            "triggers": ["notebook", "charger", "cable", "energy drink", "red bull", "pen", "sticky notes", "office", "desk", "laptop"],
            "min_cart_value": 300,
            "scenario_badge": "⚡ High-Speed Power Backup",
            "why_suggested": "Emergency power backup for your active workstation.",
            "cobuying_utility": "Fast charge your smartphone up to 50% in 25 minutes during work sessions.",
            "title": "Type-C 20W PD Fast Charging Adapter",
            "mrp": 1299,
            "price": 699,
            "emoji": "🔌",
            "social_proof": "👥 34 tech users in DLF Phase 3 bought this this week"
        }
    ],
    "STAPLES_DAIRY": [
        {
            "sku": "301",
            "triggers": ["milk", "paneer", "dairy"],
            "scenario_badge": "☕ 15-Second Cafe Micro-Foam",
            "why_suggested": "Pairs with your fresh dairy & milk selection.",
            "cobuying_utility": "Create cafe-grade velvety micro-foam in 15 seconds directly inside your morning milk or coffee.",
            "title": "Electric Stainless Steel Milk Frother & Foamer",
            "mrp": 799,
            "price": 399,
            "emoji": "⚡",
            "social_proof": "👥 63 dairy buyers in DLF Phase 3 bought this this week"
        }
    ]
}

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

def create_nudge_payload(anchor_name, candidate):
    return {
        "should_nudge": True,
        "anchor_item": anchor_name or "Basket Item",
        "nudge_badge": "✨ BLINKSMART CONTEXTUAL NUDGE",
        "category_pill": candidate["scenario_badge"],
        "why_suggested": candidate["why_suggested"],
        "cobuying_utility": candidate["cobuying_utility"],
        "product": {
            "title": candidate["title"],
            "mrp": candidate["mrp"],
            "offer_price": candidate["price"],
            "authenticity_badge": "🔰 100% Brand Authenticity Seal",
            "shield_badge": "🔰 1st Trial Shield Active"
        },
        "social_proof": candidate["social_proof"],
        "emoji": candidate["emoji"]
    }

def get_blinksmart_recommendation(cart_items):
    # 1. SILENT COLLAPSE: Return false if cart is empty
    if not cart_items:
        return {"should_nudge": False}

    cart_subtotal = sum(item.get("price", 0) for item in cart_items)
    max_allowed_price = cart_subtotal * 3

    # Dynamic Keyword Routing across cart items
    for item in cart_items:
        item_name = item.get("name", "").lower()
        item_cat = item.get("category", "").lower()
        full_text = f"{item_name} {item_cat}"

        # Route 1: COFFEE / TEA / BEVERAGE ROUTE
        for candidate in BLINKSMART_CATALOG["COFFEE_TEA"]:
            if any(t in full_text for t in candidate["triggers"]):
                if candidate["price"] <= max_allowed_price:
                    return create_nudge_payload(item.get("name"), candidate)

        # Route 2: SNACKS / CHIPS / PACKAGED FOOD ROUTE
        for candidate in BLINKSMART_CATALOG["SNACKS"]:
            if any(t in full_text for t in candidate["triggers"]):
                if candidate["price"] <= max_allowed_price:
                    return create_nudge_payload(item.get("name"), candidate)

        # Route 3: BEAUTY & SKINCARE ROUTE
        for candidate in BLINKSMART_CATALOG["BEAUTY"]:
            if any(t in full_text for t in candidate["triggers"]):
                if candidate["price"] <= max_allowed_price:
                    return create_nudge_payload(item.get("name"), candidate)

        # Route 4: TECH & OFFICE SUPPLIES ROUTE (Cart > 300)
        for candidate in BLINKSMART_CATALOG["TECH"]:
            if any(t in full_text for t in candidate["triggers"]):
                if cart_subtotal >= candidate.get("min_cart_value", 300) and candidate["price"] <= max_allowed_price:
                    return create_nudge_payload(item.get("name"), candidate)

        # Route 5: STAPLES / DAIRY / HOUSEHOLD ROUTE
        for candidate in BLINKSMART_CATALOG["STAPLES_DAIRY"]:
            if any(t in full_text for t in candidate["triggers"]):
                if candidate["price"] <= max_allowed_price:
                    return create_nudge_payload(item.get("name"), candidate)

    # 2. STRICT SILENT COLLAPSE: No default recommendation!
    # SKU 001 (Wet Wipes) is NEVER defaulted for non-snack items.
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
    # 3. BLINKSMART CONTEXTUAL NUDGE CARD (STRICT MULTI-CATEGORY ROUTING & NO DEFAULT)
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
