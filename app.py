import streamlit as st
import json
import time
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
# DYNAMIC BLINKIT CATALOG LOADING
# -----------------------------------------------------------------------------
@st.cache_data
def load_blinkit_catalog():
    if os.path.exists("blinkit_catalog.csv"):
        df = pd.read_csv("blinkit_catalog.csv")
        return df.to_dict(orient="records")
    else:
        return [
            {"id": "blue_tokai", "name": "Blue Tokai Dark Roast Coffee Beans 250g", "category": "Gourmet & Specialty", "price": 490, "mrp": 550, "emoji": "☕"},
            {"id": "amul_milk", "name": "Amul Taaza T-Special Milk 1L", "category": "Dairy & Breakfast", "price": 72, "mrp": 75, "emoji": "🥛"},
            {"id": "doritos", "name": "Doritos Nacho Cheese Chips 150g", "category": "Munchies & Snacks", "price": 60, "mrp": 60, "emoji": "🧀"},
            {"id": "lays_chips", "name": "Lay's India's Magic Masala Chips 90g", "category": "Munchies & Snacks", "price": 40, "mrp": 40, "emoji": "🥔"},
            {"id": "red_bull", "name": "Red Bull Energy Drink 250ml", "category": "Beverages & Cold Drinks", "price": 125, "mrp": 125, "emoji": "⚡"},
            {"id": "minimalist_serum", "name": "Minimalist 10% Vitamin C Face Serum 30ml", "category": "Beauty & Personal Care", "price": 664, "mrp": 699, "emoji": "🧴"},
            {"id": "spigen_charger", "name": "Spigen 20W Type-C Fast Wall Charger", "category": "Electronics & Tech", "price": 899, "mrp": 1499, "emoji": "🔌"},
            {"id": "pampers_wipes", "name": "Pampers Fresh Clean Baby Wipes (80 Sheets)", "category": "Baby Care", "price": 185, "mrp": 225, "emoji": "👶"},
            {"id": "pedigree_food", "name": "Pedigree Adult Dry Dog Food 1.2kg", "category": "Pet Care", "price": 380, "mrp": 410, "emoji": "🐶"}
        ]

CATALOG_LIST = load_blinkit_catalog()
CATALOG_DF = pd.DataFrame(CATALOG_LIST)

# -----------------------------------------------------------------------------
# SESSION STATE INITIALIZATION
# -----------------------------------------------------------------------------
if "cart" not in st.session_state:
    st.session_state.cart = [
        {"id": "doritos", "name": "Doritos Nacho Cheese Chips 150g", "category": "Munchies & Snacks", "price": 60, "emoji": "🧀"},
        {"id": "red_bull", "name": "Red Bull Energy Drink 250ml", "category": "Beverages & Cold Drinks", "price": 125, "emoji": "⚡"}
    ]

if "nudge_added" not in st.session_state:
    st.session_state.nudge_added = False

if "order_placed" not in st.session_state:
    st.session_state.order_placed = False

if "exchange_triggered" not in st.session_state:
    st.session_state.exchange_triggered = False

# -----------------------------------------------------------------------------
# GEMINI API / LOCAL FALLBACK RECOMMENDATION LOGIC WITH WATERTIGHT MATRIX
# -----------------------------------------------------------------------------
def get_blinksmart_recommendation(cart_items, api_key=""):
    cart_names = [item["name"] for item in cart_items]
    cart_categories = [item.get("category", "") for item in cart_items]
    cart_text = " ".join(cart_names).lower() + " " + " ".join(cart_categories).lower()

    # Silent API Key resolution
    if not api_key:
        api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_AI_STUDIO_API_KEY") or getattr(st, "secrets", {}).get("GEMINI_API_KEY", "")

    # Attempt Live Gemini API Call with tight pairing instructions
    if api_key:
        try:
            endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            prompt = f"""
            Act as the BlinkSmart Recommendation Engine for Blinkit quick commerce.
            Active Cart Items: {cart_names}
            Cart Categories: {cart_categories}
            Location: DLF Phase 3, Gurgaon.
            
            Recommend strictly ONE high-margin non-grocery SKU (Electronics & Tech, Beauty & Personal Care, Home & Kitchen, Baby Care, or Pet Care) that contextually pairs with this cart mix based on this matrix:
            1. Grocery Staples (Atta, Rice, Oil, Dal, Spices) -> Recommend "Portronics Digital Kitchen Weight Scale" (Home & Kitchen, ₹399) - Scenario: "👩🍳 Perfect Kitchen Measurement". Co-buying utility: "Measure exact flour-to-water ratios with 1-gram precision to consistently make soft, fluffy rotis and dough without guessing."
            2. Munchies & Snacks (Doritos, Lays, Chips, Popcorn) -> Recommend "Portronics Adjustable Multi-Angle Desktop Phone Stand" (Electronics & Tech, ₹299) - Scenario: "📺 Hands-Free Binge Watching". Co-buying utility: "Prop your phone hands-free to watch YouTube or sports while eating chips, keeping your touchscreen clean from grease and cheese dust."
            3. Dairy, Gourmet & Breakfast (Coffee, Milk, Bread, Eggs, Butter) -> Recommend "InstaCuppa Electric Milk Frother & Hand Mixer" (Home & Kitchen, ₹799) - Scenario: "☕ 15-Second Homemade Cafe Foam". Co-buying utility: "Blend cold milk and espresso shots directly in your glass to create cafe-style thick, frothy lattes and iced frappes in 15 seconds."
            4. Fruits & Vegetables -> Recommend "Minimalist 10% Vitamin C Face Serum (30ml)" (Beauty & Personal Care, ₹664) - Scenario: "✨ Clean Morning Skin Routine". Co-buying utility: "Apply 2-3 drops during your morning breakfast routine to boost skin glow and protect against daily metro pollution."
            5. Baby Care (Wipes, Diapers) -> Recommend "Sebamed Baby Gentle Body Lotion 200ml" (Baby Care, ₹540) - Scenario: "👶 Baby Skin Care Essentials". Co-buying utility: "Use after cleansing with baby wipes to lock in 24-hour moisture and protect delicate infant skin."
            6. Pet Care (Dog/Cat Food) -> Recommend "Whiskas Wet Cat Food Ocean Fish (4 Pack)" (Pet Care, ₹195) - Scenario: "🐾 Pet Nutrition Booster". Co-buying utility: "Mix wet gravy food with dry kibble to enhance meal palatability and ensure optimal hydration."
            7. Beverages & Cold Drinks -> Recommend "Spigen 20W Fast Type-C Wall Charger Adapter" (Electronics & Tech, ₹899) - Scenario: "⚡ Late-Night Work Power Utility". Co-buying utility: "Power your phone from 0% to 50% in just 25 minutes while enjoying your energy drinks."
            
            Respond strictly in valid JSON format:
            {{
                "title": "Exact Recommended Title",
                "price": 299,
                "mrp": 699,
                "category": "Recommended Category",
                "emoji": "📱",
                "scenario_badge": "Scenario Badge",
                "why_suggested": "Why Suggested",
                "cobuying_utility": "Co-buying utility rationale details.",
                "social_proof": "48 snack lovers in DLF Phase 3 bought this this week"
            }}
            """
            response = requests.post(endpoint, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=4)
            if response.status_code == 200:
                data = response.json()
                text_content = data['candidates'][0]['content']['parts'][0]['text']
                clean_json = text_content.replace("```json", "").replace("```", "").strip()
                return json.loads(clean_json)
        except Exception:
            pass

    # Watertight Rule Engine Fallback Matrix
    # 1. Grocery Staples (Atta, Rice, Cooking Oil, Dal, Spices)
    if any(k in cart_text for k in ["atta", "rice", "oil", "dal", "flour", "cooking", "masala", "spices"]):
        return {
            "title": "Portronics Digital Kitchen Weight Scale",
            "price": 399,
            "mrp": 999,
            "category": "Home & Kitchen",
            "emoji": "⚖️",
            "scenario_badge": "👩‍🍳 Perfect Kitchen Measurement",
            "why_suggested": "Matched to your daily cooking & flour staples order.",
            "cobuying_utility": "Measure exact flour-to-water ratios with 1-gram precision to consistently make soft, fluffy rotis and dough without guessing.",
            "social_proof": "37 home cooks in DLF Phase 3 bought this this week"
        }
    # 2. Munchies & Snacks (Doritos, Lay's, Chips, Popcorn)
    elif any(k in cart_text for k in ["doritos", "lays", "chips", "munchies", "snack", "cheese", "popcorn"]):
        return {
            "title": "Portronics Adjustable Multi-Angle Desktop Phone Stand",
            "price": 299,
            "mrp": 699,
            "category": "Electronics & Tech",
            "emoji": "📱",
            "scenario_badge": "📺 Hands-Free Binge Watching",
            "why_suggested": "Pairs with your snack & munchies selection for desk entertainment.",
            "cobuying_utility": "Prop your phone hands-free to watch YouTube or sports while eating chips, keeping your touchscreen clean from grease and cheese dust.",
            "social_proof": "48 snack lovers in DLF Phase 3 bought this this week"
        }
    # 3. Dairy, Gourmet & Breakfast (Blue Tokai Coffee, Amul Milk, Bread, Eggs, Butter)
    elif any(k in cart_text for k in ["coffee", "milk", "breakfast", "bread", "butter", "tokai", "eggs", "yogurt", "gourmet", "specialty"]):
        return {
            "title": "InstaCuppa Electric Milk Frother & Hand Mixer",
            "price": 799,
            "mrp": 1200,
            "category": "Home & Kitchen",
            "emoji": "⚡",
            "scenario_badge": "☕ 15-Second Homemade Cafe Foam",
            "why_suggested": "Suggested to upgrade your coffee & breakfast basket.",
            "cobuying_utility": "Blend cold milk and espresso shots directly in your glass to create cafe-style thick, frothy lattes and iced frappes in 15 seconds.",
            "social_proof": "32 coffee lovers in DLF Phase 3 bought this this week"
        }
    # 4. Fruits & Vegetables (Fresh Hass Avocado, Tomatoes, Fruits)
    elif any(k in cart_text for k in ["avocado", "tomatoes", "bananas", "fruit", "veggie", "vegetable"]):
        return {
            "title": "Minimalist 10% Vitamin C Face Serum (30ml)",
            "price": 664,
            "mrp": 699,
            "category": "Beauty & Personal Care",
            "emoji": "🧴",
            "scenario_badge": "✨ Clean Morning Skin Routine",
            "why_suggested": "Matches your organic fresh produce selection for morning wellness care.",
            "cobuying_utility": "Apply 2-3 drops during your morning breakfast routine to boost skin glow and protect against daily metro pollution.",
            "social_proof": "28 residents in DLF Phase 3 bought this this week"
        }
    # 5. Baby Care (Pampers Baby Wipes, Diapers)
    elif any(k in cart_text for k in ["baby", "wipes", "pampers", "diaper"]):
        return {
            "title": "Sebamed Baby Gentle Body Lotion 200ml",
            "price": 540,
            "mrp": 600,
            "category": "Baby Care",
            "emoji": "🍼",
            "scenario_badge": "👶 Baby Skin Care Essentials",
            "why_suggested": "Complements your baby wipe reorder for complete skin hydration.",
            "cobuying_utility": "Use after cleansing with baby wipes to lock in 24-hour moisture and protect delicate infant skin.",
            "social_proof": "24 parents in DLF Phase 3 bought this this week"
        }
    # 6. Pet Care (Pedigree Dog Food, Whiskas Cat Food)
    elif any(k in cart_text for k in ["dog", "cat", "pet", "pedigree", "whiskas"]):
        return {
            "title": "Whiskas Wet Cat Food Ocean Fish (4 Pack)",
            "price": 195,
            "mrp": 220,
            "category": "Pet Care",
            "emoji": "🐱",
            "scenario_badge": "🐾 Pet Nutrition Booster",
            "why_suggested": "Complements your dry pet food reorder with wet gravy treats.",
            "cobuying_utility": "Mix wet gravy food with dry kibble to enhance meal palatability and ensure optimal hydration.",
            "social_proof": "19 pet owners in DLF Phase 3 bought this this week"
        }
    # 7. Beverages & Cold Drinks (Red Bull, Coca-Cola Zero)
    elif any(k in cart_text for k in ["red bull", "cola", "coca", "beverage", "drink", "energy"]):
        return {
            "title": "Spigen 20W Fast Type-C Wall Charger Adapter",
            "price": 899,
            "mrp": 1499,
            "category": "Electronics & Tech",
            "emoji": "🔌",
            "scenario_badge": "⚡ Late-Night Work Power Utility",
            "why_suggested": "Essential fast-charge utility paired with your active work sprint.",
            "cobuying_utility": "Power your phone from 0% to 50% in just 25 minutes while enjoying your energy drinks.",
            "social_proof": "42 residents in DLF Phase 3 bought this this week"
        }
    # Default Fallback
    else:
        return {
            "title": "Spigen 20W Fast Type-C Wall Charger Adapter",
            "price": 899,
            "mrp": 1499,
            "category": "Electronics & Tech",
            "emoji": "🔌",
            "scenario_badge": "⚡ Desk & Late-Night Power Utility",
            "why_suggested": "Essential fast-charge utility paired with your active order.",
            "cobuying_utility": "Power your phone from 0% to 50% in just 25 minutes while enjoying your snacks and beverages.",
            "social_proof": "42 residents in DLF Phase 3 bought this this week"
        }

# -----------------------------------------------------------------------------
# SIDEBAR CONFIGURATION (NO DEVELOPER API INPUT BOXES)
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 📍 User Profile & Location")
    st.info("**Location:** DLF Phase 3, Gurgaon\n\n**Segment:** Metro Tech Professional\n\n**Order Speed:** ⚡ 10 Mins")
    
    st.divider()
    if st.button("🔄 Reset Simulation Demo"):
        st.session_state.cart = [
            {"id": "doritos", "name": "Doritos Nacho Cheese Chips 150g", "category": "Munchies & Snacks", "price": 60, "emoji": "🧀"},
            {"id": "red_bull", "name": "Red Bull Energy Drink 250ml", "category": "Beverages & Cold Drinks", "price": 125, "emoji": "⚡"}
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
st.caption("Functional MVP Prototype | Search & Add Across ALL Blinkit Categories")

# -----------------------------------------------------------------------------
# SCREEN 1: ORDER PLACED & 10-MIN EXCHANGE SIMULATOR
# -----------------------------------------------------------------------------
if st.session_state.order_placed:
    st.balloons()
    st.success("🎉 Order Placed Successfully in 8 Minutes!")
    st.caption("Fulfillment Dark Store: Gurgaon Sector 43 Hub | Rider Assigned: **Ramesh Kumar**")
    
    st.markdown("---")
    
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
# SCREEN 2: ACTIVE CART & CATEGORY-FILTERED SEARCH BAR
# -----------------------------------------------------------------------------
else:
    st.markdown("#### 🛒 Search & Add Items to Grocery Basket")
    
    col_cat, col_prod, col_btn = st.columns([1.5, 2.5, 1])
    
    all_categories = ["All Categories"] + sorted(list(CATALOG_DF["category"].unique()))
    with col_cat:
        selected_cat = st.selectbox("Category:", all_categories, label_visibility="collapsed")
        
    filtered_df = CATALOG_DF if selected_cat == "All Categories" else CATALOG_DF[CATALOG_DF["category"] == selected_cat]
    product_map = {row["name"]: row for _, row in filtered_df.iterrows()}
    
    selected_title = None
    if product_map:
        with col_prod:
            selected_title = st.selectbox("Select Product:", list(product_map.keys()), label_visibility="collapsed")
        with col_btn:
            if st.button("+ Add Item"):
                item_to_add = product_map[selected_title]
                st.session_state.cart.append(item_to_add)
                st.rerun()
    else:
        with col_prod:
            st.selectbox("Select Product:", ["No products found"], disabled=True, label_visibility="collapsed")

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
        # BLINKSMART CONTEXTUAL AI NUDGE CARD WITH CLEAR CO-BUYING REASONING
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
