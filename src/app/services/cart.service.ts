import { Injectable } from '@angular/core';
import { Product } from '../../app/models/products'; // Assurez-vous que l'interface Product est bien définie
import { BehaviorSubject, Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class CartService {

  private apiUrl = 'http://localhost:5000/cart'; // L'URL de l'API Flask

  // BehaviorSubject est utilisé pour maintenir et observer l'état du panier
  private cartItemsSubject = new BehaviorSubject<Product[]>([]);
  cartItems$ = this.cartItemsSubject.asObservable();

  constructor( private http : HttpClient){}

  getCartItems() :Observable<Product[]> {
    return this.http.get<Product[]>(this.apiUrl);
  }
  updateCart(cartItems: Product[]){}

  // // Récupérer les articles du panier actuel
  // getCartItems(): Product[] {
  //   return this.cartItemsSubject.getValue();
  // }

  // // Ajouter un produit au panier
  // addToCart(product: Product): void {
  //   const currentItems = this.getCartItems();
  //   const existingItem = currentItems.find(item => item.id === product.id);

  //   if (existingItem) {
  //     existingItem.quantity++;  // Augmenter la quantité si l'article est déjà dans le panier
  //   } else {
  //     currentItems.push({ ...product, quantity: 1 });  // Ajouter un nouvel article avec une quantité initiale de 1
  //   }

  //   this.cartItemsSubject.next(currentItems);  // Mettre à jour le panier
  // }

  // // Mettre à jour le panier
  // updateCart(items: Product[]): void {
  //   this.cartItemsSubject.next(items);
  // }

  // // Supprimer un article du panier
  // removeFromCart(productId: number): void {
  //   const updatedItems = this.getCartItems().filter(item => item.id !== productId);
  //   this.cartItemsSubject.next(updatedItems);
  // }

  // // Vider le panier
  // clearCart(): void {
  //   this.cartItemsSubject.next([]);
  // }

  // // Calculer le nombre total d'articles dans le panier
  // getTotalItems(): number {
  //   return this.getCartItems().reduce((total, item) => total + item.quantity, 0);
  // }

  // // Calculer le prix total du panier
  // getTotalPrice(): number {
  //   return this.getCartItems().reduce((total, item) => total + (item.price * item.quantity), 0);
  // }
}
