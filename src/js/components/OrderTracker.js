/* ==========================================================================
   Order Tracker Component - Live Telemetry, SVG Map Animation, Countdown & OTP
   ========================================================================== */

import { store } from '../store.js';

export class OrderTracker {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.timerInterval = null;
    this.telemetryInterval = null;
    this.etaSeconds = 480; // 8 minutes initial ETA
    this.riderProgressPct = 0.1;
    this.init();
  }

  init() {
    store.subscribe(() => this.render());
    this.startTimerAndTelemetry();
    this.render();
  }

  startTimerAndTelemetry() {
    if (this.timerInterval) clearInterval(this.timerInterval);
    if (this.telemetryInterval) clearInterval(this.telemetryInterval);

    // Countdown Timer tick
    this.timerInterval = setInterval(() => {
      const state = store.getState();
      const activeOrder = state.orders.find(o => o.id === state.activeOrderId) || state.orders[0];

      if (activeOrder && activeOrder.orderStatus === 'DELIVERED') {
        clearInterval(this.timerInterval);
        this.etaSeconds = 0;
        this.updateTimerDOM();
        return;
      }

      if (this.etaSeconds > 0) {
        this.etaSeconds -= 1;
        this.updateTimerDOM();
      }
    }, 1000);

    // Live GPS Telemetry simulation tick (moves rider smoothly)
    this.telemetryInterval = setInterval(() => {
      const state = store.getState();
      const activeOrder = state.orders.find(o => o.id === state.activeOrderId) || state.orders[0];
      
      if (activeOrder && activeOrder.orderStatus === 'ON_THE_WAY') {
        if (this.riderProgressPct < 0.94) {
          this.riderProgressPct += 0.03;
          this.renderMapOnly();
        }
      } else if (activeOrder && activeOrder.orderStatus === 'DELIVERED') {
        this.riderProgressPct = 1.0;
        this.renderMapOnly();
        clearInterval(this.telemetryInterval);
      }
    }, 2000);
  }

  updateTimerDOM() {
    const el = this.container.querySelector('#countdownTimerText');
    if (el) {
      const mins = Math.floor(this.etaSeconds / 60);
      const secs = this.etaSeconds % 60;
      el.textContent = `${mins}m ${secs < 10 ? '0' : ''}${secs}s`;
    }
  }

  renderMapOnly() {
    const svgMarker = this.container.querySelector('#movingRiderGroup');
    if (svgMarker) {
      const startX = 60;
      const endX = 740;
      const currentX = startX + (endX - startX) * this.riderProgressPct;
      svgMarker.setAttribute('transform', `translate(${currentX}, 145)`);
    }
  }

  render() {
    const state = store.getState();
    const activeOrder = state.orders.find(o => o.id === state.activeOrderId) || state.orders[0];

    if (!activeOrder || state.activePersona !== 'consumer') {
      return;
    }

    const rider = state.riders.find(r => r.id === activeOrder.riderId) || state.riders[0];
    const mins = Math.floor(this.etaSeconds / 60);
    const secs = this.etaSeconds % 60;

    // Adjust progress percentage based on order status
    if (activeOrder.orderStatus === 'PLACED') this.riderProgressPct = 0.08;
    else if (activeOrder.orderStatus === 'PACKING') this.riderProgressPct = 0.20;
    else if (activeOrder.orderStatus === 'DISPATCHED') this.riderProgressPct = 0.40;
    else if (activeOrder.orderStatus === 'DELIVERED') this.riderProgressPct = 1.0;

    const startX = 60;
    const endX = 740;
    const currentX = startX + (endX - startX) * this.riderProgressPct;

    this.container.innerHTML = `
      <div class="tracker-container">
        <!-- Tracker Header & Countdown -->
        <div class="tracker-header">
          <div>
            <span style="font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px; opacity: 0.9;">
              Order #${activeOrder.id} • ${new Date(activeOrder.createdAt).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
            </span>
            <h2 style="font-family: var(--font-heading); font-weight: 800; margin-top: 4px;">
              ${activeOrder.orderStatus === 'DELIVERED' ? '🎉 Order Delivered!' : 'Arriving in 10 Minutes'}
            </h2>
          </div>

          <div style="text-align: right;">
            <div style="font-size: 0.75rem; opacity: 0.9;">LIVE ETA</div>
            <div class="eta-timer-display" id="countdownTimerText">
              ${activeOrder.orderStatus === 'DELIVERED' ? '0m 00s' : `${mins}m ${secs < 10 ? '0' : ''}${secs}s`}
            </div>
          </div>
        </div>

        <!-- Order Lifecycle Stepper -->
        <div style="padding: 16px 24px; background: var(--bg-main); border-bottom: 1px solid var(--border-color); display: flex; justify-content: space-between; align-items: center; gap: 8px;">
          <div style="display: flex; align-items: center; gap: 6px;">
            <span class="badge-status ${activeOrder.orderStatus === 'PLACED' ? 'placed' : 'delivered'}">1. Placed</span>
          </div>
          <span style="color: var(--border-color);">→</span>
          <div style="display: flex; align-items: center; gap: 6px;">
            <span class="badge-status ${activeOrder.orderStatus === 'PACKING' ? 'packing' : (['DISPATCHED','ON_THE_WAY','DELIVERED'].includes(activeOrder.orderStatus) ? 'delivered' : 'placed')}">2. Packing</span>
          </div>
          <span style="color: var(--border-color);">→</span>
          <div style="display: flex; align-items: center; gap: 6px;">
            <span class="badge-status ${activeOrder.orderStatus === 'ON_THE_WAY' || activeOrder.orderStatus === 'DISPATCHED' ? 'dispatched' : (activeOrder.orderStatus === 'DELIVERED' ? 'delivered' : 'placed')}">3. On the Way</span>
          </div>
          <span style="color: var(--border-color);">→</span>
          <div style="display: flex; align-items: center; gap: 6px;">
            <span class="badge-status ${activeOrder.orderStatus === 'DELIVERED' ? 'delivered' : 'placed'}">4. Delivered</span>
          </div>
        </div>

        <!-- Interactive SVG GPS Telemetry Map Simulator -->
        <div class="map-simulation-container">
          <svg width="100%" height="100%" viewBox="0 0 800 320" xmlns="http://www.w3.org/2000/svg">
            <defs>
              <linearGradient id="mapBg" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#f1f5f9" />
                <stop offset="100%" stop-color="#e2e8f0" />
              </linearGradient>
            </defs>
            <rect width="800" height="320" fill="url(#mapBg)" />

            <!-- City Grid Roads -->
            <path d="M 50 160 Q 200 80 400 160 T 750 160" stroke="#cbd5e1" stroke-width="18" fill="none" />
            <path d="M 50 160 Q 200 80 400 160 T 750 160" stroke="#ffffff" stroke-width="12" fill="none" stroke-dasharray="8 6" />

            <!-- Dark Store Marker (Origin) -->
            <g transform="translate(60, 160)">
              <circle r="22" fill="#0c831f" />
              <text x="0" y="6" text-anchor="middle" font-size="18">🏢</text>
              <text x="0" y="38" text-anchor="middle" font-size="11" font-weight="bold" fill="#0f172a">Dark Store #104</text>
            </g>

            <!-- Customer Destination Marker -->
            <g transform="translate(740, 160)">
              <circle r="22" fill="#ff5722" />
              <text x="0" y="6" text-anchor="middle" font-size="18">🏠</text>
              <text x="0" y="38" text-anchor="middle" font-size="11" font-weight="bold" fill="#0f172a">Your Address</text>
            </g>

            <!-- Moving Rider Icon with Telemetry Simulation -->
            <g id="movingRiderGroup" transform="translate(${currentX}, 145)">
              <circle r="20" fill="#f8cb46" stroke="#000" stroke-width="2" />
              <text x="0" y="6" text-anchor="middle" font-size="20">🛵</text>
              <rect x="-45" y="-30" width="90" height="18" rx="4" fill="#0f172a" opacity="0.88" />
              <text x="0" y="-18" text-anchor="middle" font-size="9" font-weight="bold" fill="#ffffff">${rider.name.split(' ')[0]} (${Math.round(this.riderProgressPct * 100)}%)</text>
            </g>
          </svg>
        </div>

        <!-- Delivery OTP Card -->
        <div class="otp-box">
          <span style="font-size: 0.8rem; text-transform: uppercase; font-weight: 700; display: block; letter-spacing: 1px; color: #334155;">
            Share Delivery OTP with Rider at Doorstep
          </span>
          <span style="font-size: 2.2rem; font-weight: 900; letter-spacing: 8px;">${activeOrder.otp}</span>
        </div>

        <!-- Rider Information Footer -->
        <div style="padding: 16px 24px; border-top: 1px solid var(--border-color); display: flex; justify-content: space-between; align-items: center; background: var(--bg-surface);">
          <div style="display: flex; align-items: center; gap: 12px;">
            <div style="font-size: 2rem;">${rider.avatar}</div>
            <div>
              <strong style="font-size: 0.95rem;">${rider.name}</strong>
              <p style="font-size: 0.78rem; color: var(--text-muted);">${rider.vehicle}</p>
            </div>
          </div>

          <div style="display: flex; gap: 8px;">
            <button 
              id="callRiderBtn"
              style="background: var(--color-brand-light); color: var(--color-brand); font-weight: 800; padding: 8px 14px; border-radius: var(--radius-sm); border: 1px solid var(--color-brand); font-size: 0.85rem;"
            >
              📞 Call Rider (${rider.name.split(' ')[0]})
            </button>
          </div>
        </div>
      </div>
    `;

    this.bindEvents(rider);
  }

  bindEvents(rider) {
    const callBtn = this.container.querySelector('#callRiderBtn');
    if (callBtn) {
      callBtn.addEventListener('click', () => {
        alert(`📞 Simulating call to delivery partner ${rider.name} (${rider.phone})...`);
      });
    }
  }
}
