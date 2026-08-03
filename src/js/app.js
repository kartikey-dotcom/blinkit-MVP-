/* ==========================================================================
   App Entry Point - Component Instantiation, Routing & State Sync
   ========================================================================== */

import { store } from './store.js';
import { Header } from './components/Header.js';
import { CategoryNav } from './components/CategoryNav.js';
import { Catalog } from './components/Catalog.js';
import { CartDrawer } from './components/CartDrawer.js';
import { CheckoutModal } from './components/CheckoutModal.js';
import { OrderTracker } from './components/OrderTracker.js';
import { DarkStoreView } from './components/DarkStoreView.js';
import { RiderView } from './components/RiderView.js';
import { AdminView } from './components/AdminView.js';

class App {
  constructor() {
    this.cartDrawer = null;
    this.checkoutModal = null;
    this.orderTracker = null;
    this.init();
  }

  init() {
    // 1. Initialize Cart Drawer & Checkout Modal first to pass callbacks
    this.checkoutModal = new CheckoutModal('checkout-modal-container', (order) => {
      // Order placed callback
      console.log('Order placed successfully:', order);
    });

    this.cartDrawer = new CartDrawer('cart-drawer-container', () => {
      // Proceed to checkout callback
      this.checkoutModal.open();
    });

    // 2. Initialize Header
    new Header('header-container', () => {
      this.cartDrawer.open();
    });

    // 3. Initialize Category Nav & Catalog
    new CategoryNav('category-nav-container');
    new Catalog('catalog-container');

    // 4. Initialize Order Tracker
    this.orderTracker = new OrderTracker('order-tracker-container');

    // 5. Initialize Persona Views
    new DarkStoreView('picker-view-container');
    new RiderView('rider-view-container');
    new AdminView('admin-view-container');

    // 6. Listen to state changes for theme & view visibility
    store.subscribe((state) => this.handleStateChange(state));
    this.handleStateChange(store.getState());

    console.log('⚡ Blinkit Quick Commerce MVP initialized!');
  }

  handleStateChange(state) {
    // Apply theme
    document.documentElement.setAttribute('data-theme', state.theme);

    // Toggle Visibility of Consumer Sub-views
    const catalogContainer = document.getElementById('catalog-container');
    const categoryNavContainer = document.getElementById('category-nav-container');
    const trackerContainer = document.getElementById('order-tracker-container');

    if (state.activePersona === 'consumer') {
      if (state.orders.length > 0 && state.orders[0].orderStatus !== 'DELIVERED') {
        // Show tracker if there is an active non-delivered order
        if (trackerContainer) trackerContainer.style.display = 'block';
      } else {
        if (trackerContainer) trackerContainer.style.display = 'none';
      }
      if (catalogContainer) catalogContainer.style.display = 'block';
      if (categoryNavContainer) categoryNavContainer.style.display = 'block';
    } else {
      if (trackerContainer) trackerContainer.style.display = 'none';
      if (catalogContainer) catalogContainer.style.display = 'none';
      if (categoryNavContainer) categoryNavContainer.style.display = 'none';
    }
  }
}

// Bootstrap Application
document.addEventListener('DOMContentLoaded', () => {
  new App();
});
