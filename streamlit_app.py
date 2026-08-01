"""
BlinkSmart: Zero-Risk First-Trial Shield Engine MVP
Streamlit App entrypoint for Streamlit Cloud Deployment.
"""

import os
import time
import requests
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

# Load environment variables (.env / Streamlit secrets)
load_dotenv()

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
st.markdown("""
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
        margin-bottom: 16px;
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

    /* Basket Item Row */
    .basket-item {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 10px 0;
        border-bottom: 1px solid #F1F5F9;
    }
    .basket-item:last-child {
        border-bottom: none;
    }
    .item-img {
        width: 54px;
        height: 54px;
        border-radius: 8px;
        object-fit: contain;
        background-color: #F8FAFC;
        border: 1px solid #F1F5F9;
        margin-right: 12px;
    }
    .item-details {
        flex: 1;
    }
    .item-title {
        font-size: 0.92rem;
        font-weight: 700;
        color: #1E293B;
        line-height: 1.2;
    }
    .item-subtext {
        font-size: 0.75rem;
        color: #94A3B8;
        margin-top: 2px;
    }
    .item-price {
        font-size: 0.95rem;
        font-weight: 800;
        color: #0F172A;
        margin-top: 4px;
    }
    .stepper-btn {
        background-color: #0C831F;
        color: #FFFFFF;
        border-radius: 8px;
        padding: 6px 14px;
        font-size: 0.9rem;
        font-weight: 800;
        display: flex;
        align-items: center;
        gap: 12px;
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
        width: 90px;
        height: 90px;
        background: #FFFFFF;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 6px;
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
        margin-top: 14px;
        padding-top: 10px;
    }
    .shield-applied-text {
        font-size: 0.78rem;
        font-weight: 800;
        color: #0C831F;
        display: flex;
        align-items: center;
        gap: 4px;
    }
    .btn-add-nudge {
        background-color: #FFFFFF;
        color: #0C831F;
        border: 2px solid #0C831F;
        border-radius: 8px;
        padding: 6px 18px;
        font-size: 0.88rem;
        font-weight: 800;
        cursor: pointer;
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
        margin-bottom: 24px;
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

    /* Fixed Sticky Footer */
    .fixed-bottom-bar {
        position: fixed;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 100%;
        max-width: 480px;
        background: #FFFFFF;
        border-top: 1px solid #E2E8F0;
        padding: 12px 16px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        z-index: 999;
        box-shadow: 0 -4px 12px rgba(0,0,0,0.05);
    }
    .pay-btn-exact {
        background-color: #0C831F;
        color: #FFFFFF;
        border-radius: 12px;
        padding: 12px 24px;
        font-size: 1.05rem;
        font-weight: 800;
        border: none;
        display: flex;
        align-items: center;
        gap: 8px;
        cursor: pointer;
    }
</style>
""", unsafe_allow_html=True)

# Helper SVG Image creator for clear UI previews
def get_svg_url(emoji, bg="#FFFFFF"):
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100">
    <rect width="100" height="100" fill="{bg}" rx="12"/>
    <text x="50%" y="55%" dominant-baseline="central" text-anchor="middle" font-size="45">{emoji}</text>
    </svg>"""
    return f"data:image/svg+xml;utf8,{requests.utils.quote(svg)}"

# ==============================================================================
# SESSION STATE INITIALIZATION
# ==============================================================================
if "cart" not in st.session_state:
    st.session_state.cart = [
        {"id": "GS-101", "name": "Blue Tokai Coffee (250g)", "subtext": "Roasted Arabica", "price": 499, "mrp": 550, "emoji": "☕", "qty": 1},
        {"id": "DB-001", "name": "Amul Gold Milk (1L)", "subtext": "Full Cream", "price": 66, "mrp": 66, "emoji": "🥛", "qty": 1}
    ]

if "nudge_added" not in st.session_state:
    st.session_state.nudge_added = False

if "order_placed" not in st.session_state:
    st.session_state.order_placed = False

if "exchange_requested" not in st.session_state:
    st.session_state.exchange_requested = False

# ==============================================================================
# TOP HEADER BAR (EXACT DESIGN MATCH)
# ==============================================================================
st.markdown("""
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
""", unsafe_allow_html=True)

# ==============================================================================
# MAIN CHECKOUT VIEW VS ORDER PLACED VIEW
# ==============================================================================
if not st.session_state.order_placed:

    # --------------------------------------------------------------------------
    # SIDEBAR CONTROL FOR TESTING & REPOSITORIES
    # --------------------------------------------------------------------------
    with st.sidebar:
        st.markdown("### ⚙️ Demo Controls")
        st.info("📍 **DLF Phase 3, Gurgaon**\n\n⚡ Served by *Dark Store #104*")
        
        # Read API key from Streamlit Secrets or Environment Variable
        secret_key = ""
        try:
            secret_key = st.secrets.get("GEMINI_API_KEY", "")
        except Exception:
            pass
        env_gemini_key = secret_key or os.getenv("GEMINI_API_KEY", "")
        api_key_input = st.text_input("Gemini API Key (Optional)", value=env_gemini_key, type="password")

        st.markdown("---")
        st.markdown("#### Basket Modification")
        if st.button("➕ Add Test Coffee SKU"):
            st.session_state.cart.append({"id": "GS-101", "name": "Blue Tokai Coffee (250g)", "subtext": "Roasted Arabica", "price": 499, "mrp": 550, "emoji": "☕", "qty": 1})
            st.rerun()
            
        if st.button("🔄 Reset Basket"):
            st.session_state.cart = [
                {"id": "GS-101", "name": "Blue Tokai Coffee (250g)", "subtext": "Roasted Arabica", "price": 499, "mrp": 550, "emoji": "☕", "qty": 1},
                {"id": "DB-001", "name": "Amul Gold Milk (1L)", "subtext": "Full Cream", "price": 66, "mrp": 66, "emoji": "🥛", "qty": 1}
            ]
            st.session_state.nudge_added = False
            st.session_state.order_placed = False
            st.session_state.exchange_requested = False
            st.rerun()

    # --------------------------------------------------------------------------
    # CARD 1: YOUR BASKET
    # --------------------------------------------------------------------------
    st.markdown('<div class="blinkit-card"><div class="card-label">YOUR BASKET</div>', unsafe_allow_html=True)

    for idx, item in enumerate(st.session_state.cart):
        img_url = get_svg_url(item["emoji"], "#F8FAFC")
        col_img, col_info, col_btn = st.columns([0.2, 0.55, 0.25])
        
        with col_img:
            st.image(img_url, width=50)
            
        with col_info:
            st.markdown(f"""
            <div class="item-title">{item['name']}</div>
            <div class="item-subtext">{item.get('subtext', 'Fresh Stock')}</div>
            <div class="item-price">₹{item['price']}</div>
            """, unsafe_allow_html=True)
            
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
                st.markdown(f"<div style='text-align:center; font-weight:800; margin-top:4px;'>{item['qty']}</div>", unsafe_allow_html=True)
            with c3:
                if st.button("+", key=f"plus_{idx}"):
                    item["qty"] += 1
                    st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # CARD 2: AI RECOMMEND / BLINKSMART NUDGE CARD
    # --------------------------------------------------------------------------
    if not st.session_state.nudge_added:
        frother_img = get_svg_url("☕", "#FFFFFF")
        
        st.markdown(f"""
        <div class="nudge-card-exact">
            <span class="badge-discount">33% OFF</span>
            <span class="badge-ai">AI RECOMMEND</span>
            
            <div class="nudge-body">
                <div class="nudge-img-container">
                    <img src="{frother_img}" width="65" />
                </div>
                <div style="flex:1;">
                    <div class="nudge-title">InstaCuppa Electric Coffee Frother</div>
                    <div class="nudge-rationale">"Pairs with your Blue Tokai coffee..."</div>
                    <div class="nudge-price-row">
                        <span class="nudge-price">₹799</span>
                        <span class="nudge-mrp">₹1,200</span>
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
        """, unsafe_allow_html=True)
        
        if st.button("+ Add Frother to Order", key="add_nudge_btn", type="primary", use_container_width=True):
            st.session_state.cart.append({
                "id": "HK-001",
                "name": "InstaCuppa Electric Coffee Frother",
                "subtext": "Frother Wand",
                "price": 799,
                "mrp": 1200,
                "emoji": "☕",
                "qty": 1
            })
            st.session_state.nudge_added = True
            st.toast("Added InstaCuppa Coffee Frother with Zero-Risk Shield!", icon="🛡️")
            st.rerun()

    # --------------------------------------------------------------------------
    # CARD 3: BILL SUMMARY
    # --------------------------------------------------------------------------
    item_total = sum(i["price"] * i["qty"] for i in st.session_state.cart)
    delivery_fee = 0
    handling_fee = 15
    grand_total = item_total + delivery_fee + handling_fee

    st.markdown(f"""
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
    """, unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # CARD 4: INFORMATION NUDGE / SHIELD EXPANDER
    # --------------------------------------------------------------------------
    st.markdown("""
    <div class="info-shield-box">
        <div class="info-icon">ⓘ</div>
        <div class="info-text">
            Don't like the frother? Request a doorstep exchange within 10 minutes of delivery. No questions asked.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # FIXED BOTTOM CHECKOUT BAR
    # --------------------------------------------------------------------------
    col_pay_left, col_pay_right = st.columns([0.4, 0.6])
    
    with col_pay_left:
        st.markdown(f"""
        <div style="padding-top: 4px;">
            <div style="font-size: 1.3rem; font-weight: 900; color: #0F172A;">₹{grand_total}</div>
            <div style="font-size: 0.68rem; font-weight: 800; color: #0C831F; text-transform: uppercase;">VIEW BILL ^</div>
        </div>
        """, unsafe_allow_html=True)

    with col_pay_right:
        if st.button("Pay via Face ID 🔲", type="primary", use_container_width=True):
            st.session_state.order_placed = True
            st.rerun()

# ==============================================================================
# POST-PURCHASE 10-MINUTE EXCHANGE SIMULATION SCREEN
# ==============================================================================
else:
    st.balloons()
    st.markdown("""
    <div style="background-color: #064E3B; border: 2px solid #10B981; border-radius: 16px; padding: 24px; text-align: center; margin-bottom: 20px; color: #FFFFFF;">
        <h2 style="margin: 0; color: #FFFFFF;">🎉 Order Placed Successfully!</h2>
        <p style="color: #A7F3D0; font-size: 1rem; margin-top: 4px;">
            Arriving in <strong>8-10 Minutes</strong> • Dark Store #104 (Indiranagar)
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Active 10-Minute Safety Net Banner
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1E1B4B 0%, #312E81 100%); border: 2px solid #6366F1; border-radius: 16px; padding: 20px; color: #FFFFFF; margin-bottom: 20px;">
        <h3 style="color: #A5B4FC; margin-top: 0;">🛡️ Active 10-Minute First-Trial Safety Net</h3>
        <p style="color: #E0E7FF; font-size: 0.9rem;">
            Your order is protected by Blinkit's Zero-Risk Shield. Need an exchange or return? Request a 1-click doorstep rider exchange within 10 minutes!
        </p>
        <div style="font-family: monospace; font-size: 2rem; font-weight: 900; color: #F7C200; background-color: #0F172A; padding: 10px; border-radius: 10px; text-align: center;">
            ⏳ 09:59 (Shield Protection Active)
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Doorstep Exchange Request Button
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
