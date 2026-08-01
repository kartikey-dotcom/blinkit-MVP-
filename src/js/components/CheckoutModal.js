/* ==========================================================================
   Checkout Modal Component - Address Manager, Payment Gateway & Order Placement
   ========================================================================== */

import { store } from '../store.js';

export class CheckoutModal {
  constructor(containerId, onOrderPlaced) {
    this.container = document.getElementById(containerId);
    this.onOrderPlaced = onOrderPlaced;
    this.isOpen = false;
    this.selectedAddressId = 'addr-1';
    this.selectedPayment = 'UPI';
    this.isProcessing = false;
    this.deliveryInstructions = new Set(['🔕 Do not ring bell']);
    this.init();
  }

  init() {
    store.subscribe(() => this.render());
    this.render();
  }

  open() {
    this.isOpen = true;
    this.isProcessing = false;
    this.render();
  }

  close() {
    this.isOpen = false;
    this.isProcessing = false;
    this.render();
  }

  render() {
    const state = store.getState();

    // Compute bill summary
    let itemTotal = 0;
    Object.entries(state.cart).forEach(([prodId, qty]) => {
      const p = state.products.find(item => item.id === prodId);
      if (p) itemTotal += p.price * qty;
    });

    const deliveryFee = itemTotal >= 199 ? 0 : 25;
    const surgeFee = itemTotal > 0 ? 5 : 0;
    const discount = state.appliedCoupon ? state.appliedCoupon.discount : 0;
    const grandTotal = Math.max(0, itemTotal + deliveryFee + surgeFee - discount);

    this.container.innerHTML = `
      <div class="modal-backdrop ${this.isOpen ? 'active' : ''}" id="checkoutModalBackdrop">
        <div class="modal-card">
          <div class="modal-header">
            <h3 style="font-family: var(--font-heading); font-weight: 800; display: flex; align-items: center; gap: 8px;">
              <span>⚡</span> Checkout & Pay
            </h3>
            <button id="closeCheckoutBtn" style="font-size: 1.2rem; color: var(--text-muted);" ${this.isProcessing ? 'disabled' : ''}>✕</button>
          </div>

          <div class="modal-body">
            <!-- Delivery Address Section -->
            <div class="form-group">
              <label class="form-label">📍 Select Delivery Address</label>
              <div style="display: flex; flex-direction: column; gap: 10px;">
                ${state.userAddresses.map(addr => `
                  <div 
                    class="payment-card ${this.selectedAddressId === addr.id ? 'selected' : ''}"
                    data-address-id="${addr.id}"
                  >
                    <span style="font-size: 1.4rem;">${addr.label === 'Home' ? '🏠' : '🏢'}</span>
                    <div>
                      <strong style="font-size: 0.9rem;">${addr.label}</strong>
                      <p style="font-size: 0.78rem; color: var(--text-muted); line-height: 1.2;">${addr.street}</p>
                      <span style="font-size: 0.7rem; color: var(--color-brand); font-weight: bold;">⚡ Served by Indiranagar DS-104</span>
                    </div>
                  </div>
                `).join('')}
              </div>
            </div>

            <!-- Delivery Instructions -->
            <div class="form-group">
              <label class="form-label">📝 Delivery Instructions for Rider</label>
              <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                ${['🔕 Do not ring bell', '🚪 Leave at door', '📞 Call upon arrival'].map(inst => {
                  const selected = this.deliveryInstructions.has(inst);
                  return `
                    <span 
                      class="instruction-chip" 
                      data-inst="${inst}"
                      style="background: ${selected ? 'var(--color-brand-light)' : 'var(--bg-main)'}; color: ${selected ? 'var(--color-brand)' : 'var(--text-main)'}; border: 1px solid ${selected ? 'var(--color-brand)' : 'var(--border-color)'}; font-size: 0.75rem; font-weight: 700; padding: 6px 12px; border-radius: 20px; cursor: pointer; transition: all 0.15s ease;"
                    >
                      ${selected ? '✓ ' : ''}${inst}
                    </span>
                  `;
                }).join('')}
              </div>
            </div>

            <!-- Payment Methods -->
            <div class="form-group">
              <label class="form-label">💳 Select Payment Method</label>
              <div class="payment-option-grid">
                <div class="payment-card ${this.selectedPayment === 'UPI' ? 'selected' : ''}" data-payment="UPI">
                  <span style="font-size: 1.2rem;">📱</span>
                  <div>
                    <strong style="font-size: 0.85rem;">UPI / GPay / PhonePe</strong>
                    <p style="font-size: 0.7rem; color: var(--text-muted);">Instant 1-Click Pay</p>
                  </div>
                </div>

                <div class="payment-card ${this.selectedPayment === 'CARD' ? 'selected' : ''}" data-payment="CARD">
                  <span style="font-size: 1.2rem;">💳</span>
                  <div>
                    <strong style="font-size: 0.85rem;">Credit / Debit Card</strong>
                    <p style="font-size: 0.7rem; color: var(--text-muted);">Visa, Mastercard, RuPay</p>
                  </div>
                </div>

                <div class="payment-card ${this.selectedPayment === 'WALLET' ? 'selected' : ''}" data-payment="WALLET">
                  <span style="font-size: 1.2rem;">👛</span>
                  <div>
                    <strong style="font-size: 0.85rem;">Paytm Wallet</strong>
                    <p style="font-size: 0.7rem; color: var(--text-muted);">Quick Wallet Pay</p>
                  </div>
                </div>

                <div class="payment-card ${this.selectedPayment === 'COD' ? 'selected' : ''}" data-payment="COD">
                  <span style="font-size: 1.2rem;">💵</span>
                  <div>
                    <strong style="font-size: 0.85rem;">Cash on Delivery</strong>
                    <p style="font-size: 0.7rem; color: var(--text-muted);">Pay cash at doorstep</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Order Total Banner -->
            <div style="background: var(--color-brand-light); border: 1px solid rgba(12, 131, 31, 0.3); border-radius: var(--radius-md); padding: 12px; display: flex; justify-content: space-between; align-items: center; margin-top: 10px;">
              <div>
                <span style="font-size: 0.75rem; color: var(--text-muted); display: block;">Total Amount to Pay</span>
                <strong style="font-size: 1.25rem; color: var(--color-brand);">₹${grandTotal}</strong>
              </div>
              <span style="background: var(--color-brand); color: #fff; font-size: 0.7rem; font-weight: 800; padding: 4px 8px; border-radius: 4px;">
                ⚡ 10-MIN GUARANTEE
              </span>
            </div>
          </div>

          <div style="padding: 16px 24px; border-top: 1px solid var(--border-color); background: var(--bg-surface);">
            <button class="btn-proceed-checkout" id="confirmPayBtn" ${this.isProcessing ? 'disabled style="opacity:0.6; cursor:not-allowed;"' : ''}>
              ${this.isProcessing ? `
                <span>⏳ Processing Payment...</span>
                <span>Connecting to Bank...</span>
              ` : `
                <span>Pay & Place Order</span>
                <span>₹${grandTotal} ✓</span>
              `}
            </button>
          </div>
        </div>
      </div>
    `;

    this.bindEvents();
  }

  bindEvents() {
    const backdrop = this.container.querySelector('#checkoutModalBackdrop');
    if (backdrop) {
      backdrop.addEventListener('click', (e) => {
        if (e.target === backdrop && !this.isProcessing) this.close();
      });
    }

    const closeBtn = this.container.querySelector('#closeCheckoutBtn');
    if (closeBtn) {
      closeBtn.addEventListener('click', () => {
        if (!this.isProcessing) this.close();
      });
    }

    // Address selection
    this.container.querySelectorAll('[data-address-id]').forEach(card => {
      card.addEventListener('click', (e) => {
        if (!this.isProcessing) {
          this.selectedAddressId = e.currentTarget.dataset.addressId;
          this.render();
        }
      });
    });

    // Delivery instruction chips toggle
    this.container.querySelectorAll('.instruction-chip').forEach(chip => {
      chip.addEventListener('click', (e) => {
        const inst = e.currentTarget.dataset.inst;
        if (this.deliveryInstructions.has(inst)) {
          this.deliveryInstructions.delete(inst);
        } else {
          this.deliveryInstructions.add(inst);
        }
        this.render();
      });
    });

    // Payment selection
    this.container.querySelectorAll('[data-payment]').forEach(card => {
      card.addEventListener('click', (e) => {
        if (!this.isProcessing) {
          this.selectedPayment = e.currentTarget.dataset.payment;
          this.render();
        }
      });
    });

    // Confirm Pay
    const confirmBtn = this.container.querySelector('#confirmPayBtn');
    if (confirmBtn) {
      confirmBtn.addEventListener('click', () => {
        if (this.isProcessing) return;

        this.isProcessing = true;
        this.render();

        // Simulate 800ms payment gateway processing time
        setTimeout(() => {
          const order = store.placeOrder({
            addressId: this.selectedAddressId,
            paymentMethod: this.selectedPayment
          });

          if (order) {
            this.close();
            if (this.onOrderPlaced) this.onOrderPlaced(order);
          }
        }, 800);
      });
    }
  }
}
