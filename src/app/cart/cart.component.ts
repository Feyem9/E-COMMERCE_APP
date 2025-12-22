import { Component, OnInit, OnDestroy } from '@angular/core';
import { CartService } from '../services/cart.service';
import { Cart, Product } from '../models/products';
import { FormBuilder, FormGroup, Validators, FormsModule } from '@angular/forms';
import { TransactionService } from '../services/transaction.service';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';

@Component({
  selector: 'app-cart',
  templateUrl: './cart.component.html',
  styleUrl: './cart.component.scss'
})
export class CartComponent implements OnInit, OnDestroy {


  cartForm!: FormGroup;
  private destroy$ = new Subject<void>();

  cartItems: Cart[] = [];  // Liste des articles du panier
  totalItems: number = 0;  // Nombre total d'articles dans le panier
  totalPrice: number = 0;  // Prix total du panier
  total: number = 0;  // Prix total du panier
  private cartKey = 'my_cart';

  // ✅ Géolocalisation
  customerLocation: { lat: number, lng: number } | null = null;
  locationError: string = '';

  constructor(private cartService: CartService,
    private fb: FormBuilder,
    formModule: FormsModule,
    private transactionService: TransactionService
  ) { }

  ngOnInit(): void {
    this.loadCart();
    this.calculateTotal();
    this.cartService.clearCart();
    this.getCustomerLocation();  // ✅ Demander position GPS

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
    this.cartService.getCartItems()
      .pipe(takeUntil(this.destroy$))
      .subscribe(items => {
        console.log('Données reçues dans le panier :', items);  // ⬅️ Vérifie ici

        this.cartItems = items;
        this.calculateTotal();
      });
  }


  decreaseQuantity(item: Cart): void {
    if (item.quantity > 1) {
      const newQuantity = item.quantity - 1;

      this.cartService.updateQuantity(item.id, newQuantity)
        .pipe(takeUntil(this.destroy$))
        .subscribe(
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

    this.cartService.updateQuantity(item.id, newQuantity)
      .pipe(takeUntil(this.destroy$))
      .subscribe(
        res => {
          item.quantity = res.new_quantity;
          this.calculateTotal();
          console.log('Quantité mise à jour avec succès sur le backend', res);
        },
        err => {
          console.error('Erreur lors de l\'augmentation de la quantité', err);
        }
      );
  }



  removeItem(item: Cart): void {
    console.log('items', item.id);

    if (!item.id) {
      console.error('ID du produit manquant');
      return;
    }
    this.cartService.removeFromCart(item.id)
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: () => {
          this.loadCart();
        },
        error: err => {
          console.error('Erreur lors de la suppression', err);
        }
      });
  }

  // \u2705 Obtenir la position GPS du client
  getCustomerLocation(): void {
    if ('geolocation' in navigator) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          this.customerLocation = {
            lat: position.coords.latitude,
            lng: position.coords.longitude
          };
          console.log('\ud83d\udccd Position client captur\u00e9e:', this.customerLocation);
        },
        (error) => {
          this.locationError = error.message;
          console.warn('\u26a0\ufe0f G\u00e9olocalisation refus\u00e9e:', error.message);
          // Continuer sans g\u00e9olocalisation
        },
        {
          enableHighAccuracy: true,
          timeout: 5000,
          maximumAge: 0
        }
      );
    } else {
      this.locationError = 'G\u00e9olocalisation non support\u00e9e';
      console.warn('\u26a0\ufe0f G\u00e9olocalisation non support\u00e9e par ce navigateur');
    }
  }


  // Procéder au paiement
  checkout(): void {
    // Dynamic return URL based on current host
    const returnUrl = typeof window !== 'undefined' 
      ? `${window.location.origin}/payment-success`
      : 'https://staging-market.vercel.app/payment-success';

    const paymentData = {
      total_amount: this.totalPrice,
      currency: 'XAF',
      return_url: returnUrl,
      notify_url: "https://webhook.site/d457b2f3-dd71-4f04-9af5-e2fcf3be8f34",
      payment_country: "CM"
    };
    
    this.transactionService.initiatePayment(paymentData)
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (response: any) => {
          if (response && response.payment_url) {
            // ✅ Vider le panier AVANT de rediriger
            this.cartItems.forEach(item => {
              if (item.id) {
                this.cartService.removeFromCart(item.id).subscribe();
              }
            });
            
            // Vider le panier local également
            this.cartItems = [];
            this.totalPrice = 0;
            this.cartService.updateCartCount(0);
            
            console.log('✅ Panier vidé avec succès');
            
            // Attendre un peu avant de rediriger (laisser les requêtes DELETE se terminer)
            setTimeout(() => {
              window.location.href = response.payment_url;
            }, 500);
          } else {
            alert('Erreur de redirection vers PayUnit.');
          }
        },
        error: (err: any) => {
          console.error('Erreur paiement :', err);
          alert('Erreur lors du paiement.');
        }
      });
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

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  payer() {
    this.checkout();
  }

  // Vider le panier
  clearCart() {
    localStorage.removeItem(this.cartKey);
  }

} 