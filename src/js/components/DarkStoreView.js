/* ==========================================================================
   Dark Store Picker Portal Component - Sub-2-Minute Order Picking & Rack Coordinates
   ========================================================================== */

import { store } from '../store.js';

export class DarkStoreView {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.checkedItemsState = {}; // { 'orderId-idx': true }
    this.init();
  }

  init() {
    store.subscribe(() => this.render());
    this.render();
  }

  render() {
    const state = store.getState();
    if (state.activePersona !== 'picker') {
      this.container.style.display = 'none';
      return;
    }
    this.container.style.display = 'block';

    const storeOrders = state.orders.filter(o => o.darkStoreId === state.activeDarkStoreId);
    const activeStoreObj = state.darkStores.find(ds => ds.id === state.activeDarkStoreId);
    const pendingOrdersCount = storeOrders.filter(o => o.orderStatus === 'PLACED' || o.orderStatus === 'PACKING').length;

    this.container.innerHTML = `
      <main class="main-layout">
        <!-- Top Dark Store Status Header -->
        <div style="background: linear-gradient(135deg, #0f172a, #1e293b); color: #fff; padding: 22px 24px; border-radius: var(--radius-lg); margin-bottom: 24px; display: flex; justify-content: space-between; align-items: center; box-shadow: var(--shadow-md);">
          <div>
            <div style="display: flex; align-items: center; gap: 8px;">
              <span style="background: var(--color-brand); color: #fff; font-size: 0.7rem; font-weight: 900; padding: 2px 8px; border-radius: 4px; text-transform: uppercase;">
                LIVE PICKER WORKSPACE
              </span>
              <span style="background: ${pendingOrdersCount > 0 ? 'var(--color-express)' : 'var(--color-success)'}; color: #fff; font-size: 0.7rem; font-weight: 900; padding: 2px 8px; border-radius: 4px;">
                ${pendingOrdersCount > 0 ? `⚡ ${pendingOrdersCount} PENDING ORDERS` : '✓ ALL CLEAR'}
              </span>
            </div>

            <h2 style="font-family: var(--font-heading); font-weight: 800; font-size: 1.6rem; margin-top: 6px;">
              📦 ${activeStoreObj ? activeStoreObj.name : 'Dark Store #104'}
            </h2>
            <p style="font-size: 0.85rem; color: #94a3b8; margin-top: 2px;">
              Optimal Pick-and-Pack KPI: <strong>&lt; 120 Seconds</strong> per order
            </p>
          </div>

          <div style="display: flex; gap: 10px;">
            <button id="chimeAlertBtn" style="background: rgba(255,255,255,0.1); color: #fff; border: 1px solid rgba(255,255,255,0.2); padding: 10px 16px; border-radius: var(--radius-md); font-weight: 700; font-size: 0.85rem; transition: background 0.15s ease;">
              🔔 Test Audio Chime
            </button>
          </div>
        </div>

        <!-- Incoming Orders Queue -->
        <div style="display: grid; grid-template-columns: 1fr; gap: 20px;">
          ${storeOrders.length === 0 ? `
            <div style="text-align: center; padding: 60px 20px; background: var(--bg-surface); border-radius: var(--radius-lg); border: 1px solid var(--border-color);">
              <div style="font-size: 3.5rem; margin-bottom: 12px;">✅</div>
              <h3 style="font-weight: 800; font-size: 1.2rem; margin-bottom: 6px;">All store orders fulfilled!</h3>
              <p style="color: var(--text-muted); font-size: 0.88rem;">Waiting for new incoming orders from consumers...</p>
            </div>
          ` : storeOrders.map(order => this.renderPickerOrderCard(order)).join('')}
        </div>
      </main>
    `;

    this.bindEvents();
  }

  renderPickerOrderCard(order) {
    const isPacked = order.orderStatus === 'PACKED' || order.orderStatus === 'DISPATCHED' || order.orderStatus === 'ON_THE_WAY' || order.orderStatus === 'DELIVERED';
    
    // Calculate pick progress
    const totalItemTypes = order.items.length;
    let checkedCount = 0;
    order.items.forEach((_, idx) => {
      if (this.checkedItemsState[`${order.id}-${idx}`] || isPacked) {
        checkedCount += 1;
      }
    });

    const isFullyChecked = checkedCount === totalItemTypes;
    const elapsedSecs = Math.max(10, Math.floor((new Date() - new Date(order.createdAt)) / 1000));
    const isUrgent = elapsedSecs > 120 && !isPacked;

    return `
      <div class="portal-card" style="border: 2px solid ${isUrgent ? 'var(--color-danger)' : (isPacked ? 'var(--color-brand)' : 'var(--border-color)')}; position: relative;">
        ${isUrgent ? `
          <span style="position: absolute; top: -12px; right: 20px; background: var(--color-danger); color: #fff; font-size: 0.7rem; font-weight: 900; padding: 2px 8px; border-radius: 4px;">
            ⚠️ PICK DELAYED (> 120s)
          </span>
        ` : ''}

        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 14px;">
          <div>
            <div style="display: flex; align-items: center; gap: 8px;">
              <span class="badge-status ${order.orderStatus.toLowerCase()}">${order.orderStatus}</span>
              <span style="font-size: 0.78rem; font-family: monospace; color: var(--text-muted);">
                ⏱️ Elapsed: ${elapsedSecs}s / 120s Target
              </span>
            </div>

            <h3 style="font-family: var(--font-heading); font-weight: 800; font-size: 1.3rem; margin-top: 6px;">
              Order #${order.id}
            </h3>
            <span style="font-size: 0.78rem; color: var(--text-muted);">
              Customer: User #usr-1 • Address: ${order.address}
            </span>
          </div>

          <div style="text-align: right;">
            <span style="font-weight: 900; font-size: 1.2rem; color: var(--color-brand); display: block;">
              ${order.items.reduce((s, i) => s + i.quantity, 0)} Items
            </span>
            <span style="font-size: 0.75rem; font-weight: 700; color: ${isFullyChecked ? 'var(--color-success)' : 'var(--text-muted)'};">
              Checked: ${checkedCount} / ${totalItemTypes}
            </span>
          </div>
        </div>

        <!-- Pick List Checklist with Rack Coordinates -->
        <h4 style="font-weight: 800; font-size: 0.9rem; margin-bottom: 10px;">
          📍 Dark Store Pick Route & Rack Locations:
        </h4>

        <div style="background: var(--bg-main); border-radius: var(--radius-md); padding: 12px; margin-bottom: 16px;">
          ${order.items.map((item, idx) => {
            const isChecked = this.checkedItemsState[`${order.id}-${idx}`] || isPacked;
            return `
              <div style="display: flex; align-items: center; justify-content: space-between; padding: 10px 0; border-bottom: ${idx < order.items.length - 1 ? '1px solid var(--border-color)' : 'none'}; opacity: ${isChecked ? 0.6 : 1};">
                <div style="display: flex; align-items: center; gap: 12px;">
                  <input 
                    type="checkbox" 
                    class="item-picker-chk"
                    data-order-id="${order.id}"
                    data-item-idx="${idx}"
                    id="chk-${order.id}-${idx}" 
                    ${isChecked ? 'checked' : ''} 
                    ${isPacked ? 'disabled' : ''} 
                    style="width: 20px; height: 20px; accent-color: var(--color-brand); cursor: pointer;" 
                  />
                  <label for="chk-${order.id}-${idx}" style="font-size: 0.9rem; font-weight: 700; cursor: pointer; ${isChecked ? 'text-decoration: line-through;' : ''}">
                    ${item.title} <span style="color: var(--text-muted); font-weight: 500;">(${item.unit})</span>
                  </label>
                </div>

                <div style="display: flex; align-items: center; gap: 12px;">
                  <span style="background: #fef08a; color: #854d0e; font-weight: 800; font-size: 0.78rem; padding: 4px 10px; border-radius: 4px; font-family: monospace;">
                    📍 ${item.rack}
                  </span>
                  <span style="font-weight: 900; font-size: 0.95rem; background: var(--bg-surface); padding: 4px 10px; border-radius: 4px; border: 1px solid var(--border-color);">
                    x${item.quantity}
                  </span>
                </div>
              </div>
            `;
          }).join('')}
        </div>

        <div style="display: flex; justify-content: space-between; align-items: center;">
          <div style="font-size: 0.8rem; color: var(--text-muted);">
            ${isFullyChecked ? '✓ All items picked & audited' : '⚠️ Please check all items off the list before packing'}
          </div>

          <button 
            class="btn-pack-order" 
            data-order-id="${order.id}"
            ${isPacked ? 'disabled style="opacity:0.5; background:#64748b; cursor:not-allowed;"' : ''}
            style="background: ${isFullyChecked ? 'var(--color-brand)' : 'var(--color-warning)'}; color: #fff; font-weight: 800; padding: 12px 24px; border-radius: var(--radius-md); font-size: 0.95rem; transition: background 0.15s ease;"
          >
            ${isPacked ? '✓ Order Packed & Handed to Rider' : '📦 Confirm Packing & Handover to Rider'}
          </button>
        </div>
      </div>
    `;
  }

  bindEvents() {
    // Checkbox toggles
    this.container.querySelectorAll('.item-picker-chk').forEach(chk => {
      chk.addEventListener('change', (e) => {
        const orderId = e.currentTarget.dataset.orderId;
        const itemIdx = e.currentTarget.dataset.itemIdx;
        this.checkedItemsState[`${orderId}-${itemIdx}`] = e.currentTarget.checked;
        this.render();
      });
    });

    // Pack Order Action
    this.container.querySelectorAll('.btn-pack-order').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const orderId = e.currentTarget.dataset.orderId;
        store.updateOrderStatus(orderId, 'DISPATCHED');
        alert(`📦 Order #${orderId} marked PACKED & DISPATCHED to Rider! Notification sent to Rider Partner app.`);
      });
    });

    const chimeBtn = this.container.querySelector('#chimeAlertBtn');
    if (chimeBtn) {
      chimeBtn.addEventListener('click', () => {
        alert('🔔 Sound chime test: 120-second pick notification sound active!');
      });
    }
  }
}
