/* ==========================================================================
   Admin & Operations Dashboard Component - KPIs, Inventory & Order Audit
   ========================================================================== */

import { store } from '../store.js';

export class AdminView {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.stockSearchQuery = '';
    this.init();
  }

  init() {
    store.subscribe(() => this.render());
    this.render();
  }

  render() {
    const state = store.getState();
    if (state.activePersona !== 'admin') {
      this.container.style.display = 'none';
      return;
    }
    this.container.style.display = 'block';

    const totalOrders = state.orders.length;
    const totalRevenue = state.orders.reduce((sum, o) => sum + o.totalAmount, 0);
    const activeDarkStores = state.darkStores.filter(ds => ds.active).length;

    // Filter products for stock control table
    let productsList = state.products;
    if (this.stockSearchQuery.trim()) {
      const q = this.stockSearchQuery.trim().toLowerCase();
      productsList = productsList.filter(p => p.title.toLowerCase().includes(q) || p.rack.toLowerCase().includes(q));
    }

    this.container.innerHTML = `
      <main class="main-layout">
        <!-- Top Admin Header -->
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
          <div>
            <span style="background: var(--color-brand); color: #fff; font-size: 0.7rem; font-weight: 900; padding: 2px 8px; border-radius: 4px; text-transform: uppercase;">
              PLATFORM GOVERNANCE
            </span>
            <h2 style="font-family: var(--font-heading); font-weight: 800; font-size: 1.7rem; margin-top: 4px;">
              📊 Merchant & Operations Dashboard
            </h2>
            <p style="color: var(--text-muted); font-size: 0.85rem;">Real-time Q-Commerce Metrics, Inventory Control & Order Audits</p>
          </div>

          <button id="resetDemoBtn" style="background: var(--color-danger); color: #fff; font-weight: 800; padding: 12px 20px; border-radius: var(--radius-md); font-size: 0.88rem; box-shadow: var(--shadow-sm);">
            🔄 Reset Demo State
          </button>
        </div>

        <!-- Metric KPI Cards -->
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; margin-bottom: 24px;">
          <div class="portal-card" style="border-left: 4px solid var(--color-brand);">
            <span style="font-size: 0.75rem; color: var(--text-muted); font-weight: 700;">TOTAL PLATFORM ORDERS</span>
            <h3 style="font-family: var(--font-heading); font-size: 1.8rem; font-weight: 800; margin-top: 4px;">
              ${totalOrders}
            </h3>
            <span style="font-size: 0.75rem; color: var(--color-brand); font-weight: 700;">↑ 100% Fulfillment Rate</span>
          </div>

          <div class="portal-card" style="border-left: 4px solid var(--color-accent);">
            <span style="font-size: 0.75rem; color: var(--text-muted); font-weight: 700;">GROSS REVENUE</span>
            <h3 style="font-family: var(--font-heading); font-size: 1.8rem; font-weight: 800; margin-top: 4px; color: var(--color-brand);">
              ₹${totalRevenue}
            </h3>
            <span style="font-size: 0.75rem; color: var(--text-muted);">Avg Order Value: ₹${totalOrders ? Math.round(totalRevenue / totalOrders) : 0}</span>
          </div>

          <div class="portal-card" style="border-left: 4px solid var(--color-express);">
            <span style="font-size: 0.75rem; color: var(--text-muted); font-weight: 700;">ACTIVE DARK STORES</span>
            <h3 style="font-family: var(--font-heading); font-size: 1.8rem; font-weight: 800; margin-top: 4px;">
              ${activeDarkStores} / ${state.darkStores.length}
            </h3>
            <span style="font-size: 0.75rem; color: var(--text-muted);">Indiranagar, Koramangala, HSR</span>
          </div>

          <div class="portal-card" style="border-left: 4px solid var(--color-info);">
            <span style="font-size: 0.75rem; color: var(--text-muted); font-weight: 700;">AVG DELIVERY SPEED</span>
            <h3 style="font-family: var(--font-heading); font-size: 1.8rem; font-weight: 800; margin-top: 4px;">
              7m 42s
            </h3>
            <span style="font-size: 0.75rem; color: var(--color-success); font-weight: 700;">⚡ Under 10-Min Target</span>
          </div>
        </div>

        <!-- Dark Stores Overview Section -->
        <div class="portal-card" style="margin-bottom: 24px;">
          <h3 style="font-family: var(--font-heading); font-weight: 800; font-size: 1.2rem; margin-bottom: 12px;">
            🏢 Operational Dark Store Hubs
          </h3>
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 14px;">
            ${state.darkStores.map(ds => `
              <div style="background: var(--bg-main); border: 1px solid var(--border-color); border-radius: var(--radius-md); padding: 14px; display: flex; justify-content: space-between; align-items: center;">
                <div>
                  <span style="background: #0f172a; color: #a3e635; font-size: 0.7rem; font-weight: 900; padding: 2px 6px; border-radius: 4px; font-family: monospace;">
                    ${ds.code}
                  </span>
                  <h4 style="font-weight: 800; font-size: 0.95rem; margin-top: 4px;">${ds.name}</h4>
                  <p style="font-size: 0.75rem; color: var(--text-muted);">${ds.address}</p>
                </div>
                <span style="background: ${ds.active ? 'var(--color-brand-light)' : '#fee2e2'}; color: ${ds.active ? 'var(--color-brand)' : '#991b1b'}; font-size: 0.75rem; font-weight: 800; padding: 4px 10px; border-radius: 20px;">
                  ${ds.active ? '🟢 OPERATIONAL' : '🔴 OFFLINE'}
                </span>
              </div>
            `).join('')}
          </div>
        </div>

        <!-- Live Orders Audit Table -->
        <div class="portal-card" style="margin-bottom: 24px;">
          <h3 style="font-family: var(--font-heading); font-weight: 800; font-size: 1.2rem; margin-bottom: 14px;">
            📝 Live Order Audit & Status Override
          </h3>
          <div style="overflow-x: auto;">
            <table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 0.85rem;">
              <thead>
                <tr style="border-bottom: 2px solid var(--border-color); background: var(--bg-main);">
                  <th style="padding: 10px;">Order ID</th>
                  <th style="padding: 10px;">Status</th>
                  <th style="padding: 10px;">Items</th>
                  <th style="padding: 10px;">Amount</th>
                  <th style="padding: 10px;">OTP</th>
                  <th style="padding: 10px;">Address</th>
                  <th style="padding: 10px;">Quick Status Override</th>
                </tr>
              </thead>
              <tbody>
                ${state.orders.map(order => `
                  <tr style="border-bottom: 1px solid var(--border-color);">
                    <td style="padding: 10px; font-weight: 800; font-family: monospace;">${order.id}</td>
                    <td style="padding: 10px;"><span class="badge-status ${order.orderStatus.toLowerCase()}">${order.orderStatus}</span></td>
                    <td style="padding: 10px;">${order.items.length} items</td>
                    <td style="padding: 10px; font-weight: 800;">₹${order.totalAmount}</td>
                    <td style="padding: 10px; font-family: monospace; font-weight: 800; color: var(--color-brand);">${order.otp}</td>
                    <td style="padding: 10px; color: var(--text-muted); max-width: 180px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">${order.address}</td>
                    <td style="padding: 10px;">
                      <select class="admin-status-override" data-order-id="${order.id}" style="padding: 4px 8px; border-radius: 4px; border: 1px solid var(--border-color); font-weight: 700; font-size: 0.78rem;">
                        <option value="PLACED" ${order.orderStatus === 'PLACED' ? 'selected' : ''}>PLACED</option>
                        <option value="PACKING" ${order.orderStatus === 'PACKING' ? 'selected' : ''}>PACKING</option>
                        <option value="DISPATCHED" ${order.orderStatus === 'DISPATCHED' ? 'selected' : ''}>DISPATCHED</option>
                        <option value="ON_THE_WAY" ${order.orderStatus === 'ON_THE_WAY' ? 'selected' : ''}>ON_THE_WAY</option>
                        <option value="DELIVERED" ${order.orderStatus === 'DELIVERED' ? 'selected' : ''}>DELIVERED</option>
                      </select>
                    </td>
                  </tr>
                `).join('')}
              </tbody>
            </table>
          </div>
        </div>

        <!-- Inventory Stock Management Table -->
        <div class="portal-card">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; flex-wrap: wrap; gap: 10px;">
            <h3 style="font-family: var(--font-heading); font-weight: 800; font-size: 1.2rem;">
              📦 Dark Store Stock Control
            </h3>
            <input 
              type="text" 
              id="adminStockSearch" 
              placeholder="Search product stock or rack location..." 
              value="${this.stockSearchQuery}"
              style="padding: 6px 12px; border-radius: var(--radius-sm); border: 1px solid var(--border-color); font-size: 0.85rem; width: 260px;"
            />
          </div>

          <div style="overflow-x: auto;">
            <table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 0.85rem;">
              <thead>
                <tr style="border-bottom: 2px solid var(--border-color); background: var(--bg-main);">
                  <th style="padding: 10px;">Product Name</th>
                  <th style="padding: 10px;">Category</th>
                  <th style="padding: 10px;">Price</th>
                  <th style="padding: 10px;">Rack Loc</th>
                  <th style="padding: 10px;">Stock Qty</th>
                  <th style="padding: 10px;">Quick Stock Controls</th>
                </tr>
              </thead>
              <tbody>
                ${productsList.map(p => `
                  <tr style="border-bottom: 1px solid var(--border-color);">
                    <td style="padding: 10px; font-weight: 700;">
                      <div style="display: flex; align-items: center; gap: 8px;">
                        <img src="${p.image}" width="28" height="28" style="object-fit: contain;" />
                        <span>${p.title}</span>
                      </div>
                    </td>
                    <td style="padding: 10px; color: var(--text-muted);">${p.categoryId.replace('cat-', '')}</td>
                    <td style="padding: 10px; font-weight: 800;">₹${p.price}</td>
                    <td style="padding: 10px; font-family: monospace; font-size: 0.75rem;">${p.rack}</td>
                    <td style="padding: 10px;">
                      <span style="font-weight: 800; color: ${p.stock > 0 ? 'var(--color-brand)' : 'var(--color-danger)'};">
                        ${p.stock} units
                      </span>
                    </td>
                    <td style="padding: 10px;">
                      <div style="display: flex; gap: 6px;">
                        <button class="btn-stock-toggle" data-id="${p.id}" data-qty="0" style="background: #fca5a5; color: #991b1b; font-size: 0.7rem; font-weight: 800; padding: 4px 8px; border-radius: 4px;">Set 0 (Out of Stock)</button>
                        <button class="btn-stock-toggle" data-id="${p.id}" data-qty="50" style="background: #bbf7d0; color: #166534; font-size: 0.7rem; font-weight: 800; padding: 4px 8px; border-radius: 4px;">Set 50 (In Stock)</button>
                      </div>
                    </td>
                  </tr>
                `).join('')}
              </tbody>
            </table>
          </div>
        </div>
      </main>
    `;

    this.bindEvents();
  }

  bindEvents() {
    // Admin Stock Search
    const stockSearch = this.container.querySelector('#adminStockSearch');
    if (stockSearch) {
      stockSearch.addEventListener('input', (e) => {
        this.stockSearchQuery = e.target.value;
        this.render();
      });
    }

    // Status override dropdowns
    this.container.querySelectorAll('.admin-status-override').forEach(select => {
      select.addEventListener('change', (e) => {
        const orderId = e.currentTarget.dataset.orderId;
        const newStatus = e.target.value;
        store.updateOrderStatus(orderId, newStatus);
        alert(`Order #${orderId} status updated to ${newStatus}`);
      });
    });

    // Stock toggles
    this.container.querySelectorAll('.btn-stock-toggle').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const id = e.currentTarget.dataset.id;
        const qty = e.currentTarget.dataset.qty;
        store.toggleStock(id, qty);
      });
    });

    // Reset Demo State
    const resetBtn = this.container.querySelector('#resetDemoBtn');
    if (resetBtn) {
      resetBtn.addEventListener('click', () => {
        if (confirm('Are you sure you want to reset all demo state to initial defaults?')) {
          store.resetState();
          alert('Demo state reset successfully!');
        }
      });
    }
  }
}
