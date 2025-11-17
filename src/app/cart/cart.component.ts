import { Component, OnInit } from '@angular/core';
import { CartService } from '../services/cart.service';
import { Cart, Product } from '../models/products';
import { FormBuilder, FormGroup, Validators, FormsModule } from '@angular/forms';
import { TransactionService } from '../services/transaction.service';

@Component({
  selector: 'app-cart',
  templateUrl: './cart.component.html',
  styleUrl: './cart.component.scss'
})
export class CartComponent implements OnInit {


  cartForm!: FormGroup;

  cartItems: Cart[] = [];  // Liste des articles du panier
  totalItems: number = 0;  // Nombre total d'articles dans le panier
  totalPrice: number = 0;  // Prix total du panier
  total: number = 0;  // Prix total du panier
  private cartKey = 'my_cart';

  constructor(private cartService: CartService,
    private fb: FormBuilder,
    formModule: FormsModule,
    private transactionService: TransactionService
  ) { }

  ngOnInit(): void {
    this.loadCart();
    this.calculateTotal();
    this.cartService.clearCart();


    // Initialisation du formulaire réactif
    this.cartForm = this.fb.group({
      product_id: [''],  // Le champ caché product_id
      quantity: [
        1,  // Valeur par défaut
        [Validators.required, Validators.min(1), Validators.max(10000)]  // Validations pour la quantité
      ]
    });
  }

  // Charger les articles du panier à partir du service
  loadCart(): void {
    this.cartService.getCartItems().subscribe(items => {
      console.log('Données reçues dans le panier :', items);  // ⬅️ Vérifie ici

      this.cartItems = items;
      this.calculateTotal();
    });
  }


  decreaseQuantity(item: Cart): void {
    if (item.quantity > 1) {
      const newQuantity = item.quantity - 1;

      this.cartService.updateQuantity(item.id, newQuantity).subscribe(
        res => {
          item.quantity = res.new_quantity;
          this.calculateTotal();
          console.log('Quantité mise à jour avec succès sur le backend', res);

        },
        err => {
          console.error('Erreur lors de la diminution de la quantité', err);
        }
      );
    }
  }

  increaseQuantity(item: Cart): void {
    const newQuantity = item.quantity + 1;

    this.cartService.updateQuantity(item.id, newQuantity).subscribe(
      res => {
        item.quantity = res.new_quantity;
        this.calculateTotal();
        console.log('Quantité mise à jour avec succès sur le backend', res);

      },
      err => {
        console.error('Erreur lors de l’augmentation de la quantité', err);
      }
    );
  }



  removeItem(item: Cart): void {
    console.log('items', item.id);

    if (!item.id) {
      console.error('ID du produit manquant');
      return;
    }
    this.cartService.removeFromCart(item.id).subscribe({
      next: () => {
        this.loadCart();
      },
      error: err => {
        console.error('Erreur lors de la suppression', err);
      }
    });
  }


  // Procéder au paiement
  checkout(): void {
    const paymentData = {
      total_amount: this.totalPrice,
      currency: 'XAF',
      return_url: "https://sf6lj8b2-4200.uks1.devtunnels.ms/payment-success",
      notify_url: "https://webhook.site/d457b2f3-dd71-4f04-9af5-e2fcf3be8f34",
      payment_country: "CM"

    };
    this.transactionService.initiatePayment(paymentData).subscribe(
      (response: any) => {
        if (response && response.payment_url) {
          window.location.href = response.payment_url;
        } else {
          alert('Erreur de redirection vers PayUnit.');
        }
      },
      (err: any) => {
        console.error('Erreur paiement :', err);
        alert('Erreur lors du paiement.');
      }
    );
  }

  // }

  // cart.component.ts
  calculateTotal(): void {
    this.total = 0;
    let count = 0;
    this.cartItems.forEach(item => {
      this.total += item.current_price * item.quantity;
      count += item.quantity;
    });

    this.totalPrice = this.cartItems.reduce((acc, item) => {
      const price = Number(item.current_price) || 0;
      const quantity = Number(item.quantity) || 0;
      return acc + (price * quantity);
    }, 0);
    console.log('Total Price:', this.totalPrice);

    // Mettre à jour le nombre d'articles dans le panier
    this.cartService.updateCartCount(this.cartItems.length);
  }



  get showTotal(): string {
    return this.totalPrice.toFixed(2);
  }

  payer() {
    this.checkout();
  }

  // Vider le panier
  clearCart() {
    localStorage.removeItem(this.cartKey);
  }

}