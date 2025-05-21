import { Injectable } from '@angular/core';
import { Cart, Product } from '../../app/models/products'; // Assurez-vous que l'interface Product est bien définie
import { BehaviorSubject, catchError, Observable, switchMap, throwError } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { AuthService } from '../customers/auth.service';

@Injectable({
  providedIn: 'root'
})
export class CartService {

  private apiUrl = 'http://localhost:5000/product/add-to-cart-post/'; // L'URL de l'API Flask
  private url = 'http://localhost:5000/cart'
  private paymentUrl = 'http://localhost:5000/api/pay'; // Change selon ton URL

  // BehaviorSubject est utilisé pour maintenir et observer l'état du panier
  private cartItemsSubject = new BehaviorSubject<Product[]>([]);
  cartItems$ = this.cartItemsSubject.asObservable();

  



  constructor(private http: HttpClient , private authService:AuthService) { }

  // Obtenir les éléments du panier
  getCartItems(): Observable<Product[]> { 
    return this.http.get<any[]>(`${this.url}`);
  }

  // Ajouter un produit au panier

addToCart(formData: any, product: Product, customerId: number, errorHandler: (error: any) => void): Observable<any> {
  const baseUrl = `${this.apiUrl}${product.id}`; // e.g., http://localhost:5000/cart/add/1

  const token = localStorage.getItem('access_token');
  if (!token) {
    const error = 'Aucun token trouvé : l’utilisateur n’est pas connecté.';
    errorHandler(error);
    return throwError(() => new Error(error));
  }

  // On ajoute l'ID du client dans les données envoyées
  const payload = {
    ...formData,
    customer_id: customerId,
    product_id: product.id
  };

  const headers = new HttpHeaders({
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  });

  return this.http.post<any>(baseUrl, payload, { headers }).pipe(
    switchMap(response => {
      alert(response.message);
      return this.getCartItems(); // recharge le panier
    }),
    catchError(error => {
      errorHandler(error);
      return throwError(() => error);
    })
  );
}



  updateCart(){
    
    // Mettre à jour les éléments du panier
    this.cartItemsSubject.next(this.cartItemsSubject.getValue());

    // Envoyer une requête PUT pour mettre à jour les quantités des produits dans le panier

    this.http.put<Product[]>(this.apiUrl, this.cartItemsSubject.getValue(), { }).subscribe();
    this.cartItemsSubject.getValue().forEach(item => {
      this.http.put<Product>(`${this.apiUrl}/${item.id}`, item).subscribe();
    });
  }

  updateQuantity(id: number, newQuantity: number):  Observable<any> {
    return this.http.put<any>(`http://localhost:5000/cart/update-cart/${id}`, { quantity: newQuantity });
  }

  // Supprimer un produit du panier
removeFromCart(item: Cart): Observable<any> {
  console.log('product',item.id);
  
  return this.http.delete(`${this.url}/delete-cart/${item.id}`).pipe(
    switchMap(() => {
      // Recharge les éléments du panier après suppression
      return this.getCartItems();
    }),
    catchError(error => {
      console.error('Erreur lors de la suppression du produit du panier', error);
      return throwError(error);
    })
  );
}

// cart.service.ts
private cartCountSubject = new BehaviorSubject<number>(0);
cartCount$ = this.cartCountSubject.asObservable();

updateCartCount(count: number): void {
  this.cartCountSubject.next(count);
}

clearCart() {
  this.cartItemsSubject.next([]); // <-- envoie une liste vide dans l'observable
  localStorage.removeItem('cart'); // si tu utilises le stockage local
}

  
}
