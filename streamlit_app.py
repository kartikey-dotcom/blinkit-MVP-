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
# DYNAMIC BLINKIT CATALOG LOADING
# -----------------------------------------------------------------------------
@st.cache_data
def load_blinkit_catalog():
    if os.path.exists("blinkit_catalog.csv"):
        df = pd.read_csv("blinkit_catalog.csv")
        return df.to_dict(orient="records")
    else:
        return [
            {"id": "aashirvaad_atta", "name": "Aashirvaad Shuddh Chakki Atta 5kg", "category": "Grocery & Staples", "price": 245, "mrp": 270, "emoji": "🌾"},
            {"id": "blue_tokai", "name": "Blue Tokai Dark Roast Coffee Beans 250g", "category": "Gourmet & Specialty", "price": 490, "mrp": 550, "emoji": "☕"},
            {"id": "amul_milk", "name": "Amul Taaza T-Special Milk 1L", "category": "Dairy & Breakfast", "price": 72, "mrp": 75, "emoji": "🥛"},
            {"id": "doritos", "name": "Doritos Nacho Cheese Chips 150g", "category": "Munchies & Snacks", "price": 60, "mrp": 60, "emoji": "🧀"},
            {"id": "lays_chips", "name": "Lay's India's Magic Masala Chips 90g", "category": "Munchies & Snacks", "price": 40, "mrp": 40, "emoji": "🥔"},
            {"id": "red_bull", "name": "Red Bull Energy Drink 250ml", "category": "Beverages & Cold Drinks", "price": 125, "mrp": 125, "emoji": "⚡"},
            {"id": "avocado", "name": "Fresh Imported Hass Avocado (2 pcs)", "category": "Fruits & Vegetables", "price": 299, "mrp": 350, "emoji": "🥑"},
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
        {"id": "amul_milk", "name": "Amul Taaza T-Special Milk 1L", "category": "Dairy & Breakfast", "price": 72, "emoji": "🥛"}
    ]

if "nudge_added" not in st.session_state:
    st.session_state.nudge_added = False

if "order_placed" not in st.session_state:
    st.session_state.order_placed = False

if "exchange_triggered" not in st.session_state:
    st.session_state.exchange_triggered = False

# -----------------------------------------------------------------------------
# CONSTRAINED GEMINI API / FEW-SHOT FALLBACK LOGIC
# -----------------------------------------------------------------------------
def get_blinksmart_recommendation(cart_items):
    # Fetch Gemini API Key silently from environment or secrets (NO FRONTEND DISPLAY)
    api_key = os.environ.get("GEMINI_API_KEY") or getattr(st, "secrets", {}).get("GEMINI_API_KEY", "")
    cart_names = [item["name"] for item in cart_items]
    cart_categories = [item.get("category", "") for item in cart_items]
    cart_text = " ".join(cart_names).lower() + " " + " ".join(cart_categories).lower()

    # Attempt Live Gemini Call with Strict Few-Shot In-Context Training
    if api_key:
        try:
            endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            prompt = f"""
            Act as the BlinkSmart Recommendation Engine for Blinkit quick commerce.
            Active Cart Items: {cart_names}
            Cart Categories: {cart_categories}
            Location: DLF Phase 3, Gurgaon.
            
            STRICT CONSTRAINTS & CATEGORY PAIRING RULES:
            1. NEVER recommend tech chargers, power banks, or USB cables for Dairy, Breakfast, Fruits, Vegetables, or Cooking Staples.
            2. Grocery & Staples (Atta, Rice, Flour, Oil) MUST recommend Home & Kitchen utilities (Kitchen Scale, Electric Kettle).
            3. Dairy & Breakfast (Milk, Coffee, Bread, Eggs) MUST recommend Frothers, Coffee Mixers, or Breakfast Appliances.
            4. Snacks & Munchies (Doritos, Chips, Popcorn) MUST recommend Desktop Phone Stands or Wet Wipes.
            
            FEW-SHOT EXAMPLES:
            Example 1 Input: ["Amul Milk", "Blue Tokai Coffee"]
            Example 1 Output:
            {{
                "title": "InstaCuppa Electric Milk Frother & Hand Mixer",
                "price": 799, "mrp": 1200, "category": "Home & Kitchen", "emoji": "⚡",
                "scenario_badge": "☕ 15-Second Homemade Cafe Foam",
                "why_suggested": "Suggested to upgrade your daily coffee & milk selection.",
                "cobuying_utility": "Blend cold milk and espresso shots directly in your glass to create thick, frothy lattes in 15 seconds.",
                "social_proof": "32 coffee lovers in DLF Phase 3 bought this this week"
            }}

            Example 2 Input: ["Aashirvaad Atta 5kg", "Fortune Sunflower Oil"]
            Example 2 Output:
            {{
                "title": "Portronics Digital Kitchen Weight Scale",
                "price": 399, "mrp": 899, "category": "Home & Kitchen", "emoji": "⚖️",
                "scenario_badge": "👩🍳 Perfect Kitchen Measurement",
                "why_suggested": "Matched to your daily cooking & flour staples selection.",
                "cobuying_utility": "Measure exact flour-to-water ratios with 1-gram precision to consistently make soft, fluffy rotis every time.",
                "social_proof": "54 home cooks in DLF Phase 3 bought this this week"
            }}

            Example 3 Input: ["Doritos Nacho Cheese", "Lay's Chips"]
            Example 3 Output:
            {{
                "title": "Portronics Multi-Angle Desktop Phone Stand",
                "price": 299, "mrp": 699, "category": "Electronics & Tech", "emoji": "📱",
                "scenario_badge": "📺 Hands-Free Binge Watching",
                "why_suggested": "Pairs with your snack & munchies selection for desk entertainment.",
                "cobuying_utility": "Prop your phone hands-free to watch YouTube or sports while eating Doritos, keeping your touchscreen clean from cheese dust and grease.",
                "social_proof": "48 snack lovers in DLF Phase 3 bought this this week"
            }}

            Respond strictly in valid JSON format matching the schema above.
            """
            response = requests.post(endpoint, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=4)
            if response.status_code == 200:
                data = response.json()
                text_content = data['candidates'][0]['content']['parts'][0]['text']
                clean_json = text_content.replace("```json", "").replace("```", "").strip()
                return json.loads(clean_json)
        except Exception:
            pass

    # Watertight Python Rule Engine (Guarantees Relevant Suggestions)
    if any(k in cart_text for k in ["atta", "rice", "oil", "staples", "flour", "dal", "wheat"]):
        return {
            "title": "Portronics Digital Kitchen Weight Scale",
            "price": 399,
            "mrp": 899,
            "category": "Home & Kitchen",
            "emoji": "⚖️",
            "scenario_badge": "👩‍🍳 Perfect Kitchen Measurement",
            "why_suggested": "Matched to your daily cooking & flour staples selection.",
            "cobuying_utility": "Measure exact flour-to-water ratios with 1-gram precision to consistently make soft, fluffy rotis and dough without guessing.",
            "social_proof": "54 home cooks in DLF Phase 3 bought this this week"
        }
    elif any(k in cart_text for k in ["milk", "coffee", "breakfast", "bread", "eggs", "butter", "dairy", "tokai"]):
        return {
            "title": "InstaCuppa Electric Milk Frother & Hand Mixer",
            "price": 799,
            "mrp": 1200,
            "category": "Home & Kitchen",
            "emoji": "⚡",
            "scenario_badge": "☕ 15-Second Homemade Cafe Foam",
            "why_suggested": "Suggested to upgrade your milk & breakfast basket.",
            "cobuying_utility": "Blend cold milk and espresso shots directly in your glass to create cafe-style thick, frothy lattes and iced frappes in 15 seconds.",
            "social_proof": "32 coffee lovers in DLF Phase 3 bought this this week"
        }
    elif any(k in cart_text for k in ["doritos", "lays", "chips", "munchies", "snack", "popcorn"]):
        return {
            "title": "Portronics Multi-Angle Desktop Phone Stand",
            "price": 299,
            "mrp": 699,
            "category": "Electronics & Tech",
            "emoji": "📱",
            "scenario_badge": "📺 Hands-Free Binge Watching",
            "why_suggested": "Pairs with your snack & munchies selection for desk entertainment.",
            "cobuying_utility": "Prop your phone hands-free to watch YouTube or sports while eating chips, keeping your touchscreen clean from grease and cheese dust.",
            "social_proof": "48 snack lovers in DLF Phase 3 bought this this week"
        }
    elif any(k in cart_text for k in ["baby", "wipes", "pampers", "diaper"]):
        return {
            "title": "Sebamed Baby Gentle Body Lotion 200ml",
            "price": 540,
            "mrp": 600,
            "category": "Baby Care",
            "emoji": "🍼",
            "scenario_badge": "👶 Baby Care Essentials",
            "why_suggested": "Complements your baby wipe reorder for complete skin hydration.",
            "cobuying_utility": "Use after cleansing with baby wipes to lock in 24-hour moisture and protect delicate infant skin from dryness.",
            "social_proof": "24 parents in DLF Phase 3 bought this this week"
        }
    elif any(k in cart_text for k in ["dog", "cat", "pet", "pedigree", "whiskas"]):
        return {
            "title": "Whiskas Wet Cat Food Ocean Fish (4 Pack)",
            "price": 195,
            "mrp": 220,
            "category": "Pet Care",
            "emoji": "🐱",
            "scenario_badge": "🐾 Pet Nutrition Booster",
            "why_suggested": "Complements your dry pet food reorder with wet gravy treats.",
            "cobuying_utility": "Mix wet gravy food with dry kibble to enhance meal palatability and ensure optimal hydration for your pet.",
            "social_proof": "19 pet owners in DLF Phase 3 bought this this week"
        }
    elif any(k in cart_text for k in ["avocado", "yogurt", "fruit", "veggie", "gourmet"]):
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
    else:
        return {
            "title": "Spigen 20W Fast Type-C Wall Charger Adapter",
            "price": 899,
            "mrp": 1499,
            "category": "Electronics & Tech",
            "emoji": "🔌",
            "scenario_badge": "⚡ Late-Night Work Power Utility",
            "why_suggested": "Essential fast-charge utility paired with your active work sprint beverages.",
            "cobuying_utility": "Power your phone from 0% to 50% in just 25 minutes while enjoying your energy drinks.",
            "social_proof": "42 residents in DLF Phase 3 bought this this week"
        }

# -----------------------------------------------------------------------------
# CLEAN SIDEBAR CONFIGURATION (ZERO FRONTEND API KEY DISPLAY)
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 📍 Location & User Profile")
    st.info("Location: DLF Phase 3, Gurgaon\n\n**Segment:** Metro Tech Professional\n\n**Delivery Promise:** ⚡ 10 Mins")
    st.divider()
    if st.button("🔄 Reset Simulation Demo"):
        st.session_state.cart = [
            {"id": "amul_milk", "name": "Amul Taaza T-Special Milk 1L", "category": "Dairy & Breakfast", "price": 72, "emoji": "🥛"}
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
