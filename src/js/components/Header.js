/* ==========================================================================
   Header Component - Enhanced Multi-Persona Switcher, Location Modal & Search Engine
   ========================================================================== */

import { store } from '../store.js';

export class Header {
  constructor(containerId, onOpenCart) {
    this.container = document.getElementById(containerId);
    this.onOpenCart = onOpenCart;
    this.showLocationModal = false;
    this.init();
  }

  init() {
    store.subscribe(() => this.render());
    this.setupGlobalShortcuts();
    this.render();
  }

  setupGlobalShortcuts() {
    document.addEventListener('keydown', (e) => {
      // Focus search on '/' press when not typing in an input
      if (e.key === '/' && document.activeElement.tagName !== 'INPUT') {
        e.preventDefault();
        const searchInput = this.container.querySelector('#searchInput');
        if (searchInput) searchInput.focus();
      }
    });
  }

  render() {
    const state = store.getState();
    const cartCount = Object.values(state.cart).reduce((sum, qty) => sum + qty, 0);

    const activeDarkStore = state.darkStores.find(ds => ds.id === state.activeDarkStoreId) || state.darkStores[0];
    const defaultAddr = state.userAddresses.find(a => a.isDefault) || state.userAddresses[0];

    // Compute search suggestions if query exists
    let suggestions = [];
    if (state.searchQuery.trim().length > 1) {
      const q = state.searchQuery.trim().toLowerCase();
      suggestions = state.products.filter(p => 
        p.title.toLowerCase().includes(q) || 
        p.tags.some(t => t.toLowerCase().includes(q))
      ).slice(0, 5);
    }

    this.container.innerHTML = `
      <!-- Top Persona Selector Bar -->
      <div class="persona-bar">
        <div class="persona-switcher">
          <button class="persona-btn ${state.activePersona === 'consumer' ? 'active' : ''}" data-persona="consumer">
            🛒 Consumer Storefront
          </button>
          <button class="persona-btn ${state.activePersona === 'picker' ? 'active' : ''}" data-persona="picker">
            📦 Dark Store Picker Portal
          </button>
          <button class="persona-btn ${state.activePersona === 'rider' ? 'active' : ''}" data-persona="rider">
            🛵 Rider Partner App
          </button>
          <button class="persona-btn ${state.activePersona === 'admin' ? 'active' : ''}" data-persona="admin">
            📊 Admin Dashboard
          </button>
        </div>
        <div>
          <span>Hub: <strong>${activeDarkStore.code}</strong> (${activeDarkStore.name.split('-')[1].trim()})</span>
        </div>
      </div>

      <!-- Main Sticky Navigation Header -->
      <header class="main-header">
        <div class="header-container">
          <div class="brand-section">
            <div class="brand-logo" id="logoClick" title="Blinkit Quick Commerce">
              blinkit <span class="brand-badge">MVP</span>
            </div>

            ${state.activePersona === 'consumer' ? `
              <div class="location-picker" id="locationPickerBtn" title="Click to change location">
                <div class="delivery-time-badge">
                  <span class="flash-icon">⚡</span> 10 MINS
                </div>
                <div class="location-address">
                  <strong>${defaultAddr.label}</strong> - ${defaultAddr.street}
                </div>
                <span style="font-size: 0.8rem; color: var(--text-muted);">▼</span>
              </div>
            ` : ''}
          </div>

          ${state.activePersona === 'consumer' ? `
            <div class="search-container">
              <div class="search-input-wrapper">
                <span style="color: var(--text-muted); font-size: 1.1rem;">🔍</span>
                <input 
                  type="text" 
                  class="search-input" 
                  id="searchInput"
                  placeholder="Search 'milk', 'tomatoes', 'chips', 'maggie'... (Press '/' to focus)" 
                  value="${state.searchQuery}"
                  autocomplete="off"
                />
                ${state.searchQuery ? `
                  <button id="clearSearchBtn" style="color: var(--text-muted); font-weight: bold; padding: 0 6px;">✕</button>
                ` : '<kbd style="font-size: 0.7rem; background: var(--bg-main); padding: 2px 6px; border-radius: 4px; color: var(--text-muted); font-family: monospace;">/</kbd>'}
              </div>

              ${suggestions.length > 0 ? `
                <div style="position: absolute; top: 100%; left: 0; right: 0; background: var(--bg-surface); border: 1px solid var(--border-color); border-radius: var(--radius-md); box-shadow: var(--shadow-md); margin-top: 6px; z-index: 150; overflow: hidden;">
                  <div style="padding: 8px 12px; font-size: 0.75rem; font-weight: 800; color: var(--text-muted); background: var(--bg-main); text-transform: uppercase;">
                    Instant Suggestions (${suggestions.length})
                  </div>
                  ${suggestions.map(item => `
                    <div 
                      class="search-suggestion-item" 
                      data-title="${item.title}"
                      style="padding: 10px 14px; display: flex; align-items: center; justify-content: space-between; cursor: pointer; border-bottom: 1px solid var(--border-color); transition: background 0.15s ease;"
                    >
                      <div style="display: flex; align-items: center; gap: 10px;">
                        <img src="${item.image}" width="28" height="28" style="object-fit: contain;" />
                        <span style="font-size: 0.88rem; font-weight: 700;">${item.title}</span>
                      </div>
                      <span style="font-size: 0.82rem; font-weight: 800; color: var(--color-brand);">₹${item.price}</span>
                    </div>
                  `).join('')}
                </div>
              ` : ''}
            </div>
          ` : ''}

          <div class="header-actions">
            <button class="btn-theme-toggle" id="themeToggleBtn" title="Toggle Dark/Light Mode">
              ${state.theme === 'dark' ? '☀️' : '🌙'}
            </button>

            ${state.activePersona === 'consumer' ? `
              <button class="btn-cart" id="openCartBtn">
                <span>🛒</span>
                <span>Cart</span>
                ${cartCount > 0 ? `<span class="cart-count-badge">${cartCount}</span>` : ''}
              </button>
            ` : ''}
          </div>
        </div>
      </header>

      <!-- Location Selector Modal -->
      ${this.showLocationModal ? `
        <div class="modal-backdrop active" id="locationModalBackdrop">
          <div class="modal-card" style="max-width: 440px;">
            <div class="modal-header">
              <h3 style="font-family: var(--font-heading); font-weight: 800;">📍 Change Delivery Location</h3>
              <button id="closeLocationModalBtn" style="font-size: 1.2rem; color: var(--text-muted);">✕</button>
            </div>
            <div class="modal-body">
              <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 14px;">Select address to calculate dark store 10-minute delivery feasibility:</p>
              <div style="display: flex; flex-direction: column; gap: 10px;">
                ${state.userAddresses.map(addr => `
                  <div 
                    class="payment-card ${addr.isDefault ? 'selected' : ''}" 
                    data-select-addr-id="${addr.id}"
                  >
                    <span style="font-size: 1.4rem;">${addr.label === 'Home' ? '🏠' : '🏢'}</span>
                    <div>
                      <strong style="font-size: 0.9rem;">${addr.label}</strong>
                      <p style="font-size: 0.78rem; color: var(--text-muted); line-height: 1.2;">${addr.street}</p>
                      <span style="font-size: 0.7rem; color: var(--color-brand); font-weight: 800;">⚡ Served by Indiranagar DS-104</span>
                    </div>
                  </div>
                `).join('')}
              </div>
            </div>
          </div>
        </div>
      ` : ''}
    `;

    this.bindEvents();
  }

  bindEvents() {
    // Persona switching
    this.container.querySelectorAll('.persona-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const persona = e.currentTarget.dataset.persona;
        store.setPersona(persona);
      });
    });

    // Theme toggle
    const themeBtn = this.container.querySelector('#themeToggleBtn');
    if (themeBtn) {
      themeBtn.addEventListener('click', () => store.toggleTheme());
    }

    // Logo click reset
    const logo = this.container.querySelector('#logoClick');
    if (logo) {
      logo.addEventListener('click', () => {
        store.setCategory('cat-all');
        store.setSearchQuery('');
        store.setPersona('consumer');
      });
    }

    // Open Cart Drawer
    const cartBtn = this.container.querySelector('#openCartBtn');
    if (cartBtn) {
      cartBtn.addEventListener('click', () => {
        if (this.onOpenCart) this.onOpenCart();
      });
    }

    // Search input
    const searchInput = this.container.querySelector('#searchInput');
    if (searchInput) {
      searchInput.addEventListener('input', (e) => {
        store.setSearchQuery(e.target.value);
      });
    }

    const clearSearchBtn = this.container.querySelector('#clearSearchBtn');
    if (clearSearchBtn) {
      clearSearchBtn.addEventListener('click', () => {
        store.setSearchQuery('');
      });
    }

    // Search suggestion click
    this.container.querySelectorAll('.search-suggestion-item').forEach(item => {
      item.addEventListener('click', (e) => {
        const title = e.currentTarget.dataset.title;
        store.setSearchQuery(title);
      });
    });

    // Location Modal toggle
    const locBtn = this.container.querySelector('#locationPickerBtn');
    if (locBtn) {
      locBtn.addEventListener('click', () => {
        this.showLocationModal = true;
        this.render();
      });
    }

    const closeLocBtn = this.container.querySelector('#closeLocationModalBtn');
    if (closeLocBtn) {
      closeLocBtn.addEventListener('click', () => {
        this.showLocationModal = false;
        this.render();
      });
    }

    this.container.querySelectorAll('[data-select-addr-id]').forEach(card => {
      card.addEventListener('click', (e) => {
        const addrId = e.currentTarget.dataset.selectAddrId;
        const state = store.getState();
        state.userAddresses.forEach(a => a.isDefault = (a.id === addrId));
        this.showLocationModal = false;
        store.notify();
      });
    });
  }
}
