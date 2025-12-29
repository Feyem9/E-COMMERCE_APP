import { Injectable, Inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { Router, NavigationEnd } from '@angular/router';
import { filter } from 'rxjs/operators';

declare let gtag: Function;

@Injectable({
  providedIn: 'root'
})
export class AnalyticsService {
  private isBrowser: boolean;
  private initialized = false;

  constructor(
    @Inject(PLATFORM_ID) platformId: Object,
    private router: Router
  ) {
    this.isBrowser = isPlatformBrowser(platformId);
  }

  /**
   * Initialise Google Analytics avec le Measurement ID
   */
  init(measurementId: string): void {
    if (!this.isBrowser || this.initialized) return;

    // Créer les scripts Google Analytics
    const script1 = document.createElement('script');
    script1.async = true;
    script1.src = `https://www.googletagmanager.com/gtag/js?id=${measurementId}`;

    const script2 = document.createElement('script');
    script2.innerHTML = `
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', '${measurementId}', {
        page_path: window.location.pathname,
        send_page_view: true
      });
    `;

    document.head.appendChild(script1);
    document.head.appendChild(script2);

    // Tracker les changements de page automatiquement
    this.router.events.pipe(
      filter(event => event instanceof NavigationEnd)
    ).subscribe((event: any) => {
      this.trackPageView(event.urlAfterRedirects);
    });

    this.initialized = true;
    console.log('📊 Analytics initialized');
  }

  /**
   * Tracker une vue de page
   */
  trackPageView(url: string): void {
    if (!this.isBrowser || typeof gtag === 'undefined') return;

    gtag('config', 'GA_MEASUREMENT_ID', {
      page_path: url
    });
  }

  /**
   * Tracker un événement personnalisé
   */
  trackEvent(
    eventName: string,
    eventParams: { [key: string]: any } = {}
  ): void {
    if (!this.isBrowser || typeof gtag === 'undefined') {
      console.log(`📊 Event (offline): ${eventName}`, eventParams);
      return;
    }

    gtag('event', eventName, eventParams);
    console.log(`📊 Event tracked: ${eventName}`, eventParams);
  }

  // ============================================
  // ÉVÉNEMENTS E-COMMERCE PRÉ-DÉFINIS
  // ============================================

  /**
   * Tracker l'ajout au panier
   */
  trackAddToCart(product: {
    id: number | string;
    name: string;
    price: number;
    quantity?: number;
    category?: string;
  }): void {
    this.trackEvent('add_to_cart', {
      currency: 'XAF',
      value: product.price * (product.quantity || 1),
      items: [{
        item_id: product.id.toString(),
        item_name: product.name,
        price: product.price,
        quantity: product.quantity || 1,
        item_category: product.category || 'Products'
      }]
    });
  }

  /**
   * Tracker la suppression du panier
   */
  trackRemoveFromCart(product: {
    id: number | string;
    name: string;
    price: number;
    quantity?: number;
  }): void {
    this.trackEvent('remove_from_cart', {
      currency: 'XAF',
      value: product.price * (product.quantity || 1),
      items: [{
        item_id: product.id.toString(),
        item_name: product.name,
        price: product.price,
        quantity: product.quantity || 1
      }]
    });
  }

  /**
   * Tracker le début du checkout
   */
  trackBeginCheckout(cart: {
    items: Array<{ id: number | string; name: string; price: number; quantity: number }>;
    total: number;
  }): void {
    this.trackEvent('begin_checkout', {
      currency: 'XAF',
      value: cart.total,
      items: cart.items.map(item => ({
        item_id: item.id.toString(),
        item_name: item.name,
        price: item.price,
        quantity: item.quantity
      }))
    });
  }

  /**
   * Tracker un achat réussi
   */
  trackPurchase(order: {
    transactionId: string;
    value: number;
    items: Array<{ id: number | string; name: string; price: number; quantity: number }>;
    shipping?: number;
    tax?: number;
  }): void {
    this.trackEvent('purchase', {
      transaction_id: order.transactionId,
      value: order.value,
      currency: 'XAF',
      shipping: order.shipping || 0,
      tax: order.tax || 0,
      items: order.items.map(item => ({
        item_id: item.id.toString(),
        item_name: item.name,
        price: item.price,
        quantity: item.quantity
      }))
    });
  }

  /**
   * Tracker une vue de produit
   */
  trackViewProduct(product: {
    id: number | string;
    name: string;
    price: number;
    category?: string;
  }): void {
    this.trackEvent('view_item', {
      currency: 'XAF',
      value: product.price,
      items: [{
        item_id: product.id.toString(),
        item_name: product.name,
        price: product.price,
        item_category: product.category || 'Products'
      }]
    });
  }

  /**
   * Tracker une recherche
   */
  trackSearch(searchTerm: string): void {
    this.trackEvent('search', {
      search_term: searchTerm
    });
  }

  /**
   * Tracker une inscription
   */
  trackSignUp(method: string = 'email'): void {
    this.trackEvent('sign_up', {
      method: method
    });
  }

  /**
   * Tracker une connexion
   */
  trackLogin(method: string = 'email'): void {
    this.trackEvent('login', {
      method: method
    });
  }

  /**
   * Tracker un partage
   */
  trackShare(contentType: string, itemId: string): void {
    this.trackEvent('share', {
      content_type: contentType,
      item_id: itemId
    });
  }

  /**
   * Tracker une erreur
   */
  trackError(error: {
    description: string;
    fatal?: boolean;
  }): void {
    this.trackEvent('exception', error);
  }
}
