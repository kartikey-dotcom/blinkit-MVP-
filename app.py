"""
BlinkSmart: Zero-Risk First-Trial Shield Engine MVP
Streamlit App entrypoint with clean HTML rendering (newlines stripped to prevent Markdown code block bugs).
"""

import os
import time
import requests
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

# Load environment variables (.env / Streamlit secrets)
load_dotenv()

# Helper function to strip newlines and extra spaces so Streamlit's Markdown parser NEVER treats HTML as raw code
def clean_html(html_str):
    return " ".join(html_str.split())

# ==============================================================================
# PAGE CONFIGURATION & EXACT BLINKIT BRAND STYLING
# ==============================================================================
st.set_page_config(
    page_title="Blinkit - 8-10 Mins Delivery",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS matching the exact visual layout
st.markdown(clean_html("""
<style>
/* Reset & Background */
.stApp {
    background-color: #F4F6F8 !important;
    color: #1E293B;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
}

/* Hide Default Streamlit Header & Footer */
header[data-testid="stHeader"] { visibility: hidden; height: 0; }
footer { visibility: hidden; }
.block-container { padding-top: 0rem; padding-bottom: 5rem; max-width: 480px; }

/* Yellow Top Header */
.blinkit-header {
    background-color: #F7C200;
    padding: 14px 18px;
    margin-left: -1rem;
    margin-right: -1rem;
    margin-top: -1rem;
    margin-bottom: 14px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}
.header-logo {
    font-size: 1.6rem;
    font-weight: 900;
    color: #000000;
    letter-spacing: -0.5px;
}
.header-location {
    font-size: 0.8rem;
    font-weight: 700;
    color: #1E293B;
    display: flex;
    align-items: center;
    gap: 4px;
    margin-top: 2px;
}
.header-badge {
    background-color: #FFFFFF;
    color: #0C831F;
    font-size: 0.75rem;
    font-weight: 800;
    padding: 4px 10px;
    border-radius: 20px;
    display: flex;
    align-items: center;
    gap: 4px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

/* Card Wrapper */
.blinkit-card {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 16px;
    margin-bottom: 16px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    border: 1px solid #E2E8F0;
}
.card-label {
    font-size: 0.75rem;
    font-weight: 800;
    color: #64748B;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    margin-bottom: 12px;
}

/* AI Recommend Nudge Card */
.nudge-card-exact {
    background: #F0FDF4;
    border: 1.5px solid #A7F3D0;
    border-radius: 16px;
    padding: 16px;
    margin-bottom: 16px;
    position: relative;
}
.badge-discount {
    background-color: #F7C200;
    color: #000000;
    font-size: 0.68rem;
    font-weight: 900;
    padding: 3px 6px;
    border-radius: 4px;
    position: absolute;
    top: 12px;
    left: 12px;
    z-index: 2;
}
.badge-ai {
    background-color: #F7C200;
    color: #000000;
    font-size: 0.65rem;
    font-weight: 900;
    padding: 3px 8px;
    border-radius: 10px;
    position: absolute;
    top: 12px;
    right: 12px;
    z-index: 2;
}
.nudge-body {
    display: flex;
    gap: 12px;
    margin-top: 16px;
}
.nudge-img-container {
    width: 85px;
    height: 85px;
    background: #FFFFFF;
    border-radius: 12px;
    border: 1px solid #E2E8F0;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 4px;
    overflow: hidden;
}
.nudge-img-container img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 8px;
}
.nudge-title {
    font-size: 0.95rem;
    font-weight: 800;
    color: #0F172A;
    line-height: 1.25;
}
.nudge-rationale {
    font-size: 0.78rem;
    font-style: italic;
    color: #0C831F;
    font-weight: 600;
    margin-top: 3px;
}
.nudge-price-row {
    margin-top: 6px;
    display: flex;
    align-items: baseline;
    gap: 6px;
}
.nudge-price {
    font-size: 1.15rem;
    font-weight: 900;
    color: #0F172A;
}
.nudge-mrp {
    font-size: 0.8rem;
    color: #94A3B8;
    text-decoration: line-through;
}
.social-proof-row {
    display: flex;
    align-items: center;
    gap: 6px;
    margin-top: 6px;
    font-size: 0.72rem;
    color: #64748B;
    font-weight: 600;
}
.avatar-stack {
    display: flex;
}
.avatar-circle {
    width: 16px;
    height: 16px;
    border-radius: 50%;
    background-color: #CBD5E1;
    border: 1.5px solid #FFFFFF;
    margin-left: -5px;
}
.avatar-circle:first-child { margin-left: 0; }

.nudge-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 12px;
    padding-top: 8px;
}
.shield-applied-text {
    font-size: 0.78rem;
    font-weight: 800;
    color: #0C831F;
    display: flex;
    align-items: center;
    gap: 4px;
}

/* Bill Summary Rows */
.bill-row {
    display: flex;
    justify-content: space-between;
    font-size: 0.88rem;
    color: #64748B;
    margin-bottom: 8px;
}
.bill-row.grand-total {
    font-size: 1.15rem;
    font-weight: 900;
    color: #0F172A;
    border-top: 1px solid #F1F5F9;
    padding-top: 10px;
    margin-bottom: 0;
}

/* Info Shield Box */
.info-shield-box {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 12px 14px;
    display: flex;
    gap: 10px;
    align-items: center;
    margin-bottom: 20px;
}
.info-icon {
    color: #0C831F;
    font-size: 1.2rem;
    font-weight: bold;
}
.info-text {
    font-size: 0.75rem;
    color: #94A3B8;
    line-height: 1.3;
}
</style>
"""), unsafe_allow_html=True)

# Direct Image URLs for authentic product thumbnails
PRODUCT_IMAGES = {
    "Blue Tokai Coffee (250g)": "https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=200",
    "Amul Gold Milk (1L)": "https://images.unsplash.com/photo-1563636619-e9143da7973b?w=200",
    "InstaCuppa Electric Coffee Frother": "https://images.unsplash.com/photo-1517668808822-9e4288246ede?w=200",
    "boAt Airdopes 141": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=200",
    "Minimalist 10% Vitamin C Face Serum 30ml": "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=200",
    "Fresh Imported Hass Avocado (2 pcs)": "https://images.unsplash.com/photo-1523049673857-eb18f1d7b578?w=200",
    "Fresh Hybrid Tomatoes 500g": "https://images.unsplash.com/photo-1592924357228-91a4daadcfea?w=200",
    "Pigeon 1.5L Electric Kettle": "https://images.unsplash.com/photo-1594213114663-d94db9b17126?w=200",
    "Pedigree Adult Dry Dog Food 1.2kg": "https://images.unsplash.com/photo-1589924691995-400dc9ecc119?w=200",
    "Pampers Fresh Clean Baby Wipes (80 sheets)": "https://images.unsplash.com/photo-1519689680058-324335c77eba?w=200"
}
DEFAULT_IMAGE = "https://images.unsplash.com/photo-1542838132-92c53300491e?w=200"

# ==============================================================================
# DATASET LOADING
# ==============================================================================
@st.cache_data
def load_catalog():
    csv_file = "blinkit_catalog.csv"
    if os.path.exists(csv_file):
        try:
            return pd.read_csv(csv_file)
        except Exception:
            pass
    return pd.DataFrame([
        {"id": "GS-101", "name": "Blue Tokai Coffee (250g)", "category": "Gourmet & Specialty", "price": 499, "mrp": 550, "emoji": "☕", "subtext": "Roasted Arabica"},
        {"id": "DB-001", "name": "Amul Gold Milk (1L)", "category": "Dairy & Breakfast", "price": 66, "mrp": 66, "emoji": "🥛", "subtext": "Full Cream"},
        {"id": "HK-001", "name": "InstaCuppa Electric Coffee Frother", "category": "Home & Kitchen", "price": 799, "mrp": 1200, "emoji": "☕", "subtext": "Frother Wand"},
        {"id": "ET-002", "name": "boAt Airdopes 141", "category": "Electronics & Tech", "price": 1299, "mrp": 2990, "emoji": "🎧", "subtext": "Wireless Earbuds"},
        {"id": "BP-001", "name": "Minimalist 10% Vitamin C Face Serum 30ml", "category": "Beauty & Personal Care", "price": 664, "mrp": 699, "emoji": "🧴", "subtext": "Face Serum"}
    ])

catalog_df = load_catalog()

# ==============================================================================
# SESSION STATE INITIALIZATION
# ==============================================================================
if "cart" not in st.session_state:
    st.session_state.cart = [
        {"id": "GS-101", "name": "Blue Tokai Coffee (250g)", "subtext": "Roasted Arabica", "price": 499, "mrp": 550, "emoji": "☕", "qty": 1, "category": "Gourmet & Specialty"},
        {"id": "DB-001", "name": "Amul Gold Milk (1L)", "subtext": "Full Cream", "price": 66, "mrp": 66, "emoji": "🥛", "qty": 1, "category": "Dairy & Breakfast"}
    ]

if "nudge_added" not in st.session_state:
    st.session_state.nudge_added = False

if "order_placed" not in st.session_state:
    st.session_state.order_placed = False

if "exchange_requested" not in st.session_state:
    st.session_state.exchange_requested = False

# ==============================================================================
# AI NUDGE RECOMMENDATION ENGINE
# ==============================================================================
def get_ai_cross_sell_nudge(cart_items, api_key):
    if not cart_items:
        return None

    cart_categories = list(set(item.get("category", "") for item in cart_items))
    cart_names = [item["name"] for item in cart_items]

    unexplored_df = catalog_df[~catalog_df["category"].isin(cart_categories)]
    if unexplored_df.empty:
        unexplored_df = catalog_df

    if api_key and len(api_key.strip()) > 10:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key.strip()}"
            prompt = f"""
You are Blinkit's AI Cross-Sell Engine.
Customer Cart: {', '.join(cart_names)}.
Recommend ONE product from unexplored categories: {unexplored_df['name'].tolist()}.
Write 1 short sentence (max 12 words) pairing rationale.
Format JSON: {{"recommended_product": "Exact Product Name", "rationale": "Your sentence."}}
"""
            res = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=3)
            if res.status_code == 200:
                result_json = res.json()
                text = result_json["candidates"][0]["content"]["parts"][0]["text"]
                import json, re
                match = re.search(r'\{.*\}', text, re.DOTALL)
                if match:
                    parsed = json.loads(match.group())
                    rec_name = parsed.get("recommended_product")
                    rationale = parsed.get("rationale")
                    rec_item = catalog_df[catalog_df["name"] == rec_name]
                    if not rec_item.empty:
                        return rec_item.iloc[0].to_dict(), rationale
        except Exception:
            pass

    if any("coffee" in name.lower() or "milk" in name.lower() for name in cart_names):
        rec_row = catalog_df[catalog_df["name"].str.contains("Frother", case=False, na=False)].iloc[0].to_dict()
        return rec_row, "Pairs with your Blue Tokai coffee..."

    rec_row = unexplored_df.iloc[0].to_dict()
    return rec_row, "Recommended non-grocery upgrade for your cart!"

# ==============================================================================
# TOP HEADER BAR
# ==============================================================================
st.markdown(clean_html("""
<div class="blinkit-header">
    <div>
        <div class="header-logo">blinkit</div>
        <div class="header-location">📍 DLF Phase 3, Gurgaon</div>
    </div>
    <div style="display: flex; align-items: center; gap: 10px;">
        <div class="header-badge">
            <span style="font-weight: 900;">⚡ 8-10 MINS</span>
        </div>
        <div style="width: 28px; height: 28px; border-radius: 50%; background: #000; color: #FFF; display: flex; align-items: center; justify-content: center; font-size: 0.8rem; font-weight: bold;">
            👤
        </div>
    </div>
</div>
"""), unsafe_allow_html=True)

# ==============================================================================
# GLOBAL SEARCH BAR
# ==============================================================================
with st.expander("🔍 Search & Add Any Product from 12 Blinkit Categories", expanded=False):
    search_query = st.text_input("Type product name (e.g., 'Milk', 'Avocado', 'Charger', 'Serum'):", "")
    
    if search_query.strip():
        search_matches = catalog_df[catalog_df["name"].str.contains(search_query, case=False, na=False)]
    else:
        search_matches = catalog_df

    selected_sku_str = st.selectbox("Select matching product:", [f"{r['emoji']} {r['name']} — ₹{r['price']} ({r['category']})" for _, r in search_matches.iterrows()])
    
    if st.button("➕ Add Selected Item to Cart", use_container_width=True):
        idx = [f"{r['emoji']} {r['name']} — ₹{r['price']} ({r['category']})" for _, r in search_matches.iterrows()].index(selected_sku_str)
        matched_row = search_matches.iloc[idx].to_dict()
        matched_row["qty"] = 1
        st.session_state.cart.append(matched_row)
        st.toast(f"Added {matched_row['name']} to cart!", icon="🛒")
        st.rerun()

# ==============================================================================
# MAIN CHECKOUT VIEW VS ORDER PLACED VIEW
# ==============================================================================
if not st.session_state.order_placed:

    # SIDEBAR CONTROLS
    with st.sidebar:
        st.markdown("### ⚙️ Demo Controls & AI Keys")
        st.info("📍 **DLF Phase 3, Gurgaon**\n\n⚡ Served by *Dark Store #104*")
        
        secret_key = ""
        try:
            secret_key = st.secrets.get("GEMINI_API_KEY", "")
        except Exception:
            pass
        env_gemini_key = secret_key or os.getenv("GEMINI_API_KEY", "")
        api_key_input = st.text_input("Gemini API Key (Optional)", value=env_gemini_key, type="password")

        st.markdown("---")
        if st.button("🔄 Reset Cart to Initial State"):
            st.session_state.cart = [
                {"id": "GS-101", "name": "Blue Tokai Coffee (250g)", "subtext": "Roasted Arabica", "price": 499, "mrp": 550, "emoji": "☕", "qty": 1, "category": "Gourmet & Specialty"},
                {"id": "DB-001", "name": "Amul Gold Milk (1L)", "subtext": "Full Cream", "price": 66, "mrp": 66, "emoji": "🥛", "qty": 1, "category": "Dairy & Breakfast"}
            ]
            st.session_state.nudge_added = False
            st.session_state.order_placed = False
            st.session_state.exchange_requested = False
            st.rerun()

    # --------------------------------------------------------------------------
    # CARD 1: YOUR BASKET (NATIVE STREAMLIT CONTAINER + COLUMNS)
    # --------------------------------------------------------------------------
    with st.container(border=True):
        st.caption("YOUR BASKET")

        if not st.session_state.cart:
            st.info("Your basket is empty. Use the search bar above to add items!")
        else:
            for idx, item in enumerate(st.session_state.cart):
                img_url = PRODUCT_IMAGES.get(item["name"], DEFAULT_IMAGE)
                col_img, col_info, col_btn = st.columns([0.2, 0.55, 0.25])
                
                with col_img:
                    st.image(img_url, width=48)
                    
                with col_info:
                    st.markdown(f"**{item['name']}**")
                    st.caption(item.get("subtext", item.get("category", "Fresh Stock")))
                    st.markdown(f"**₹{item['price']}**")
                    
                with col_btn:
                    c1, c2, c3 = st.columns([1,1,1])
                    with c1:
                        if st.button("−", key=f"minus_{idx}"):
                            if item["qty"] > 1:
                                item["qty"] -= 1
                            else:
                                st.session_state.cart.pop(idx)
                            st.rerun()
                    with c2:
                        st.markdown(f"<div style='text-align:center; font-weight:800; padding-top:4px;'>{item['qty']}</div>", unsafe_allow_html=True)
                    with c3:
                        if st.button("+", key=f"plus_{idx}"):
                            item["qty"] += 1
                            st.rerun()

    # --------------------------------------------------------------------------
    # CARD 2: AI RECOMMEND / BLINKSMART NUDGE CARD
    # --------------------------------------------------------------------------
    if not st.session_state.nudge_added and st.session_state.cart:
        nudge_data = get_ai_cross_sell_nudge(st.session_state.cart, api_key_input)
        if nudge_data:
            nudge_item, rationale = nudge_data
            nudge_img = PRODUCT_IMAGES.get(nudge_item["name"], DEFAULT_IMAGE)
            discount_pct = int(((nudge_item.get("mrp", nudge_item["price"]) - nudge_item["price"]) / nudge_item.get("mrp", nudge_item["price"])) * 100) if nudge_item.get("mrp", 0) > nudge_item["price"] else 33
            
            # Using clean_html to eliminate raw code rendering
            nudge_html = clean_html(f"""
            <div class="nudge-card-exact">
                <span class="badge-discount">{discount_pct}% OFF</span>
                <span class="badge-ai">AI RECOMMEND</span>
                <div class="nudge-body">
                    <div class="nudge-img-container">
                        <img src="{nudge_img}" />
                    </div>
                    <div style="flex:1;">
                        <div class="nudge-title">{nudge_item['name']}</div>
                        <div class="nudge-rationale">"{rationale}"</div>
                        <div class="nudge-price-row">
                            <span class="nudge-price">₹{nudge_item['price']}</span>
                            <span class="nudge-mrp">₹{nudge_item.get('mrp', nudge_item['price'] + 400)}</span>
                        </div>
                        <div class="social-proof-row">
                            <div class="avatar-stack">
                                <div class="avatar-circle"></div>
                                <div class="avatar-circle"></div>
                            </div>
                            <span>32 neighbors in DLF Phase 3 bought this</span>
                        </div>
                    </div>
                </div>
                <div class="nudge-footer">
                    <div class="shield-applied-text">
                        🛡️ Zero-Risk Shield Applied
                    </div>
                </div>
            </div>
            """)
            st.markdown(nudge_html, unsafe_allow_html=True)
            
            if st.button(f"+ Add {nudge_item['name']} to Order", key="add_nudge_btn", type="primary", use_container_width=True):
                nudge_item_cart = dict(nudge_item)
                nudge_item_cart["qty"] = 1
                st.session_state.cart.append(nudge_item_cart)
                st.session_state.nudge_added = True
                st.toast(f"Added {nudge_item['name']} with Zero-Risk Shield!", icon="🛡️")
                st.rerun()

    # --------------------------------------------------------------------------
    # CARD 3: BILL SUMMARY
    # --------------------------------------------------------------------------
    item_total = sum(i["price"] * i["qty"] for i in st.session_state.cart)
    delivery_fee = 0
    handling_fee = 15
    grand_total = item_total + delivery_fee + handling_fee

    bill_html = clean_html(f"""
    <div class="blinkit-card">
        <div class="card-label">BILL SUMMARY</div>
        <div class="bill-row">
            <span>Item Total</span>
            <span style="color: #0F172A; font-weight: 700;">₹{item_total}</span>
        </div>
        <div class="bill-row">
            <span>Delivery Partner Fee</span>
            <span style="color: #0C831F; font-weight: 800;">FREE</span>
        </div>
        <div class="bill-row">
            <span>Handling Fee</span>
            <span style="color: #0F172A; font-weight: 700;">₹{handling_fee}</span>
        </div>
        <div class="bill-row grand-total">
            <span>Grand Total</span>
            <span>₹{grand_total}</span>
        </div>
    </div>
    """)
    st.markdown(bill_html, unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # CARD 4: INFORMATION SHIELD BOX
    # --------------------------------------------------------------------------
    info_html = clean_html("""
    <div class="info-shield-box">
        <div class="info-icon">ⓘ</div>
        <div class="info-text">
            Don't like the non-grocery item? Request a doorstep exchange within 10 minutes of delivery. No questions asked.
        </div>
    </div>
    """)
    st.markdown(info_html, unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # FIXED BOTTOM CHECKOUT BAR
    # --------------------------------------------------------------------------
    col_pay_left, col_pay_right = st.columns([0.4, 0.6])
    
    with col_pay_left:
        st.markdown(f"### ₹{grand_total}")
        st.caption("VIEW BILL ^")

    with col_pay_right:
        if st.button("Pay via Face ID 🔲", type="primary", use_container_width=True):
            st.session_state.order_placed = True
            st.rerun()

# ==============================================================================
# POST-PURCHASE 10-MINUTE EXCHANGE SIMULATION SCREEN
# ==============================================================================
else:
    st.balloons()
    success_html = clean_html("""
    <div style="background-color: #064E3B; border: 2px solid #10B981; border-radius: 16px; padding: 24px; text-align: center; margin-bottom: 20px; color: #FFFFFF;">
        <h2 style="margin: 0; color: #FFFFFF;">🎉 Order Placed Successfully!</h2>
        <p style="color: #A7F3D0; font-size: 1rem; margin-top: 4px;">
            Arriving in <strong>8-10 Minutes</strong> • Dark Store #104 (Indiranagar)
        </p>
    </div>
    """)
    st.markdown(success_html, unsafe_allow_html=True)

    shield_html = clean_html("""
    <div style="background: linear-gradient(135deg, #1E1B4B 0%, #312E81 100%); border: 2px solid #6366F1; border-radius: 16px; padding: 20px; color: #FFFFFF; margin-bottom: 20px;">
        <h3 style="color: #A5B4FC; margin-top: 0;">🛡️ Active 10-Minute First-Trial Safety Net</h3>
        <p style="color: #E0E7FF; font-size: 0.9rem;">
            Your order is protected by Blinkit's Zero-Risk Shield. Need an exchange or return? Request a 1-click doorstep rider exchange within 10 minutes!
        </p>
        <div style="font-family: monospace; font-size: 2rem; font-weight: 900; color: #F7C200; background-color: #0F172A; padding: 10px; border-radius: 10px; text-align: center;">
            ⏳ 09:59 (Shield Protection Active)
        </div>
    </div>
    """)
    st.markdown(shield_html, unsafe_allow_html=True)

    if st.button("🚨 Request 10-Minute Doorstep Exchange", type="primary", use_container_width=True):
        st.session_state.exchange_requested = True

    if st.session_state.exchange_requested:
        st.info("📍 **Locating nearest Dark Store rider...** (Rider: Ramesh Kumar)")
        time.sleep(1)
        st.warning("🛵 **Rider Ramesh Kumar dispatched to DLF Phase 3!**")
        time.sleep(1)
        st.success("🎉 **Rider arrived at doorstep! Replacement product handed over.**")

    st.markdown("---")
    if st.button("🛒 Return to Storefront", use_container_width=True):
        st.session_state.order_placed = False
        st.session_state.exchange_requested = False
        st.rerun()
