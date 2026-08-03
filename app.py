import streamlit as st
import json
import requests
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables (.env / Streamlit secrets)
load_dotenv()

# Robust helper function to strip all leading/trailing whitespace from each line before joining
def clean_html(html_str):
    lines = [line.strip() for line in html_str.splitlines() if line.strip()]
    return " ".join(lines)

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION & BLINKIT BRAND STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="BlinkSmart Zero-Risk Shield MVP",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom light CSS styling matching Blinkit's mobile app theme
st.markdown(clean_html("""
<style>
.main { background-color: #f8fafc; }
.stApp { background-color: #f8fafc; color: #1e293b; }

.blinkit-badge {
    background-color: #f7c200;
    color: #000000;
    font-weight: 800;
    padding: 6px 14px;
    border-radius: 8px;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    font-size: 18px;
    display: inline-block;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.nudge-card {
    background: #f0fdf4;
    border: 1.5px solid #10b981;
    border-radius: 16px;
    padding: 18px;
    margin-top: 14px;
    margin-bottom: 14px;
    box-shadow: 0 4px 15px rgba(16, 185, 129, 0.1);
    color: #1e293b;
}

.nudge-tag {
    background-color: #0c831f;
    color: #ffffff;
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
}

.scenario-badge {
    background-color: #f7c200;
    color: #000000;
    font-weight: 800;
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 11px;
    display: inline-block;
}

.rationale-box {
    background-color: #ffffff !important;
    border: 1.5px solid #10b981 !important;
    border-radius: 12px;
    padding: 14px;
    margin-top: 10px;
    margin-bottom: 12px;
    color: #1e293b !important;
    box-shadow: inset 0 1px 3px rgba(0,0,0,0.02);
}

.shield-badge {
    background-color: #fef08a;
    color: #854d0e;
    font-weight: 700;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 11px;
}

.stButton > button {
    background-color: #0c831f;
    color: white;
    font-weight: 700;
    border-radius: 10px;
    border: none;
    padding: 8px 16px;
    width: 100%;
}
.stButton > button:hover {
    background-color: #15803d;
    color: white;
}
</style>
"""), unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# DYNAMIC BLINKIT CATALOG LOADING (REPRESENTING ALL 19 CATEGORIES)
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
    st.session_state.cart = [
        {"id": "amul_milk_1l", "name": "Amul Taaza T-Special Milk 1L", "category": "Dairy, Bread & Eggs", "price": 72, "emoji": "🥛"}
    ]

if "nudge_added" not in st.session_state:
    st.session_state.nudge_added = False

if "order_placed" not in st.session_state:
    st.session_state.order_placed = False

if "exchange_triggered" not in st.session_state:
    st.session_state.exchange_triggered = False

# -----------------------------------------------------------------------------
# CONSTRAINED RECOMMENDATION MATRIX LOGIC (100% RELIABLE DECISION ENGINE)
# -----------------------------------------------------------------------------
def get_blinksmart_recommendation(cart_items):
    for item in cart_items:
        category = item.get("category", "")
        if category in CATEGORY_RECOMMENDATIONS:
            return CATEGORY_RECOMMENDATIONS[category]

    return CATEGORY_RECOMMENDATIONS["Munchies & Snacks"]

# -----------------------------------------------------------------------------
# CLEAN SIDEBAR CONFIGURATION (ZERO FRONTEND API KEY DISPLAY)
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 📍 Location & User Profile")
    st.info("Location: DLF Phase 3, Gurgaon\n\n**Segment:** Metro Tech Professional\n\n**Delivery Promise:** ⚡ 10 Mins")
    st.divider()
    if st.button("🔄 Reset Simulation Demo"):
        st.session_state.cart = [
            {"id": "amul_milk_1l", "name": "Amul Taaza T-Special Milk 1L", "category": "Dairy, Bread & Eggs", "price": 72, "emoji": "🥛"}
        ]
        st.session_state.nudge_added = False
        st.session_state.order_placed = False
        st.session_state.exchange_triggered = False
        st.rerun()

# -----------------------------------------------------------------------------
# MAIN APP HEADER
# -----------------------------------------------------------------------------
col_logo, col_loc = st.columns([1, 2])
with col_logo:
    st.markdown(clean_html('<span class="blinkit-badge">blinkit</span>'), unsafe_allow_html=True)
with col_loc:
    st.markdown(clean_html("<div style='text-align:right; font-size:12px; color:#475569;'>📍 DLF Phase 3, Gurgaon • <strong style='color:#0c831f;'>10 Mins Delivery</strong></div>"), unsafe_allow_html=True)

st.title("BlinkSmart: Zero-Risk Shield Engine")
st.caption("Functional MVP Prototype | Contextual Non-Grocery Cross-Sell Engine")

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
# SCREEN 2: ACTIVE CART & LIVE SEARCH BAR (100% CATEGORY & SKU COVERAGE)
# -----------------------------------------------------------------------------
else:
    st.markdown("#### 🛒 Search & Add Items to Grocery Basket")
    
    search_query = st.text_input("🔍 Search any product (e.g. Maggi, Oats, Milk, Sunscreen, Coke, Diapers, Colgate, Atta):")
    selected_cat = st.selectbox("Category Filter:", ["All Categories"] + sorted(list(CATALOG_DF["category"].unique())))

    # Dynamically filter dataset
    filtered_df = CATALOG_DF
    if selected_cat != "All Categories":
        filtered_df = filtered_df[filtered_df["category"] == selected_cat]
    if search_query:
        filtered_df = filtered_df[filtered_df["name"].str.contains(search_query, case=False, na=False)]

    product_map = {f"{row.get('emoji', '🛒')} {row['name']} - ₹{row['price']}": row for _, row in filtered_df.iterrows()}

    col_prod, col_btn = st.columns([3.5, 1.5])
    if product_map:
        with col_prod:
            selected_title = st.selectbox("Select Matching Product:", list(product_map.keys()), label_visibility="collapsed")
        with col_btn:
            if st.button("+ Add to Cart", use_container_width=True):
                item_to_add = product_map[selected_title]
                st.session_state.cart.append(item_to_add)
                st.rerun()
    else:
        with col_prod:
            st.selectbox("Select Product:", ["No products found matching search/filter"], disabled=True, label_visibility="collapsed")

    # Active Cart List
    st.markdown("#### 🧺 Active Grocery Basket")
    
    if not st.session_state.cart:
        st.info("🛒 Your basket is empty. Use the search bar above to add items!")
    else:
        subtotal = 0
        for idx, item in enumerate(st.session_state.cart):
            subtotal += item["price"]
            col_item, col_del = st.columns([5, 1])
            with col_item:
                cart_item_html = clean_html(f"""
<div style='display:flex; justify-content:space-between; align-items:center; background-color:#ffffff; border:1px solid #e2e8f0; border-radius:10px; padding:8px 14px; box-shadow:0 1px 3px rgba(0,0,0,0.02);'>
<div>
<span style='font-size:16px;'>{item.get('emoji', '🛒')}</span>
<strong style='font-size:13px; color:#1e293b; margin-left:8px;'>{item['name']}</strong>
<span style='font-size:10px; color:#64748b; margin-left:6px;'>({item.get('category', 'Grocery')})</span>
</div>
<span style='font-weight:bold; font-size:13px; color:#1e293b;'>₹{item['price']}</span>
</div>
""")
                st.markdown(cart_item_html, unsafe_allow_html=True)
            with col_del:
                if st.button("❌", key=f"del_{idx}"):
                    st.session_state.cart.pop(idx)
                    st.rerun()

        # -------------------------------------------------------------------------
        # BLINKSMART CONTEXTUAL AI NUDGE CARD (CLEAN VISUAL HTML RENDERING)
        # -------------------------------------------------------------------------
        rec = get_blinksmart_recommendation(st.session_state.cart)

        nudge_card_html = clean_html(f"""
<div class="nudge-card">
<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
<span class="nudge-tag">✨ BlinkSmart Contextual Nudge</span>
<span class="scenario-badge">{rec['scenario_badge']}</span>
</div>
<div class="rationale-box">
<div style="font-size:11px; color:#0c831f; font-weight:800; margin-bottom:2px;">🎯 WHY SUGGESTED:</div>
<div style="font-size:12px; color:#1e293b; margin-bottom:8px;">{rec['why_suggested']}</div>
<div style="font-size:11px; color:#d97706; font-weight:800; margin-bottom:2px;">🤝 CO-BUYING UTILITY:</div>
<div style="font-size:12px; color:#475569; line-height:1.4;">"{rec['cobuying_utility']}"</div>
</div>
<div style="background-color:#ffffff; border:1px solid #e2e8f0; border-radius:12px; padding:12px; display:flex; justify-content:space-between; align-items:center; box-shadow:0 1px 3px rgba(0,0,0,0.02);">
<div>
<div style="font-size:18px; margin-bottom:2px;">{rec['emoji']} <strong style="font-size:13px; color:#1e293b;">{rec['title']}</strong></div>
<div style="font-size:11px; color:#0c831f; font-weight:600;">🔰 100% Brand Authenticity Seal</div>
<div style="margin-top:4px;">
<span style="font-size:14px; font-weight:800; color:#0c831f;">₹{rec['price']}</span>
<span style="font-size:11px; color:#64748b; text-decoration:line-through; margin-left:4px;">₹{rec['mrp']}</span>
</div>
</div>
</div>
<div style="margin-top:12px; font-size:12px; color:#475569; display:flex; justify-content:space-between; align-items:center;">
<span>👥 <strong>{rec['social_proof']}</strong></span>
<span class="shield-badge">🔰 1st Trial Shield Active</span>
</div>
</div>
""")
        st.markdown(nudge_card_html, unsafe_allow_html=True)

        # Nudge Add Action Button
        if not st.session_state.nudge_added:
            if st.button(f"+ Add {rec['title']} to Order (₹15 Fee Waived)"):
                st.session_state.nudge_added = True
                st.rerun()
        else:
            st.success(f"✓ {rec['title']} Added to Basket with First-Trial Shield!")
            subtotal += rec['price']

        # -------------------------------------------------------------------------
        # BILL SUMMARY & FAST CHECKOUT BAR
        # -------------------------------------------------------------------------
        st.markdown("#### 📄 Bill Summary")
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

        # Sticky Checkout Bar
        if st.button(f"Pay ₹{grand_total} via Face ID / UPI (<15s) ➔"):
            st.session_state.order_placed = True
            st.rerun()
