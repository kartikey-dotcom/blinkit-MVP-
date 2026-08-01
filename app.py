import streamlit as st
import json
import time
import requests
import pandas as pd
import os

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION & BLINKIT BRAND STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="BlinkSmart Zero-Risk Shield MVP",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main { background-color: #0f172a; }
    .stApp { background-color: #0f172a; color: #f8fafc; }
    
    .blinkit-badge {
        background-color: #f7c200;
        color: #000000;
        font-weight: 800;
        padding: 4px 12px;
        border-radius: 6px;
        font-family: 'Poppins', sans-serif;
        font-size: 16px;
        display: inline-block;
    }
    
    .nudge-card {
        background: linear-gradient(135deg, #0f172a 0%, #064e3b 50%, #0f172a 100%);
        border: 1.5px solid #10b981;
        border-radius: 16px;
        padding: 18px;
        margin-top: 14px;
        margin-bottom: 14px;
        box-shadow: 0 10px 25px rgba(16, 185, 129, 0.2);
    }
    
    .nudge-tag {
        background-color: rgba(16, 185, 129, 0.2);
        color: #34d399;
        border: 1px solid rgba(52, 211, 153, 0.3);
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
    }

    .scenario-badge {
        background-color: #f7c200;
        color: #0f172a;
        font-weight: 800;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 11px;
        display: inline-block;
    }
    
    .rationale-box {
        background-color: rgba(30, 41, 59, 0.85);
        border: 1px solid rgba(51, 65, 85, 0.8);
        border-radius: 12px;
        padding: 12px;
        margin-top: 10px;
        margin-bottom: 12px;
    }
    
    .shield-badge {
        background-color: #fef08a;
        color: #854d0e;
        font-weight: 700;
        padding: 2px 8px;
        border-radius: 4px;
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
""", unsafe_allow_html=True)

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
# GEMINI API / LOCAL FALLBACK RECOMMENDATION LOGIC
# -----------------------------------------------------------------------------
def get_blinksmart_recommendation(cart_items, api_key=""):
    cart_names = [item["name"] for item in cart_items]
    cart_categories = [item.get("category", "") for item in cart_items]
    cart_text = " ".join(cart_names).lower() + " " + " ".join(cart_categories).lower()
    
    # Attempt Live Gemini API Call if key provided
    if api_key:
        try:
            endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            prompt = f"""
            Act as the BlinkSmart Recommendation Engine for Blinkit quick commerce.
            Active Cart Items: {cart_names}
            Cart Categories: {cart_categories}
            Location: DLF Phase 3, Gurgaon.
            
            Recommend strictly ONE high-margin non-grocery SKU (Electronics & Tech, Beauty & Personal Care, Home & Kitchen, Baby Care, or Pet Care) that logically and contextually pairs with this active cart mix.
            
            CRITICAL REQUIREMENT: You MUST provide a real-world scenario explaining WHY this product was suggested and HOW buying this recommended product along with the cart items creates a useful co-buying scenario.
            
            Respond strictly in valid JSON format:
            {{
                "title": "Portronics Adjustable Desktop Phone Stand",
                "price": 299,
                "mrp": 699,
                "category": "Electronics & Tech",
                "emoji": "📱",
                "scenario_badge": "📺 Hands-Free Binge Watching",
                "why_suggested": "Matched to your snack & drink selection for desk snacking.",
                "cobuying_utility": "Prop your phone hands-free to watch YouTube or movies while eating Doritos without getting cheese dust or grease on your touchscreen.",
                "social_proof": "48 snack lovers in DLF Phase 3 bought this this week"
            }}
            """
            response = requests.post(endpoint, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=5)
            if response.status_code == 200:
                data = response.json()
                text_content = data['candidates'][0]['content']['parts'][0]['text']
                clean_json = text_content.replace("```json", "").replace("```", "").strip()
                return json.loads(clean_json)
        except Exception:
            pass

    # Universal Rule Engine for Any Cart Combo
    if "doritos" in cart_text or "lays" in cart_text or "chips" in cart_text or "munchies" in cart_text or "snack" in cart_text:
        return {
            "title": "Portronics Adjustable Multi-Angle Desktop Phone Stand",
            "price": 299,
            "mrp": 699,
            "category": "Electronics & Tech",
            "emoji": "📱",
            "scenario_badge": "📺 Hands-Free Binge Watching",
            "why_suggested": "Pairs with your snack & munchies selection for desk entertainment.",
            "cobuying_utility": "Prop your phone hands-free to watch YouTube or sports while eating Doritos, keeping your touchscreen clean from cheese dust and grease.",
            "social_proof": "48 snack lovers in DLF Phase 3 bought this this week"
        }
    elif "baby" in cart_text or "wipes" in cart_text or "pampers" in cart_text:
        return {
            "title": "Sebamed Baby Gentle Body Lotion 200ml",
            "price": 540,
            "mrp": 600,
            "category": "Baby Care",
            "emoji": "🍼",
            "scenario_badge": "👶 Baby Care Essentials",
            "why_suggested": "Complements your baby wipe reorder for complete skin care.",
            "cobuying_utility": "Use after cleansing with baby wipes to lock in 24-hour hydration and protect delicate infant skin from dryness.",
            "social_proof": "24 parents in DLF Phase 3 bought this this week"
        }
    elif "dog" in cart_text or "cat" in cart_text or "pet" in cart_text or "pedigree" in cart_text:
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
    elif "coffee" in cart_text or "milk" in cart_text or "breakfast" in cart_text or "bread" in cart_text:
        return {
            "title": "InstaCuppa Electric Milk Frother & Hand Mixer",
            "price": 799,
            "mrp": 1200,
            "category": "Home & Kitchen",
            "emoji": "⚡",
            "scenario_badge": "☕ 15-Second Homemade Cafe Foam",
            "why_suggested": "Suggested to upgrade your Blue Tokai coffee & Amul milk basket.",
            "cobuying_utility": "Blend cold milk and espresso shots directly in your glass to create cafe-style thick, frothy lattes and iced frappes in 15 seconds.",
            "social_proof": "32 coffee lovers in DLF Phase 3 bought this this week"
        }
    elif "avocado" in cart_text or "yogurt" in cart_text or "gourmet" in cart_text:
        return {
            "title": "Minimalist 10% Vitamin C Face Serum (30ml)",
            "price": 664,
            "mrp": 699,
            "category": "Beauty & Personal Care",
            "emoji": "🧴",
            "scenario_badge": "✨ Clean Morning Skin Routine",
            "why_suggested": "Matches your organic gourmet food selection for wellness care.",
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
            "scenario_badge": "⚡ Desk & Late-Night Power Utility",
            "why_suggested": "Essential fast-charge utility paired with your active order.",
            "cobuying_utility": "Power your phone from 0% to 50% in just 25 minutes while enjoying your snacks and beverages.",
            "social_proof": "42 residents in DLF Phase 3 bought this this week"
        }

# -----------------------------------------------------------------------------
# SIDEBAR CONFIGURATION
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚙️ Engine Settings")
    secret_key = ""
    try:
        secret_key = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        pass
    env_key = secret_key or os.getenv("GEMINI_API_KEY", "")
    gemini_key = st.text_input("Gemini API Key (Optional)", value=env_key, type="password", help="Enter key to enable live LLM generation across all catalog items.")
    
    st.divider()
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
    st.markdown('<span class="blinkit-badge">blinkit</span>', unsafe_allow_html=True)
with col_loc:
    st.markdown("<div style='text-align:right; font-size:12px; color:#94a3b8;'>📍 DLF Phase 3, Gurgaon • <strong>10 Mins Delivery</strong></div>", unsafe_allow_html=True)

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
    
    st.markdown("""
        <div style='background-color:#064e3b; border: 1px solid #10b981; border-radius:12px; padding:16px; margin-bottom:16px;'>
            <div style='display:flex; justify-content:space-between; align-items:center;'>
                <span style='color:#34d399; font-weight:800; font-size:14px;'>🔰 First-Trial Safety Net Active</span>
                <span style='background-color:#022c22; color:#facc15; font-family:monospace; font-weight:bold; padding:2px 8px; border-radius:4px;'>09:59 MINS</span>
            </div>
            <p style='font-size:12px; color:#e2e8f0; margin-top:8px;'>
                Your trial item is covered under the 10-Minute Doorstep Exchange Guarantee. Inspect the unit upon arrival!
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.exchange_triggered:
        if st.button("🧪 Test 10-Minute Doorstep Rider Exchange Request"):
            st.session_state.exchange_triggered = True
            st.rerun()
    else:
        st.warning("⚡ Doorstep Exchange Dispatched!")
        st.markdown("""
            <div style='background-color:#1e293b; border:1px solid #334155; border-radius:10px; padding:12px; font-size:12px;'>
                <div style='font-weight:bold; color:#f8fafc; margin-bottom:4px;'>🛵 Live Exchange Status Log:</div>
                <div style='color:#34d399;'>• Exchange request logged via automated chatbot.</div>
                <div style='color:#cbd5e1;'>• Rider Ramesh Kumar dispatched with fresh sealed unit from dark store.</div>
                <div style='color:#cbd5e1;'>• Estimated Doorstep Swap Time: <strong>7 Minutes</strong>.</div>
            </div>
        """, unsafe_allow_html=True)

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
    
    with col_prod:
        selected_title = st.selectbox("Select Product:", list(product_map.keys()), label_visibility="collapsed")
        
    with col_btn:
        if st.button("+ Add Item"):
            item_to_add = product_map[selected_title]
            st.session_state.cart.append(item_to_add)
            st.rerun()

    # Active Cart List
    st.markdown("#### 🧺 Active Grocery Basket")
    subtotal = 0
    
    for idx, item in enumerate(st.session_state.cart):
        subtotal += item["price"]
        col_item, col_del = st.columns([5, 1])
        with col_item:
            st.markdown(f"""
                <div style='display:flex; justify-content:space-between; align-items:center; background-color:#1e293b; border:1px solid #334155; border-radius:10px; padding:8px 14px;'>
                    <div>
                        <span style='font-size:16px;'>{item.get('emoji', '🛒')}</span>
                        <strong style='font-size:13px; color:#f8fafc; margin-left:8px;'>{item['name']}</strong>
                        <span style='font-size:10px; color:#94a3b8; margin-left:6px;'>({item.get('category', 'Grocery')})</span>
                    </div>
                    <span style='font-weight:bold; font-size:13px; color:#f8fafc;'>₹{item['price']}</span>
                </div>
            """, unsafe_allow_html=True)
        with col_del:
            if st.button("❌", key=f"del_{idx}"):
                st.session_state.cart.pop(idx)
                st.rerun()

    # -------------------------------------------------------------------------
    # BLINKSMART CONTEXTUAL AI NUDGE CARD WITH CLEAR CO-BUYING REASONING
    # -------------------------------------------------------------------------
    rec = get_blinksmart_recommendation(st.session_state.cart, gemini_key)
    
    st.markdown(f"""
        <div class="nudge-card">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                <span class="nudge-tag">✨ BlinkSmart Contextual Nudge</span>
                <span class="scenario-badge">{rec['scenario_badge']}</span>
            </div>
            
            <div class="rationale-box">
                <div style="font-size:11px; color:#34d399; font-weight:700; margin-bottom:2px;">🎯 WHY SUGGESTED:</div>
                <div style="font-size:12px; color:#f8fafc; margin-bottom:8px;">{rec['why_suggested']}</div>
                
                <div style="font-size:11px; color:#facc15; font-weight:700; margin-bottom:2px;">🤝 CO-BUYING UTILITY:</div>
                <div style="font-size:12px; color:#cbd5e1; line-height:1.4;">"{rec['cobuying_utility']}"</div>
            </div>

            <div style="background-color:#1e293b; border:1px solid #334155; border-radius:12px; padding:12px; display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <div style="font-size:18px; margin-bottom:2px;">{rec['emoji']} <strong style="font-size:13px; color:#ffffff;">{rec['title']}</strong></div>
                    <div style="font-size:11px; color:#34d399; font-weight:600;">🔰 100% Brand Authenticity Seal</div>
                    <div style="margin-top:4px;">
                        <span style="font-size:14px; font-weight:800; color:#facc15;">₹{rec['price']}</span>
                        <span style="font-size:11px; color:#94a3b8; text-decoration:line-through; margin-left:4px;">₹{rec['mrp']}</span>
                    </div>
                </div>
            </div>
            <div style="margin-top:12px; font-size:12px; color:#cbd5e1; display:flex; justify-content:space-between; align-items:center;">
                <span>👥 <strong>{rec['social_proof']}</strong></span>
                <span class="shield-badge">🔰 1st Trial Shield Active</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
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
