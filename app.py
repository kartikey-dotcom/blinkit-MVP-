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
# PAGE CONFIGURATION & OFFICIAL BLINKIT LIGHT UX THEME (#F4F6FB, #F7C200, #0C831F)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Blinkit Quick Commerce | Mobile App MVP",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Light Theme & Differentiated CTA Visual Hierarchy
st.markdown(clean_html("""
<style>
/* Blinkit Palette: Yellow #F7C200, Green #0C831F, Light Background #F4F6FB, Text #111827 */
.main { background-color: #F4F6FB; padding: 10px 0; }
.stApp { background-color: #F4F6FB; color: #111827; font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'SF Pro Text', 'Segoe UI', Roboto, sans-serif; }

/* Hide default streamlit headers/footers for app feel */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }

/* iOS Top Status Bar & Dynamic Island */
.ios-status-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 16px 4px 16px;
    font-size: 12px;
    font-weight: 700;
    color: #111827;
    background-color: #FFFFFF;
    border-top-left-radius: 20px;
    border-top-right-radius: 20px;
    border-bottom: 1px solid #F1F5F9;
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
    background-color: #F0FDF4;
    border: 1.5px solid #BBF7D0;
    color: #0C831F;
    font-weight: 800;
    font-size: 11px;
    padding: 4px 12px;
    border-radius: 20px;
    display: inline-block;
    text-align: center;
}

.nudge-card {
    background: #FFFFFF;
    border: 1.5px solid #10B981;
    border-radius: 16px;
    padding: 16px;
    margin-top: 14px;
    margin-bottom: 14px;
    box-shadow: 0 4px 15px rgba(16, 185, 129, 0.08);
    color: #1E293B;
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
    background-color: #F8FAFC !important;
    border: 1.5px solid #10B981 !important;
    border-radius: 12px;
    padding: 12px;
    margin-top: 10px;
    margin-bottom: 12px;
    color: #1E293B !important;
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
    background-color: #0C831F;
    color: #FFFFFF;
    font-weight: 800;
    border-radius: 10px;
    border: none;
    padding: 8px 14px;
    font-size: 13px;
    width: 100%;
    box-shadow: 0 2px 4px rgba(12, 131, 31, 0.2);
}
.stButton > button:hover {
    background-color: #096818;
    color: #FFFFFF;
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
    background-color: #FFFFFF;
    border-top: 1px solid #E5E7EB;
    padding: 10px 0 6px 0;
    margin-top: 20px;
    border-radius: 16px;
    box-shadow: 0 -2px 10px rgba(0,0,0,0.03);
}

.ios-tab-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    font-size: 10px;
    font-weight: 600;
    color: #6B7280;
}

.ios-tab-item.active {
    color: #0C831F;
    font-weight: 800;
}

.ios-home-indicator {
    width: 134px;
    height: 5px;
    background-color: #CBD5E1;
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
# UNIVERSAL 100% CATEGORY RECOMMENDATION MATRIX (COVERING ALL 19 CATEGORIES)
# -----------------------------------------------------------------------------
CATEGORY_RECOMMENDATIONS = {
    "Dairy, Bread & Eggs": {
        "title": "InstaCuppa Electric Milk Frother & Hand Mixer",
        "price": 799,
        "mrp": 1200,
        "category": "Home & Kitchen Utilities",
        "emoji": "⚡",
        "scenario_badge": "☕ 15-Second Homemade Cafe Foam",
        "why_suggested": "Suggested to upgrade your milk & breakfast basket.",
        "cobuying_utility": "Blend cold milk and espresso shots directly in your glass to create cafe-style thick, frothy lattes and iced frappes in 15 seconds.",
        "social_proof": "32 coffee lovers in DLF Phase 3 bought this this week"
    },
    "Fruits & Vegetables": {
        "title": "Portronics Digital Kitchen Scale",
        "price": 399,
        "mrp": 999,
        "category": "Home & Kitchen Utilities",
        "emoji": "⚖️",
        "scenario_badge": "👩‍🍳 Perfect Kitchen Portioning",
        "why_suggested": "Matches your fresh produce and cooking ingredients.",
        "cobuying_utility": "Weigh salad portions, recipe ingredients, and meal preps with 1g accuracy.",
        "social_proof": "54 home cooks in DLF Phase 3 bought this this week"
    },
    "Grocery & Staples": {
        "title": "Portronics Digital Kitchen Scale",
        "price": 399,
        "mrp": 999,
        "category": "Home & Kitchen Utilities",
        "emoji": "⚖️",
        "scenario_badge": "👩‍🍳 Perfect Kitchen Measurement",
        "why_suggested": "Matched to your daily cooking & flour staples selection.",
        "cobuying_utility": "Measure exact flour-to-water ratios with 1-gram precision to consistently make soft, fluffy rotis and dough without guessing.",
        "social_proof": "54 home cooks in DLF Phase 3 bought this this week"
    },
    "Munchies & Snacks": {
        "title": "Portronics Multi-Angle Desktop Phone Stand",
        "price": 249,
        "mrp": 699,
        "category": "Electronics & Tech Accessories",
        "emoji": "📱",
        "scenario_badge": "📺 Hands-Free Binge Watching",
        "why_suggested": "Pairs with your snack & munchies selection for desk entertainment.",
        "cobuying_utility": "Prop your phone hands-free to watch YouTube or sports while eating chips, keeping your touchscreen clean from grease and cheese dust.",
        "social_proof": "48 snack lovers in DLF Phase 3 bought this this week"
    },
    "Beverages & Cold Drinks": {
        "title": "Borosil Vacuum Insulated Stainless Steel Tumbler",
        "price": 699,
        "mrp": 999,
        "category": "Home & Kitchen Utilities",
        "emoji": "🥤",
        "scenario_badge": "❄️ Sub-Zero Beverage Chill",
        "why_suggested": "Pairs with your choice of beverages & cold drinks.",
        "cobuying_utility": "Pour cold energy drinks or sodas into the vacuum insulated tumbler to keep them sub-zero cold for up to 12 hours without watering them down with ice.",
        "social_proof": "42 drink lovers in DLF Phase 3 bought this this week"
    },
    "Tea, Coffee & Health Drinks": {
        "title": "InstaCuppa Electric Milk Frother & Hand Mixer",
        "price": 799,
        "mrp": 1200,
        "category": "Home & Kitchen Utilities",
        "emoji": "⚡",
        "scenario_badge": "☕ Cafe-Style Instant Froth",
        "why_suggested": "Perfect pairing for your tea & premium coffee beans.",
        "cobuying_utility": "Froth milk in 15 seconds to prepare barista-grade lattes and cappuccinos right at home.",
        "social_proof": "61 coffee enthusiasts in DLF Phase 3 bought this this week"
    },
    "Instant & Frozen Food": {
        "title": "Borosil Microwave Safe Glass Bowl",
        "price": 299,
        "mrp": 499,
        "category": "Home & Kitchen Utilities",
        "emoji": "🥣",
        "scenario_badge": "🍜 2-Min Instant Microwave Heating",
        "why_suggested": "Complements your instant noodles and quick meals.",
        "cobuying_utility": "Safely heat ramen, soups, and frozen snacks without toxic plastic leaching.",
        "social_proof": "39 instant food lovers in DLF Phase 3 bought this this week"
    },
    "Sweet Tooth, Chocolates & Bakery": {
        "title": "Borosil Microwave Safe Glass Bowl",
        "price": 299,
        "mrp": 499,
        "category": "Home & Kitchen Utilities",
        "emoji": "🥣",
        "scenario_badge": "🍫 Instant Dessert Fondue",
        "why_suggested": "Matched with your premium sweet & chocolate order.",
        "cobuying_utility": "Melt chocolate or heat syrup in this microwave-safe bowl for an instant, rich dessert fondue dip with fruit skewers or cookies.",
        "social_proof": "29 chocolate lovers in DLF Phase 3 bought this this week"
    },
    "Beauty & Cosmetics": {
        "title": "Jade Facial Roller & Gua Sha Massager Set",
        "price": 499,
        "mrp": 999,
        "category": "Beauty & Personal Care",
        "emoji": "💎",
        "scenario_badge": "✨ Facial Sculpt & Glow Massage",
        "why_suggested": "Complements your beauty & skincare serum selection.",
        "cobuying_utility": "Massage skin after applying sunscreen or serums to enhance product absorption and boost natural circulation.",
        "social_proof": "28 skincare users in DLF Phase 3 bought this this week"
    },
    "Bath, Body & Personal Care": {
        "title": "Microfiber Quick-Dry Bath Hair Towel",
        "price": 299,
        "mrp": 599,
        "category": "Bath, Body & Personal Care",
        "emoji": "🧖‍♀️",
        "scenario_badge": "🚿 Ultra-Soft Post-Shower Care",
        "why_suggested": "Pairs with your shower gel and body care order.",
        "cobuying_utility": "Ultra-absorbent microfiber wrap dries hair 3x faster without frizz or friction damage.",
        "social_proof": "37 personal care buyers in DLF Phase 3 bought this this week"
    },
    "Electronics & Tech Accessories": {
        "title": "Spigen 20W Fast Type-C Wall Charger Adapter",
        "price": 899,
        "mrp": 1499,
        "category": "Electronics & Tech Accessories",
        "emoji": "🔌",
        "scenario_badge": "⚡ High-Speed Power Utility",
        "why_suggested": "Fast charging accessory for your electronic devices.",
        "cobuying_utility": "Power your phone, earbuds, or tablet from 0% to 50% in just 25 minutes with safe, certified wall charging.",
        "social_proof": "72 tech buyers in DLF Phase 3 bought this this week"
    },
    "Home & Kitchen Utilities": {
        "title": "Portronics Digital Kitchen Scale",
        "price": 399,
        "mrp": 999,
        "category": "Home & Kitchen Utilities",
        "emoji": "⚖️",
        "scenario_badge": "👩‍🍳 Precision Cooking Tool",
        "why_suggested": "Top utility item for modern home kitchen setups.",
        "cobuying_utility": "Accurately measure baking and cooking ingredients down to 1 gram.",
        "social_proof": "45 home makers in DLF Phase 3 bought this this week"
    },
    "Cleaning & Household Essentials": {
        "title": "Waterproof Silicon Cleaning Gloves",
        "price": 249,
        "mrp": 499,
        "category": "Cleaning & Household Essentials",
        "emoji": "🧤",
        "scenario_badge": "🧼 Safe Cleaning Guard",
        "why_suggested": "Matched to your cleaning supplies & household order.",
        "cobuying_utility": "Protect your hands from harsh detergent chemicals and grease while washing dishes or doing deep household cleaning.",
        "social_proof": "31 home makers in DLF Phase 3 bought this this week"
    },
    "Baby Care": {
        "title": "Ultra-Soft Bamboo Baby Washcloth Set",
        "price": 299,
        "mrp": 499,
        "category": "Baby Care",
        "emoji": "👶",
        "scenario_badge": "🍼 Gentle Baby Skincare",
        "why_suggested": "Complements your baby wipes and hygiene essentials.",
        "cobuying_utility": "Use these ultra-soft bamboo washcloths for gentle wiping to prevent diaper rash and irritation on delicate baby skin.",
        "social_proof": "24 parents in DLF Phase 3 bought this this week"
    },
    "Pet Care": {
        "title": "Interactive Pet Slow-Feeder Lick Mat",
        "price": 349,
        "mrp": 599,
        "category": "Pet Care",
        "emoji": "🐾",
        "scenario_badge": "🐶 Calming slow-feeding aid",
        "why_suggested": "Complements your dog/cat food and treats.",
        "cobuying_utility": "Spread wet gravy food or peanut butter on the slow-feeder lick mat to calm your pets and slow down fast eating during feeding sessions.",
        "social_proof": "19 pet owners in DLF Phase 3 bought this this week"
    },
    "Health, Pharma & Wellness": {
        "title": "Weekly Pill Organizer & Hydration Bottle",
        "price": 399,
        "mrp": 699,
        "category": "Health, Pharma & Wellness",
        "emoji": "💊",
        "scenario_badge": "💧 Daily Hydration & Supplement Track",
        "why_suggested": "Pairs with your pharmacy & wellness selection.",
        "cobuying_utility": "Organize your weekly supplements and track your daily hydration intake with this multi-compartment bottle combo.",
        "social_proof": "22 health lovers in DLF Phase 3 bought this this week"
    },
    "Stationery, Books & Games": {
        "title": "Parker Vector Stainless Steel Gel Pen",
        "price": 275,
        "mrp": 300,
        "category": "Stationery, Books & Games",
        "emoji": "🖊️",
        "scenario_badge": "📝 Smooth Executive Writing",
        "why_suggested": "Pairs with your notebooks and desk stationery.",
        "cobuying_utility": "Premium stainless steel gel pen for smooth, smudge-free daily note-taking.",
        "social_proof": "18 desk workers in DLF Phase 3 bought this this week"
    },
    "Paan & Party Essentials": {
        "title": "Catch Club Soda 750ml",
        "price": 20,
        "mrp": 20,
        "category": "Paan & Party Essentials",
        "emoji": "🥤",
        "scenario_badge": "🎉 Party Beverage Mixer",
        "why_suggested": "Essential mixer for party snacks and mouth fresheners.",
        "cobuying_utility": "Refreshing carbonated soda for quick party drink mixing.",
        "social_proof": "35 party hosts in DLF Phase 3 bought this this week"
    },
    "Meat, Fish & Eggs": {
        "title": "Non-Stick Cast Iron Grill Pan",
        "price": 899,
        "mrp": 1499,
        "category": "Home & Kitchen Utilities",
        "emoji": "🍳",
        "scenario_badge": "🍗 High-Heat Meat Searing",
        "why_suggested": "Ideal cooking utility for fresh poultry, meat, and eggs.",
        "cobuying_utility": "Sear chicken breasts and steaks evenly with restaurant-style grill marks.",
        "social_proof": "27 gourmet cooks in DLF Phase 3 bought this this week"
    }
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

def get_blinksmart_recommendation(cart_items):
    for item in cart_items:
        category = item.get("category", "")
        if category in CATEGORY_RECOMMENDATIONS:
            return CATEGORY_RECOMMENDATIONS[category]
    return CATEGORY_RECOMMENDATIONS["Munchies & Snacks"]

# -----------------------------------------------------------------------------
# TOP APP HEADER (1:2:1 CENTERED MIDPOINT ALIGNMENT IN LIGHT THEME)
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
        <div style='font-size:12px; font-weight:800; color:#111827; margin-bottom:3px;'>📍 DLF Phase 3, Gurgaon</div>
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
<div style='background-color:#f0fdf4; border: 1.5px solid #10b981; border-radius:12px; padding:16px; margin-bottom:16px;'>
<div style='display:flex; justify-content:space-between; align-items:center;'>
<span style='color:#0c831f; font-weight:800; font-size:14px;'>🔰 First-Trial Safety Net Active</span>
<span style='background-color:#f7c200; color:#000000; font-family:monospace; font-weight:bold; padding:2px 8px; border-radius:4px;'>09:59 MINS</span>
</div>
<p style='font-size:12px; color:#1e293b; margin-top:8px;'>
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
<div style='background-color:#ffffff; border:1px solid #e2e8f0; border-radius:10px; padding:12px; font-size:12px; box-shadow:0 1px 3px rgba(0,0,0,0.05);'>
<div style='font-weight:bold; color:#1e293b; margin-bottom:4px;'>🛵 Live Exchange Status Log:</div>
<div style='color:#0c831f;'>• Exchange request logged via automated chatbot.</div>
<div style='color:#475569;'>• Rider Ramesh Kumar dispatched with fresh sealed unit from dark store.</div>
<div style='color:#475569;'>• Estimated Doorstep Swap Time: <strong>7 Minutes</strong>.</div>
</div>
""")
        st.markdown(exchange_log_html, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# SCREEN 2: CART-FIRST RE-ORDERED INFORMATION ARCHITECTURE
# -----------------------------------------------------------------------------
else:
    # -------------------------------------------------------------------------
    # 1. SEARCH & CATALOG LISTING / SELECTION
    # -------------------------------------------------------------------------
    st.markdown("<div style='font-weight:800; font-size:15px; color:#111827;'>🔍 Search & Add Grocery Items</div>", unsafe_allow_html=True)
    
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

    # Filter catalog dataset
    filtered_df = CATALOG_DF
    if target_category != "All Categories":
        filtered_df = filtered_df[filtered_df["category"] == target_category]
    
    # Clean Search Banner Logic (Suppress error box on empty, whitespace, or '-')
    if search_query and search_query.strip() not in ["", "-"]:
        filtered_df = filtered_df[filtered_df["name"].str.contains(search_query, case=False, na=False)]

    product_map = {f"{row.get('emoji', '🛒')} {row['name']} — ₹{row['price']}": row for _, row in filtered_df.iterrows()}

    if product_map:
        selected_item_key = st.selectbox("Select Product to Add:", list(product_map.keys()))
        if st.button("+ Add Item to Grocery Basket", use_container_width=True, key="add_catalog_item_btn"):
            item_to_add = product_map[selected_item_key]
            st.session_state.cart.append(item_to_add)
            st.rerun()
    else:
        # Triggered ONLY during actual failed searches
        if search_query and search_query.strip() not in ["", "-"]:
            st.info("🔍 No products match your search query. Try searching for milk, sunscreen, chips, or oats.")

    st.markdown("---")

    # -------------------------------------------------------------------------
    # 2. ACTIVE GROCERY BASKET (RENDERS FIRST BELOW CATALOG)
    # -------------------------------------------------------------------------
    st.markdown("<div style='font-weight:800; font-size:15px; color:#111827;'>🧺 Active Grocery Basket</div>", unsafe_allow_html=True)
    
    if not st.session_state.cart:
        st.info("🛒 Your basket is empty. Select an item above to add!")
    else:
        subtotal = 0
        for idx, item in enumerate(st.session_state.cart):
            subtotal += item["price"]
            col_item, col_del = st.columns([4.5, 0.8])
            with col_item:
                cart_item_html = clean_html(f"""
                <div style='display:flex; justify-content:space-between; align-items:center; background-color:#ffffff; border:1px solid #E5E7EB; border-radius:10px; padding:8px 12px; margin-bottom:6px;'>
                    <div>
                        <span style='font-size:16px;'>{item.get('emoji', '🛒')}</span>
                        <strong style='font-size:13px; color:#111827; margin-left:6px;'>{item['name']}</strong>
                    </div>
                    <span style='font-weight:bold; font-size:13px; color:#111827;'>₹{item['price']}</span>
                </div>
                """)
                st.markdown(cart_item_html, unsafe_allow_html=True)
            with col_del:
                if st.button("❌", key=f"del_cart_{idx}"):
                    st.session_state.cart.pop(idx)
                    st.rerun()

    st.markdown("---")

    # -------------------------------------------------------------------------
    # 3. BLINKSMART CONTEXTUAL NUDGE CARD (RENDERS SECOND BELOW BASKET)
    # -------------------------------------------------------------------------
    rec = get_blinksmart_recommendation(st.session_state.cart)

    nudge_card_html = clean_html(f"""
<div class="nudge-card">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
        <span class="nudge-tag">✨ BlinkSmart Contextual Nudge</span>
        <span class="scenario-badge">{rec['scenario_badge']}</span>
    </div>
    <div class="rationale-box">
        <div style="font-size:11px; color:#0C831F; font-weight:800; margin-bottom:2px;">🎯 WHY SUGGESTED:</div>
        <div style="font-size:12px; color:#111827; margin-bottom:4px;">{rec['why_suggested']}</div>
        <div style="font-size:11px; color:#D97706; font-weight:800; margin-bottom:2px;">🤝 CO-BUYING UTILITY:</div>
        <div style="font-size:12px; color:#475569; line-height:1.4;">"{rec['cobuying_utility']}"</div>
    </div>
    <div style="background-color:#FFFFFF; border:1px solid #E5E7EB; border-radius:12px; padding:10px; display:flex; justify-content:space-between; align-items:center;">
        <div>
            <div style="font-size:15px; font-weight:700; color:#111827;">{rec['emoji']} {rec['title']}</div>
            <div style="font-size:11px; color:#0C831F; font-weight:600;">🔰 100% Brand Authenticity Seal</div>
            <div style="margin-top:4px;">
                <span style="font-size:14px; font-weight:800; color:#0C831F;">₹{rec['price']}</span>
                <span style="font-size:11px; color:#9CA3AF; text-decoration:line-through; margin-left:4px;">₹{rec['mrp']}</span>
            </div>
        </div>
    </div>
    <div style="margin-top:8px; font-size:11px; color:#475569; display:flex; justify-content:space-between; align-items:center;">
        <span>👥 <strong>{rec['social_proof']}</strong></span>
        <span class="shield-badge">🔰 1st Trial Shield Active</span>
    </div>
</div>
""")
    st.markdown(nudge_card_html, unsafe_allow_html=True)

    # Differentiated Secondary CTA button styling (Blinkit Gold #F7C200)
    if not st.session_state.nudge_added:
        st.markdown('<div class="nudge-btn-wrapper">', unsafe_allow_html=True)
        if st.button(f"+ Add {rec['title']} to Order (₹15 Fee Waived)", key="add_nudge_btn"):
            st.session_state.nudge_added = True
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.success(f"✓ {rec['title']} Added to Basket with First-Trial Shield!")

    st.markdown("---")

    # -------------------------------------------------------------------------
    # 4. BILL SUMMARY & PRIMARY CHECKOUT CTA (RENDERS THIRD)
    # -------------------------------------------------------------------------
    if st.session_state.cart:
        if st.session_state.nudge_added:
            subtotal += rec['price']

        st.markdown("<div style='font-weight:800; font-size:14px; color:#111827; margin-top:10px;'>📄 Bill Summary</div>", unsafe_allow_html=True)
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
        <span style="font-size:18px;">🔍</span>
        <span>Search</span>
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
