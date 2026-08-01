/* ==========================================================================
   Blinkit Quick Commerce MVP - Centralized Reactive State Store
   ========================================================================== */

import { MOCK_DATA } from './mockData.js';

const STORAGE_KEY = 'blinkit_mvp_store_v1';

class Store {
  constructor() {
    this.listeners = [];
    this.state = this.loadInitialState();
  }

  loadInitialState() {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        // Ensure products and categories fall back to fresh mock data if structure changed
        return {
          ...parsed,
          products: parsed.products && parsed.products.length ? parsed.products : MOCK_DATA.products,
          categories: MOCK_DATA.categories,
          darkStores: MOCK_DATA.darkStores,
          riders: MOCK_DATA.riders
        };
      } catch (e) {
        console.warn('Failed to load saved state, using default mock data', e);
      }
    }

    return {
      activePersona: 'consumer', // 'consumer' | 'picker' | 'rider' | 'admin'
      theme: 'light',
      activeDarkStoreId: 'ds-104',
      activeCategoryId: 'cat-all',
      searchQuery: '',
      cart: {}, // { 'p-101': 2, 'p-201': 1 }
      appliedCoupon: null, // { code: 'BLINKIT100', discount: 100 }
      orders: [
        {
          id: 'BLK-892401',
          userId: 'usr-1',
          darkStoreId: 'ds-104',
          items: [
            { id: 'p-101', title: 'Fresh Farm Tomatoes', unit: '500 g', price: 24, quantity: 2, rack: 'Aisle 1 • Shelf A1' },
            { id: 'p-201', title: 'Amul Taaza Toned Milk', unit: '500 ml', price: 27, quantity: 1, rack: 'Cold Refrigerator #1' }
          ],
          itemTotal: 75,
          deliveryFee: 0,
          surgeFee: 5,
          discount: 0,
          totalAmount: 80,
          paymentMethod: 'UPI',
          paymentStatus: 'PAID',
          orderStatus: 'PLACED', // PLACED -> PACKING -> PACKED -> DISPATCHED -> ON_THE_WAY -> DELIVERED
          otp: '4819',
          address: '104 Park View Apartments, 12th Main, Indiranagar',
          deliveryLat: 12.972500,
          deliveryLng: 77.595000,
          riderId: 'r-101',
          riderLat: 12.971598,
          riderLng: 77.594566,
          createdAt: new Date().toISOString()
        }
      ],
      activeOrderId: 'BLK-892401',
      products: [...MOCK_DATA.products],
      categories: [...MOCK_DATA.categories],
      darkStores: [...MOCK_DATA.darkStores],
      riders: [...MOCK_DATA.riders],
      userAddresses: [...MOCK_DATA.userAddresses]
    };
  }

  saveState() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(this.state));
    } catch (e) {
      console.error('Failed to save store state to localStorage', e);
    }
  }

  getState() {
    return this.state;
  }

  subscribe(listener) {
    this.listeners.push(listener);
    return () => {
      this.listeners = this.listeners.filter(l => l !== listener);
    };
  }

  notify() {
    this.saveState();
    this.listeners.forEach(listener => listener(this.state));
  }

  // --- Actions ---

  setPersona(persona) {
    this.state.activePersona = persona;
    this.notify();
  }

  toggleTheme() {
    this.state.theme = this.state.theme === 'light' ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', this.state.theme);
    this.notify();
  }

  setCategory(categoryId) {
    this.state.activeCategoryId = categoryId;
    this.notify();
  }

  setSearchQuery(query) {
    this.state.searchQuery = query;
    this.notify();
  }

  addToCart(productId) {
    const currentQty = this.state.cart[productId] || 0;
    const product = this.state.products.find(p => p.id === productId);
    if (!product || product.stock <= currentQty) {
      return false; // Stock limit reached
    }
    this.state.cart[productId] = currentQty + 1;
    this.notify();
    return true;
  }

  removeFromCart(productId) {
    const currentQty = this.state.cart[productId] || 0;
    if (currentQty <= 1) {
      delete this.state.cart[productId];
    } else {
      this.state.cart[productId] = currentQty - 1;
    }
    this.notify();
  }

  updateCartQty(productId, qty) {
    if (qty <= 0) {
      delete this.state.cart[productId];
    } else {
      const product = this.state.products.find(p => p.id === productId);
      if (product && product.stock >= qty) {
        this.state.cart[productId] = qty;
      }
    }
    this.notify();
  }

  clearCart() {
    this.state.cart = {};
    this.state.appliedCoupon = null;
    this.notify();
  }

  applyCoupon(code) {
    const upper = code.trim().toUpperCase();
    let discount = 0;
    if (upper === 'BLINKIT100') discount = 100;
    else if (upper === 'WELCOME50') discount = 50;
    else if (upper === 'FREE10') discount = 25;
    else {
      return { success: false, message: 'Invalid coupon code' };
    }

    this.state.appliedCoupon = { code: upper, discount };
    this.notify();
    return { success: true, message: `Coupon ${upper} applied! Saved ₹${discount}` };
  }

  removeCoupon() {
    this.state.appliedCoupon = null;
    this.notify();
  }

  placeOrder({ addressId, paymentMethod }) {
    const cartEntries = Object.entries(this.state.cart);
    if (!cartEntries.length) return null;

    const addressObj = this.state.userAddresses.find(a => a.id === addressId) || this.state.userAddresses[0];

    // Compute bill breakdown
    let itemTotal = 0;
    const orderItems = [];

    cartEntries.forEach(([prodId, qty]) => {
      const p = this.state.products.find(item => item.id === prodId);
      if (p) {
        itemTotal += p.price * qty;
        orderItems.push({
          id: p.id,
          title: p.title,
          unit: p.unit,
          price: p.price,
          quantity: qty,
          rack: p.rack
        });
        // Deduct stock atomically
        p.stock = Math.max(0, p.stock - qty);
      }
    });

    const deliveryFee = itemTotal >= 199 ? 0 : 25;
    const surgeFee = 5;
    const discount = this.state.appliedCoupon ? this.state.appliedCoupon.discount : 0;
    const totalAmount = Math.max(0, itemTotal + deliveryFee + surgeFee - discount);

    const orderId = `BLK-${Math.floor(100000 + Math.random() * 900000)}`;
    const otp = `${Math.floor(1000 + Math.random() * 9000)}`;

    const newOrder = {
      id: orderId,
      userId: 'usr-1',
      darkStoreId: this.state.activeDarkStoreId,
      items: orderItems,
      itemTotal,
      deliveryFee,
      surgeFee,
      discount,
      totalAmount,
      paymentMethod: paymentMethod || 'UPI',
      paymentStatus: 'PAID',
      orderStatus: 'PLACED',
      otp,
      address: `${addressObj.street}, ${addressObj.landmark}`,
      deliveryLat: addressObj.lat,
      deliveryLng: addressObj.lng,
      riderId: 'r-101',
      riderLat: 12.971598,
      riderLng: 77.594566,
      createdAt: new Date().toISOString()
    };

    this.state.orders.unshift(newOrder);
    this.state.activeOrderId = orderId;
    this.state.cart = {};
    this.state.appliedCoupon = null;

    this.notify();
    return newOrder;
  }

  updateOrderStatus(orderId, newStatus) {
    const order = this.state.orders.find(o => o.id === orderId);
    if (order) {
      order.orderStatus = newStatus;
      this.notify();
    }
  }

  updateRiderLocation(orderId, lat, lng) {
    const order = this.state.orders.find(o => o.id === orderId);
    if (order) {
      order.riderLat = lat;
      order.riderLng = lng;
      this.notify();
    }
  }

  toggleStock(productId, stockQty) {
    const p = this.state.products.find(item => item.id === productId);
    if (p) {
      p.stock = parseInt(stockQty, 10);
      this.notify();
    }
  }

  resetState() {
    localStorage.removeItem(STORAGE_KEY);
    this.state = this.loadInitialState();
    document.documentElement.setAttribute('data-theme', 'light');
    this.notify();
  }
}

export const store = new Store();
