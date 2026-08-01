/* ==========================================================================
   Cart Drawer Component - Slide-Over Panel, Dynamic Pricing, Coupons & Recommendations
   ========================================================================== */

import { store } from '../store.js';

export class CartDrawer {
  constructor(containerId, onProceedToCheckout) {
    this.container = document.getElementById(containerId);
    this.onProceedToCheckout = onProceedToCheckout;
    this.isOpen = false;
    this.init();
  }

  init() {
    store.subscribe(() => this.render());
    this.render();
  }

  open() {
    this.isOpen = true;
    this.render();
  }

  close() {
    this.isOpen = false;
    this.render();
  }

  render() {
    const state = store.getState();
    const cartEntries = Object.entries(state.cart);

    let itemTotal = 0;
    const cartItems = [];

    cartEntries.forEach(([prodId, qty]) => {
      const p = state.products.find(item => item.id === prodId);
      if (p) {
        const total = p.price * qty;
        itemTotal += total;
        cartItems.push({ ...p, quantity: qty, lineTotal: total });
      }
    });

    const freeDeliveryThreshold = 199;
    const deliveryFee = itemTotal >= freeDeliveryThreshold || itemTotal === 0 ? 0 : 25;
    const surgeFee = itemTotal > 0 ? 5 : 0;
    const discount = state.appliedCoupon ? state.appliedCoupon.discount : 0;
    const grandTotal = Math.max(0, itemTotal + deliveryFee + surgeFee - discount);
    const amountNeededForFreeDelivery = Math.max(0, freeDeliveryThreshold - itemTotal);
    const freeDeliveryPct = Math.min(100, Math.round((itemTotal / freeDeliveryThreshold) * 100));

    // Get 3 quick recommendation products
    const recommendations = state.products.filter(p => !state.cart[p.id] && p.stock > 0).slice(0, 3);

    this.container.innerHTML = `
      <div class="drawer-backdrop ${this.isOpen ? 'active' : ''}" id="cartBackdrop"></div>

      <div class="cart-drawer ${this.isOpen ? 'active' : ''}">
        <div class="drawer-header">
          <div class="drawer-title">
            <span>🛒 My Shopping Cart</span>
            <span style="font-size: 0.85rem; color: var(--text-muted); font-weight: 500;">(${cartItems.length} Items)</span>
          </div>
          <button class="drawer-close-btn" id="closeDrawerBtn" title="Close Cart">✕</button>
        </div>

        ${itemTotal > 0 ? `
          <div class="free-delivery-banner">
            <div style="display: flex; justify-content: space-between; font-size: 0.8rem; font-weight: 700;">
              <span>${amountNeededForFreeDelivery === 0 ? '🎉 You unlocked FREE Delivery!' : `Add ₹${amountNeededForFreeDelivery} more for FREE Delivery`}</span>
              <span>₹${itemTotal} / ₹${freeDeliveryThreshold}</span>
            </div>
            <div class="progress-bar-bg">
              <div class="progress-bar-fill" style="width: ${freeDeliveryPct}%;"></div>
            </div>
          </div>
        ` : ''}

        <div class="drawer-body">
          ${cartItems.length === 0 ? `
            <div style="text-align: center; padding: 40px 20px;">
              <div style="font-size: 3.5rem; margin-bottom: 12px;">🛍️</div>
              <h3 style="font-weight: 800; font-size: 1.1rem; margin-bottom: 6px;">Your cart is empty</h3>
              <p style="color: var(--text-muted); font-size: 0.85rem; margin-bottom: 20px;">
                Add fresh groceries & daily essentials to get instant delivery in 10 minutes!
              </p>
            </div>
          ` : `
            <div class="cart-item-list">
              ${cartItems.map(item => `
                <div class="cart-item-card">
                  <img src="${item.image}" alt="${item.title}" class="cart-item-img" />
                  <div class="cart-item-details">
                    <h5 class="cart-item-title">${item.title}</h5>
                    <span class="cart-item-unit">${item.unit} • ₹${item.price}</span>
                  </div>
                  <div class="cart-item-action" style="display: flex; flex-direction: column; align-items: flex-end; gap: 4px;">
                    <span class="cart-item-price">₹${item.lineTotal}</span>
                    <div class="stepper-container">
                      <button class="stepper-btn drawer-btn-minus" data-id="${item.id}">−</button>
                      <span class="stepper-count">${item.quantity}</span>
                      <button class="stepper-btn drawer-btn-plus" data-id="${item.id}">+</button>
                    </div>
                  </div>
                </div>
              `).join('')}
            </div>

            <!-- Coupon Engine -->
            <div class="coupon-section">
              <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-weight: 800; font-size: 0.85rem;">🏷️ Apply Coupon Code</span>
                ${state.appliedCoupon ? `<button id="removeCouponBtn" style="color: var(--color-danger); font-weight: 800; font-size: 0.75rem;">Remove</button>` : ''}
              </div>
              
              ${state.appliedCoupon ? `
                <div style="background: var(--color-brand-light); color: var(--color-brand); font-weight: 800; font-size: 0.8rem; padding: 8px 12px; border-radius: 6px; margin-top: 6px; display: flex; justify-content: space-between; align-items: center;">
                  <span>🎉 Code ${state.appliedCoupon.code} Applied!</span>
                  <span style="font-size: 0.9rem;">-₹${state.appliedCoupon.discount}</span>
                </div>
              ` : `
                <div class="coupon-input-group">
                  <input type="text" class="coupon-input" id="couponInput" placeholder="Try BLINKIT100 or WELCOME50" />
                  <button class="btn-apply-coupon" id="applyCouponBtn">Apply</button>
                </div>
                <div style="margin-top: 6px; display: flex; gap: 6px; flex-wrap: wrap;">
                  <span class="quick-code-pill" data-code="BLINKIT100" style="font-size: 0.7rem; background: var(--bg-surface); border: 1px solid var(--border-color); padding: 2px 6px; border-radius: 4px; cursor: pointer;">
                    ⚡ BLINKIT100 (₹100 Off)
                  </span>
                  <span class="quick-code-pill" data-code="WELCOME50" style="font-size: 0.7rem; background: var(--bg-surface); border: 1px solid var(--border-color); padding: 2px 6px; border-radius: 4px; cursor: pointer;">
                    🎁 WELCOME50 (₹50 Off)
                  </span>
                </div>
              `}
            </div>

            <!-- Dynamic Bill Summary -->
            <div class="bill-breakdown">
              <h5 style="font-weight: 800; margin-bottom: 10px; font-size: 0.9rem;">Bill Details</h5>
              <div class="bill-row">
                <span>Items Subtotal</span>
                <span>₹${itemTotal}</span>
              </div>
              <div class="bill-row">
                <span>Delivery Charge ${deliveryFee === 0 ? '<strong style="color: var(--color-brand);">(FREE)</strong>' : ''}</span>
                <span>₹${deliveryFee}</span>
              </div>
              <div class="bill-row">
                <span>Handling & Surge Fee</span>
                <span>₹${surgeFee}</span>
              </div>
              ${state.appliedCoupon ? `
                <div class="bill-row" style="color: var(--color-brand); font-weight: 700;">
                  <span>Discount (${state.appliedCoupon.code})</span>
                  <span>-₹${discount}</span>
                </div>
              ` : ''}
              <div class="bill-row total">
                <span>To Pay</span>
                <span>₹${grandTotal}</span>
              </div>
            </div>
          `}

          <!-- Quick Recommendations -->
          ${recommendations.length > 0 ? `
            <div style="margin-top: 20px; border-top: 1px solid var(--border-color); padding-top: 14px;">
              <h5 style="font-weight: 800; font-size: 0.85rem; margin-bottom: 10px; color: var(--text-muted);">
                ⚡ Quick Add Suggestions
              </h5>
              <div style="display: flex; flex-direction: column; gap: 8px;">
                ${recommendations.map(rec => `
                  <div style="display: flex; align-items: center; justify-content: space-between; background: var(--bg-main); padding: 8px 12px; border-radius: var(--radius-sm);">
                    <div style="display: flex; align-items: center; gap: 10px;">
                      <img src="${rec.image}" width="28" height="28" style="object-fit: contain;" />
                      <div>
                        <strong style="font-size: 0.8rem; display: block;">${rec.title}</strong>
                        <span style="font-size: 0.72rem; color: var(--text-muted);">${rec.unit} • ₹${rec.price}</span>
                      </div>
                    </div>
                    <button class="btn-rec-add" data-id="${rec.id}" style="background: var(--color-brand-light); color: var(--color-brand); font-weight: 800; font-size: 0.75rem; padding: 4px 10px; border-radius: 4px; border: 1px solid var(--color-brand);">
                      + ADD
                    </button>
                  </div>
                `).join('')}
              </div>
            </div>
          ` : ''}
        </div>

        ${itemTotal > 0 ? `
          <div class="drawer-footer">
            <button class="btn-proceed-checkout" id="checkoutBtn">
              <span>Proceed to Checkout</span>
              <span>₹${grandTotal} →</span>
            </button>
          </div>
        ` : ''}
      </div>
    `;

    this.bindEvents();
  }

  bindEvents() {
    const backdrop = this.container.querySelector('#cartBackdrop');
    if (backdrop) {
      backdrop.addEventListener('click', () => this.close());
    }

    const closeBtn = this.container.querySelector('#closeDrawerBtn');
    if (closeBtn) {
      closeBtn.addEventListener('click', () => this.close());
    }

    // Plus & Minus buttons
    this.container.querySelectorAll('.drawer-btn-plus').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const id = e.currentTarget.dataset.id;
        store.addToCart(id);
      });
    });

    this.container.querySelectorAll('.drawer-btn-minus').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const id = e.currentTarget.dataset.id;
        store.removeFromCart(id);
      });
    });

    // Quick Recommendations ADD
    this.container.querySelectorAll('.btn-rec-add').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const id = e.currentTarget.dataset.id;
        store.addToCart(id);
      });
    });

    // Apply Coupon
    const applyBtn = this.container.querySelector('#applyCouponBtn');
    if (applyBtn) {
      applyBtn.addEventListener('click', () => {
        const input = this.container.querySelector('#couponInput');
        if (input && input.value) {
          const res = store.applyCoupon(input.value);
          alert(res.message);
        }
      });
    }

    this.container.querySelectorAll('.quick-code-pill').forEach(pill => {
      pill.addEventListener('click', (e) => {
        const code = e.currentTarget.dataset.code;
        const res = store.applyCoupon(code);
        alert(res.message);
      });
    });

    const removeCouponBtn = this.container.querySelector('#removeCouponBtn');
    if (removeCouponBtn) {
      removeCouponBtn.addEventListener('click', () => store.removeCoupon());
    }

    // Checkout Button
    const checkoutBtn = this.container.querySelector('#checkoutBtn');
    if (checkoutBtn) {
      checkoutBtn.addEventListener('click', () => {
        this.close();
        if (this.onProceedToCheckout) this.onProceedToCheckout();
      });
    }
  }
}
