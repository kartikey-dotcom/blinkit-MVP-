/* ==========================================================================
   Footer Component - Responsive Desktop Web Page Footer
   ========================================================================== */

import { store } from '../store.js';

export class Footer {
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
      <footer class="desktop-footer">
        <div class="footer-container">
          <div class="footer-grid">
            <!-- Column 1: Brand & App Links -->
            <div class="footer-col brand-col">
              <div class="footer-brand">
                <span class="footer-logo">blinkit</span>
                <span class="footer-badge">MVP</span>
              </div>
              <p class="footer-tagline">India's Last Minute App — 10 Minute Grocery & Instant Needs Delivery</p>
              <div class="app-badges">
                <a href="#" class="app-btn">
                  <span>📱 App Store</span>
                </a>
                <a href="#" class="app-btn">
                  <span>🤖 Google Play</span>
                </a>
              </div>
            </div>

            <!-- Column 2: Popular Categories -->
            <div class="footer-col">
              <h4 class="footer-heading">Categories</h4>
              <ul class="footer-links">
                <li><a href="#">Fresh Vegetables & Fruits</a></li>
                <li><a href="#">Dairy, Bread & Eggs</a></li>
                <li><a href="#">Munchies & Snacks</a></li>
                <li><a href="#">Cold Drinks & Juices</a></li>
                <li><a href="#">Instant & Frozen Food</a></li>
                <li><a href="#">Tea, Coffee & Health Drinks</a></li>
              </ul>
            </div>

            <!-- Column 3: Quick Commerce Dark Stores -->
            <div class="footer-col">
              <h4 class="footer-heading">Dark Store Hubs</h4>
              <ul class="footer-links">
                <li><a href="#">DLF Phase 3 (Hub #104)</a></li>
                <li><a href="#">Indiranagar Dark Store</a></li>
                <li><a href="#">Koramangala 4th Block</a></li>
                <li><a href="#">Powai Tech Park Hub</a></li>
                <li><a href="#">Cyber City Express</a></li>
              </ul>
            </div>

            <!-- Column 4: Customer Support & Corporate -->
            <div class="footer-col">
              <h4 class="footer-heading">Company & Help</h4>
              <ul class="footer-links">
                <li><a href="#">About Us</a></li>
                <li><a href="#">Careers & Culture</a></li>
                <li><a href="#">Partner With Us</a></li>
                <li><a href="#">10-Min Delivery Terms</a></li>
                <li><a href="#">Privacy Policy</a></li>
                <li><a href="#">24x7 Customer Support</a></li>
              </ul>
            </div>
          </div>

          <div class="footer-bottom">
            <div class="footer-copy">
              © ${new Date().getFullYear()} Blinkit Quick Commerce MVP. Built for ultra-fast grocery delivery. All rights reserved.
            </div>
            <div class="footer-payment-badges">
              <span>💳 UPI</span>
              <span>⚡ Face ID</span>
              <span>🔒 100% Encrypted</span>
            </div>
          </div>
        </div>
      </footer>
    `;
  }
}
