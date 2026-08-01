/* ==========================================================================
   Rider Partner App Component - Ride Offers, Route Telemetry & Doorstep OTP
   ========================================================================== */

import { store } from '../store.js';

export class RiderView {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.simulatingRider = false;
    this.simInterval = null;
    this.init();
  }

  init() {
    store.subscribe(() => this.render());
    this.render();
  }

  render() {
    const state = store.getState();
    if (state.activePersona !== 'rider') {
      this.container.style.display = 'none';
      return;
    }
    this.container.style.display = 'block';

    const activeRider = state.riders[0];
    const assignedOrders = state.orders.filter(o => o.riderId === activeRider.id);

    this.container.innerHTML = `
      <main class="main-layout" style="max-width: 640px;">
        <div style="background: #091e12; color: #fff; padding: 22px; border-radius: var(--radius-lg); margin-bottom: 20px; box-shadow: var(--shadow-md);">
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <div style="display: flex; align-items: center; gap: 14px;">
              <span style="font-size: 2.4rem;">${activeRider.avatar}</span>
              <div>
                <span style="background: #a3e635; color: #000; font-size: 0.68rem; font-weight: 900; padding: 2px 6px; border-radius: 4px; text-transform: uppercase;">
                  RIDER PARTNER PORTAL
                </span>
                <h3 style="font-family: var(--font-heading); font-weight: 800; font-size: 1.3rem; margin-top: 2px;">
                  ${activeRider.name}
                </h3>
                <span style="font-size: 0.78rem; color: #cbd5e1;">${activeRider.vehicle} • ONLINE</span>
              </div>
            </div>

            <div style="text-align: right;">
              <span style="background: var(--color-brand); color: #fff; font-size: 0.75rem; font-weight: 800; padding: 4px 12px; border-radius: 20px;">
                🟢 ONLINE & ACTIVE
              </span>
            </div>
          </div>
        </div>

        <h3 style="font-family: var(--font-heading); font-weight: 800; font-size: 1.2rem; margin-bottom: 14px;">
          🛵 Active Assigned Deliveries (${assignedOrders.length})
        </h3>

        <div style="display: flex; flex-direction: column; gap: 16px;">
          ${assignedOrders.length === 0 ? `
            <div style="text-align: center; padding: 50px 20px; background: var(--bg-surface); border-radius: var(--radius-lg); border: 1px solid var(--border-color);">
              <div style="font-size: 3rem; margin-bottom: 10px;">🛵</div>
              <h4 style="font-weight: 800;">No active rides assigned</h4>
              <p style="color: var(--text-muted); font-size: 0.85rem;">Waiting for Dark Store order dispatches...</p>
            </div>
          ` : assignedOrders.map(order => this.renderRiderOrderCard(order)).join('')}
        </div>
      </main>
    `;

    this.bindEvents();
  }

  renderRiderOrderCard(order) {
    const isDelivered = order.orderStatus === 'DELIVERED';
    const isEnRoute = order.orderStatus === 'ON_THE_WAY';

    return `
      <div class="portal-card" style="border: 2px solid ${isEnRoute ? 'var(--color-brand)' : 'var(--border-color)'};">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 10px;">
          <div>
            <span class="badge-status ${order.orderStatus.toLowerCase()}">${order.orderStatus}</span>
            <h4 style="font-family: var(--font-heading); font-weight: 800; margin-top: 4px; font-size: 1.1rem;">
              Order #${order.id}
            </h4>
          </div>
          <span style="font-weight: 900; font-size: 1.2rem; color: var(--color-brand);">₹${order.totalAmount}</span>
        </div>

        <div style="background: var(--bg-main); padding: 12px; border-radius: var(--radius-sm); font-size: 0.85rem; margin-bottom: 14px; display: flex; flex-direction: column; gap: 6px;">
          <div>
            <strong>🏢 Pickup Dark Store:</strong> Dark Store #104 - Indiranagar
          </div>
          <div>
            <strong>🏠 Drop Location:</strong> ${order.address}
          </div>
          <div>
            <strong>📦 Items (${order.items.length}):</strong> ${order.items.map(i => `${i.title} (x${i.quantity})`).join(', ')}
          </div>
        </div>

        ${!isDelivered ? `
          <div style="display: flex; flex-direction: column; gap: 8px;">
            ${!isEnRoute ? `
              <button 
                class="btn-start-route" 
                data-order-id="${order.id}"
                style="background: var(--color-brand); color: #fff; font-weight: 800; padding: 12px; border-radius: var(--radius-sm); width: 100%; font-size: 0.95rem;"
              >
                🚀 Pick Up Package & Start Navigation
              </button>
            ` : `
              <div style="background: var(--color-accent); color: #000; padding: 10px; border-radius: var(--radius-sm); font-weight: 800; font-size: 0.85rem; text-align: center;">
                ⚡ Live GPS Navigation Active • Transmitting Telemetry
              </div>

              <div style="margin-top: 8px; padding-top: 8px; border-top: 1px solid var(--border-color);">
                <label style="font-size: 0.8rem; font-weight: 800; display: block; margin-bottom: 6px;">
                  🔑 Enter Customer Doorstep OTP (Test OTP: <strong style="color: var(--color-brand);">${order.otp}</strong>):
                </label>
                <div style="display: flex; gap: 8px;">
                  <input 
                    type="text" 
                    class="otp-input-field" 
                    id="otpInput-${order.id}"
                    placeholder="4-Digit OTP"
                    maxlength="4"
                    style="flex:1; padding: 10px; border: 1.5px solid var(--border-color); border-radius: var(--radius-sm); text-align: center; font-weight: 900; font-size: 1.1rem; letter-spacing: 4px;"
                  />
                  <button 
                    class="btn-verify-otp" 
                    data-order-id="${order.id}"
                    style="background: var(--color-brand); color: #fff; font-weight: 800; padding: 10px 18px; border-radius: var(--radius-sm); font-size: 0.9rem;"
                  >
                    Verify & Deliver
                  </button>
                </div>
              </div>
            `}
          </div>
        ` : `
          <div style="background: var(--color-brand-light); color: var(--color-brand); font-weight: 800; padding: 12px; border-radius: var(--radius-sm); text-align: center;">
            ✓ Delivery Successfully Completed
          </div>
        `}
      </div>
    `;
  }

  bindEvents() {
    this.container.querySelectorAll('.btn-start-route').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const orderId = e.currentTarget.dataset.orderId;
        store.updateOrderStatus(orderId, 'ON_THE_WAY');
        alert(`🛵 Package picked up from Dark Store #104! Starting live GPS route navigation to customer.`);
      });
    });

    this.container.querySelectorAll('.btn-verify-otp').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const orderId = e.currentTarget.dataset.orderId;
        const input = this.container.querySelector(`#otpInput-${orderId}`);
        const state = store.getState();
        const order = state.orders.find(o => o.id === orderId);

        if (order && input && input.value.trim() === order.otp) {
          store.updateOrderStatus(orderId, 'DELIVERED');
          alert(`🎉 OTP Verified! Order #${orderId} marked DELIVERED successfully! Notification pushed to Consumer.`);
        } else {
          alert(`❌ Invalid OTP entered! Customer OTP is ${order ? order.otp : '4819'}`);
        }
      });
    });
  }
}
