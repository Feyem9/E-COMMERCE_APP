import { Injectable, Inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { BehaviorSubject, Observable, of, throwError, Subject } from 'rxjs';
import { catchError, map, tap, finalize, shareReplay } from 'rxjs/operators';
import { HttpClient } from '@angular/common/http';
import { Cart, Product } from '../models/products';
import { ApiService } from './api.service';
import { environment } from '../../environment/environment';
import { AnalyticsService } from './analytics.service';

@Injectable({
  providedIn: 'root'
})
export class CartService {
  private readonly CART_STORAGE_KEY = 'cart';
  private apiUrl = environment.apiUrl;

  // Cart items observable
  private cartItemsSubject = new BehaviorSubject<Cart[]>([]);
  public cartItems$ = this.cartItemsSubject.asObservable();

  // Cart count observable (quantité totale)
  private cartCountSubject = new BehaviorSubject<number>(0);
  public cartCount$ = this.cartCountSubject.asObservable();
 
  // Loading state
  private loadingSubject = new BehaviorSubject<boolean>(false);
  public loading$ = this.loadingSubject.asObservable();
 
  // Error state
  private errorSubject = new BehaviorSubject<string | null>(null);
  public error$ = this.errorSubject.asObservable();

  // Cache and refresh trigger
  private refreshTrigger$ = new Subject<void>();

  constructor(
    private http: HttpClient,
    private apiService: ApiService,
    private analytics: AnalyticsService,
    @Inject(PLATFORM_ID) private platformId: Object
  ) {
    // Only load from storage, don't call API here to prevent cascading subscriptions
    this.loadCartFromStorage();
  }

  /**
   * Charge les articles du panier depuis l'API avec cache
   * This observable is cached with shareReplay to prevent multiple simultaneous requests
   */
  private getCartItemsFromAPI(): Observable<Cart[]> {
    if (!this.apiService.isAuthenticated()) {
      this.updateCartState([]);
      return of([]);
    }

    this.loadingSubject.next(true);
    this.errorSubject.next(null);
    
    return this.apiService.get<Cart[]>('/cart/').pipe(
      tap((items: Cart[]) => {
        this.updateCartState(items);
        this.saveCartToStorage(items);
      }),
      catchError(error => {
        console.error('Error getting cart items:', error);
        this.setError('Erreur lors de la récupération du panier');
        return of(this.cartItemsSubject.value);
      }),
      finalize(() => this.loadingSubject.next(false)),
      shareReplay(1) // Cache the result to prevent multiple API calls
    );
  }
  /**
   * Returns cart items observable
   * Only call when explicitly needed by components
   */
  getCartItems(): Observable<Cart[]> {
    return this.getCartItemsFromAPI();
  }

  /**
   * Ajoute un produit au panier
   */
  addToCart(productId: number, quantity: number = 1): Observable<any> {
    if (quantity <= 0) {
      return throwError(() => new Error('La quantité doit être supérieure à 0'));
    }

    // Vérifier si l'utilisateur est authentifié - optionnel pour l'ajout au panier local
    // Les utilisateurs non authentifiés peuvent ajouter au panier local avant de se connecter
    
    this.loadingSubject.next(true);
    this.errorSubject.next(null);
    
    // Construire les données du panier
    const cartItem: any = {
      product_id: productId,
      quantity: quantity
    };
    
    // Si l'utilisateur est authentifié, le backend extraira l'ID du JWT
    // Sinon, ajouter l'ID client depuis le localStorage (session anonyme)
    if (!this.apiService.isAuthenticated()) {
      // Utiliser un ID de session pour les paniers anonymes
      let sessionId = typeof localStorage !== 'undefined' ? localStorage.getItem('session_id') : null;
      if (!sessionId) {
        sessionId = 'guest_' + Math.random().toString(36).substr(2, 9);
        if (typeof localStorage !== 'undefined') {
          localStorage.setItem('session_id', sessionId);
        }
      }
      cartItem.customer_id = sessionId;
    }

    // Inclure les en-têtes d'authentification
    const headers = this.apiService.getAuthHeaders();
    const options = { headers };

    return this.apiService.post<any>(`/product/add-to-cart-post/${productId}`, cartItem).pipe(
      tap((response) => {
        // Refresh cart without subscribing - let components handle their subscriptions
        this.refreshTrigger$.next();
        
        // 📊 Track event (if we have product info in storage)
        const items = this.cartItemsSubject.value;
        const item = items.find(i => i.product_id === productId);
        if (item) {
          this.analytics.trackAddToCart({
            ...item as any,
            quantity: quantity
          });
        } else {
          // Fallback simple
          this.analytics.trackEvent('add_to_cart', { id: productId, quantity });
        }
      }),
      catchError(error => {
        console.error('Error adding to cart:', error);
        this.setError('Impossible d\'ajouter l\'article au panier');
        return throwError(() => error);
      }),
      finalize(() => this.loadingSubject.next(false))
    );
  }

  /**
   * Met à jour la quantité d'un article
   */
  updateQuantity(cartId: number, newQuantity: number): Observable<any> {
    if (newQuantity <= 0) {
      return this.removeFromCart(cartId);
    }

    this.loadingSubject.next(true);
    this.errorSubject.next(null);

    const headers = this.apiService.getAuthHeaders();
    const options = { headers };

    return this.apiService.put<any>(`/cart/update-cart/${cartId}`, { quantity: newQuantity }).pipe(
      tap(() => {
        // Refresh cart without subscribing
        this.refreshTrigger$.next();
      }),
      catchError(error => {
        console.error('Error updating quantity:', error);
        this.setError('Impossible de mettre à jour la quantité');
        return throwError(() => error);
      }),
      finalize(() => this.loadingSubject.next(false))
    );
  }

  /**
   * Retire un article du panier
   */
  removeFromCart(cartId: number): Observable<any> {
    if (!this.apiService.isAuthenticated()) {
      this.setError('Vous devez vous connecter pour modifier le panier');
      return throwError(() => new Error('Utilisateur non authentifié'));
    }

    this.loadingSubject.next(true);
    this.errorSubject.next(null);

    const headers = this.apiService.getAuthHeaders();
    const options = { headers };

    return this.apiService.delete<any>(`/cart/delete-cart/${cartId}`).pipe(
      tap(() => {
        // 📊 Track event before refreshing
        const item = this.cartItemsSubject.value.find(i => i.id === cartId);
        if (item) {
          this.analytics.trackRemoveFromCart(item as any);
        }
        
        // Refresh cart without subscribing
        this.refreshTrigger$.next();
      }),
      catchError(error => {
        console.error('Error removing from cart:', error);
        this.setError('Impossible de retirer l\'article du panier');
        return throwError(() => error);
      }),
      finalize(() => this.loadingSubject.next(false))
    );
  }

  /**
   * Vide complètement le panier
   */
  clearCart(): Observable<any> {
    this.loadingSubject.next(true);
    this.errorSubject.next(null);
    
    // Si vous avez un endpoint API pour vider le panier
    // return this.apiService.delete<any>('/cart/clear').pipe(...)
    
    // Sinon, mise à jour locale
    this.updateCartState([]);
    this.clearCartFromStorage();
    this.loadingSubject.next(false);
    
    return of({ message: 'Panier vidé avec succès' });
  }

  /**
   * Calcule le total du panier (Observable)
   */
  getCartTotal(): Observable<number> {
    return this.cartItems$.pipe(
      map(items => this.calculateTotal(items))
    );
  }

  /**
   * Calcule le nombre total d'articles (Observable)
   */
  getCartCount(): Observable<number> {
    return this.cartItems$.pipe(
      map(items => this.calculateTotalQuantity(items))
    );
  }

  /**
   * Obtient le prix total (valeur synchrone)
   */
  getTotalPrice(): number {
    return this.calculateTotal(this.cartItemsSubject.value);
  }

  /**
   * Obtient le nombre total d'articles (valeur synchrone)
   */
  getCartItemsCount(): number {
    return this.calculateTotalQuantity(this.cartItemsSubject.value);
  }

  /**
   * Vérifie si un produit est dans le panier
   */
  isProductInCart(productId: number): boolean {
    return this.cartItemsSubject.value.some(item => item.product_id === productId);
  }

  /**
   * Obtient la quantité d'un produit dans le panier
   */
  getProductQuantity(productId: number): number {
    const item = this.cartItemsSubject.value.find(item => item.product_id === productId);
    return item ? item.quantity : 0;
  }

  // ========== Méthodes privées ==========

  /**
   * Met à jour l'état du panier (items et compteur)
   */
  private updateCartState(items: Cart[]): void {
    this.cartItemsSubject.next(items);
    const totalQuantity = this.calculateTotalQuantity(items);
    this.cartCountSubject.next(totalQuantity);
  }

  /**
   * Calcule le prix total
   */
  private calculateTotal(items: Cart[]): number {
    return items.reduce((total, item) => {
      const price = item.current_price || 0;
      return total + (price * item.quantity);
    }, 0);
  }

  /**
   * Calcule la quantité totale d'articles
   */
  private calculateTotalQuantity(items: Cart[]): number {
    return items.reduce((total, item) => total + item.quantity, 0);
  }

  /**
   * Définit un message d'erreur
   */
  private setError(message: string): void {
    this.errorSubject.next(message);
  }

  // ========== Gestion du localStorage ==========

    /**
   * Sauvegarde le panier dans le localStorage
   */
  private saveCartToStorage(items: Cart[]): void {
    if (!isPlatformBrowser(this.platformId)) {
      return; // Skip localStorage operations on server
    }
    
    try {
      localStorage.setItem(this.CART_STORAGE_KEY, JSON.stringify(items));
    } catch (error) {
      console.error('Error saving cart to storage:', error);
    }
  }

  /**
   * Charge le panier depuis le localStorage
   */
  private loadCartFromStorage(): void {
    if (!isPlatformBrowser(this.platformId)) {
      this.updateCartState([]); // Initialize with empty cart on server
      return;
    }
    
    try {
      const saved = localStorage.getItem(this.CART_STORAGE_KEY);
      if (saved) {
        const items: Cart[] = JSON.parse(saved);
        this.updateCartState(items);
      }
    } catch (error) {
      console.error('Error loading cart from storage:', error);
      this.updateCartState([]);
    }
  }

  /**
   * Efface le panier du localStorage
   */
  private clearCartFromStorage(): void {
    if (!isPlatformBrowser(this.platformId)) {
      return; // Skip localStorage operations on server
    }
    
    try {
      localStorage.removeItem(this.CART_STORAGE_KEY);
    } catch (error) {
      console.error('Error clearing cart from storage:', error);
    }
  }

  /**
   * Met à jour le nombre d'articles dans le panier
   */
  public updateCartCount(count: number): void {
    this.cartCountSubject.next(count);
  }

  /**
   * Gets refresh trigger for components that need to reload cart
   */
  getRefreshTrigger(): Observable<void> {
    return this.refreshTrigger$.asObservable();
  }
}
    