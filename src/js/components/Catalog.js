/* ==========================================================================
   Catalog Component - Enhanced Product Grid, Sorting & Image Fallbacks
   ========================================================================== */

import { store } from '../store.js';

export class Catalog {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.sortBy = 'relevance';
    this.init();
  }

  init() {
    store.subscribe(() => this.render());
    this.render();
  }

  render() {
    const state = store.getState();
    if (state.activePersona !== 'consumer') {
      this.container.style.display = 'none';
      return;
    }
    this.container.style.display = 'block';

    let filtered = [...state.products];

    if (state.activeCategoryId && state.activeCategoryId !== 'cat-all') {
      filtered = filtered.filter(p => p.categoryId === state.activeCategoryId);
    }

    if (state.searchQuery.trim()) {
      const q = state.searchQuery.trim().toLowerCase();
      filtered = filtered.filter(p => 
        p.title.toLowerCase().includes(q) ||
        p.tags.some(t => t.toLowerCase().includes(q))
      );
    }

    // Apply Sorting
    if (this.sortBy === 'price-low') {
      filtered.sort((a, b) => a.price - b.price);
    } else if (this.sortBy === 'price-high') {
      filtered.sort((a, b) => b.price - a.price);
    } else if (this.sortBy === 'discount') {
      filtered.sort((a, b) => {
        const discA = ((a.mrp - a.price) / a.mrp);
        const discB = ((b.mrp - b.price) / b.mrp);
        return discB - discA;
      });
    }

    const activeCatObj = state.categories.find(c => c.id === state.activeCategoryId) || state.categories[0];

    const svgFallback = `data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='200' height='200' viewBox='0 0 200 200'><rect width='200' height='200' fill='%23f1f5f9' rx='16'/><text x='50%' y='50%' dominant-baseline='central' text-anchor='middle' font-size='50'>🛍️</text></svg>`;

    this.container.innerHTML = `
      <main class="main-layout">
        <!-- Hero Category Banner -->
        <div style="background: linear-gradient(135deg, #0c831f, #096818); color: #fff; padding: 20px 24px; border-radius: var(--radius-lg); margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; box-shadow: var(--shadow-md);">
          <div>
            <span style="background: var(--color-accent); color: #000; font-size: 0.7rem; font-weight: 900; padding: 2px 8px; border-radius: 4px; text-transform: uppercase;">
              ⚡ 10 MINUTE DELIVERY GUARANTEE
            </span>
            <h2 style="font-family: var(--font-heading); font-weight: 800; font-size: 1.6rem; margin-top: 6px;">
              ${activeCatObj.icon} ${state.searchQuery ? `Search Results for "${state.searchQuery}"` : activeCatObj.name}
            </h2>
            <p style="font-size: 0.85rem; opacity: 0.9; margin-top: 2px;">
              Fresh essentials delivered instantly from Dark Store #104 (Indiranagar)
            </p>
          </div>
        </div>

        <div class="catalog-header">
          <div class="catalog-title">
            <span class="catalog-count">Showing <strong>${filtered.length}</strong> items</span>
          </div>

          <!-- Sorting Controls -->
          <div style="display: flex; align-items: center; gap: 8px;">
            <label style="font-size: 0.82rem; font-weight: 700; color: var(--text-muted);">Sort By:</label>
            <select id="sortSelect" style="padding: 6px 12px; border-radius: var(--radius-sm); border: 1px solid var(--border-color); background: var(--bg-surface); color: var(--text-main); font-weight: 600;">
              <option value="relevance" ${this.sortBy === 'relevance' ? 'selected' : ''}>Relevance</option>
              <option value="price-low" ${this.sortBy === 'price-low' ? 'selected' : ''}>Price: Low to High</option>
              <option value="price-high" ${this.sortBy === 'price-high' ? 'selected' : ''}>Price: High to Low</option>
              <option value="discount" ${this.sortBy === 'discount' ? 'selected' : ''}>Highest Discount</option>
            </select>
          </div>
        </div>

        ${filtered.length === 0 ? `
          <div style="text-align: center; padding: 60px 20px; background: var(--bg-surface); border-radius: var(--radius-lg); border: 1px solid var(--border-color);">
            <div style="font-size: 3rem; margin-bottom: 12px;">🔍</div>
            <h3 style="font-weight: 800; font-size: 1.2rem; margin-bottom: 8px;">No items match your search</h3>
            <p style="color: var(--text-muted); font-size: 0.9rem;">Try searching for "Milk", "Tomatoes", "Chips", or click another category.</p>
          </div>
        ` : `
          <div class="product-grid">
            ${filtered.map(product => this.renderProductCard(product, state.cart, svgFallback)).join('')}
          </div>
        `}
      </main>
    `;

    this.bindEvents();
  }

  renderProductCard(product, cart, svgFallback) {
    const qtyInCart = cart[product.id] || 0;
    const isOutOfStock = product.stock <= 0;
    const discountPct = Math.round(((product.mrp - product.price) / product.mrp) * 100);

    return `
      <div class="product-card ${isOutOfStock ? 'out-of-stock' : ''}" data-product-id="${product.id}">
        <span class="product-badge-express">⚡ 8 MINS</span>
        ${discountPct > 0 ? `<span class="product-discount-tag">${discountPct}% OFF</span>` : ''}

        ${isOutOfStock ? `
          <div class="out-of-stock-overlay">
            <span class="out-of-stock-badge">OUT OF STOCK</span>
          </div>
        ` : ''}

        <div class="product-image-container">
          <img 
            src="${product.image}" 
            alt="${product.title}" 
            class="product-image" 
            loading="lazy" 
            onerror="this.onerror=null; this.src='${svgFallback}';"
          />
        </div>

        <div class="product-info">
          <span class="product-rack-tag">📍 ${product.rack}</span>
          <h4 class="product-title">${product.title}</h4>
          <span class="product-unit">${product.unit}</span>

          <div class="product-footer">
            <div class="price-box">
              <span class="price-discounted">₹${product.price}</span>
              ${product.mrp > product.price ? `<span class="price-mrp">₹${product.mrp}</span>` : ''}
            </div>

            <div class="cart-action-wrapper">
              ${qtyInCart > 0 ? `
                <div class="stepper-container">
                  <button class="stepper-btn btn-minus" data-id="${product.id}">−</button>
                  <span class="stepper-count">${qtyInCart}</span>
                  <button class="stepper-btn btn-plus" data-id="${product.id}" ${qtyInCart >= product.stock ? 'disabled style="opacity:0.4"' : ''}>+</button>
                </div>
              ` : `
                <button class="btn-add-cart" data-id="${product.id}" ${isOutOfStock ? 'disabled style="opacity:0.5; cursor:not-allowed;"' : ''}>
                  ADD
                </button>
              `}
            </div>
          </div>
        </div>
      </div>
    `;
  }

  bindEvents() {
    const sortSelect = this.container.querySelector('#sortSelect');
    if (sortSelect) {
      sortSelect.addEventListener('change', (e) => {
        this.sortBy = e.target.value;
        this.render();
      });
    }

    this.container.querySelectorAll('.btn-add-cart').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const id = e.currentTarget.dataset.id;
        store.addToCart(id);
      });
    });

    this.container.querySelectorAll('.btn-plus').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const id = e.currentTarget.dataset.id;
        store.addToCart(id);
      });
    });

    this.container.querySelectorAll('.btn-minus').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const id = e.currentTarget.dataset.id;
        store.removeFromCart(id);
      });
    });
  }
}
