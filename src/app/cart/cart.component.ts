import { Component, OnInit } from '@angular/core';
import { CartService } from '../services/cart.service';
import { Product } from '../models/products';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-cart',
  templateUrl: './cart.component.html',
  styleUrl: './cart.component.scss'
})
export class CartComponent  implements OnInit{

  cartForm!: FormGroup;

  cartItems: Product[] = [];  // Liste des articles du panier
  totalItems: number = 0;  // Nombre total d'articles dans le panier
  totalPrice: number = 0;  // Prix total du panier

  constructor(private cartService: CartService ,
    private fb: FormBuilder
  ) {}
 
  ngOnInit(): void {
    this.loadCart();

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
        this.cartItems = items;
        this.calculateTotal();
      });
    }

  // Diminuer la quantité d'un article dans le panier
  decreaseQuantity(item: Product): void {
    if (item.quantity > 1) {
      item.quantity--;
      this.cartService.updateCart(this.cartItems);  // Mettre à jour le panier
      this.calculateTotal();
    }
  }

  // Augmenter la quantité d'un article dans le panier
  increaseQuantity(item: Product): void {
    item.quantity++;
    this.cartService.updateCart(this.cartItems);  // Mettre à jour le panier
    this.calculateTotal();
  }

  // Supprimer un article du panier
  removeItem(item: Product): void {
    this.cartItems = this.cartItems.filter(cartItem => cartItem.id !== item.id);
    this.cartService.updateCart(this.cartItems);  // Mettre à jour le panier
    this.calculateTotal();
  }

  // Calculer le nombre total d'articles et le prix total du panier
  calculateTotal(): void {
    this.totalItems = this.cartItems.reduce((acc, item) => acc + item.quantity, 0);
    this.totalPrice = this.cartItems.reduce((acc, item) => acc + (item.price * item.quantity), 0);
  }

  // Procéder au paiement
  checkout(): void {
    // Implémenter ici la logique de paiement
    console.log('Proceeding to checkout...');
    // Tu peux rediriger vers une page de paiement ou déclencher un service de paiement
  }

// }
// export class CartComponent {
  // cartItems: Product[] = [];
//   totalItems: number = 0;
//   totalPrice: number = 0;

//   constructor(private cartService: CartService) {}

//   ngOnInit(): void {
//     this.cartService.cartItems$.subscribe(items => {
//       this.cartItems = items;
//       this.calculateTotal();
//     });
  // }

//   calculateTotal(): void {
//     this.totalItems = this.cartService.getTotalItems();
//     this.totalPrice = this.cartService.getTotalPrice();
//   }

//   // Les autres méthodes comme decreaseQuantity, increaseQuantity, removeItem sont similaires




// Gestionnaire de la soumission du formulaire
onSubmit() {
  if (this.cartForm.valid) {
    const formData = this.cartForm.value;
    console.log('Form Data:', formData);

    // Vous pouvez envoyer les données au backend via un service HTTP ici
    // Par exemple : this.cartService.addToCart(formData).subscribe(...);
  }
}

}