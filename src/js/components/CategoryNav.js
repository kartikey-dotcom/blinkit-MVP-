/* ==========================================================================
   Category Nav Component - Horizontal Scrollable Category Pills
   ========================================================================== */

import { store } from '../store.js';

export class CategoryNav {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
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

    this.container.innerHTML = `
      <div class="category-nav-section">
        <div class="category-nav-container">
          ${state.categories.map(cat => `
            <button 
              class="category-pill ${state.activeCategoryId === cat.id ? 'active' : ''}"
              data-cat-id="${cat.id}"
            >
              <span class="category-pill-icon">${cat.icon}</span>
              <span>${cat.name}</span>
            </button>
          `).join('')}
        </div>
      </div>
    `;

    this.bindEvents();
  }

  bindEvents() {
    this.container.querySelectorAll('.category-pill').forEach(pill => {
      pill.addEventListener('click', (e) => {
        const catId = e.currentTarget.dataset.catId;
        store.setCategory(catId);
      });
    });
  }
}
