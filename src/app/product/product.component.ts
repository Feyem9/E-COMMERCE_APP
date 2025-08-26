import { Component, OnInit } from '@angular/core';
import { ProductsService } from '../service/products.service';
import { Product } from '../models/products';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { CartService } from '../services/cart.service';
import { AuthService } from '../customers/auth.service';

@Component({
  selector: 'app-product',
  templateUrl: './product.component.html',
  styleUrl: './product.component.scss',
})
export class ProductComponent implements OnInit {
  products: Product[] = [];
  cartForm!: FormGroup;
  selectedProduct!: Product;
  selectProduct(product: Product): void {
    this.selectedProduct = product;
    console.log('Produit sélectionné:', product);

    this.cartForm.patchValue({
      product_id: product.id,
      quantity: 1,
      
    });
  }

  // selectProduct! : Product ;

  constructor(
    private productService: ProductsService,
    private cartService: CartService,
    private fb: FormBuilder,
    private authService: AuthService
  ) { }
  


  ngOnInit(): void {
    this.productService.getProducts().subscribe(
      (data: Product[]) => {
        this.products = data;
      },
      (error) => {
        console.error('Erreur lors du chargement des produits', error);
      }
    );
    this.cartForm = this.fb.group({
      product_id: [''], // Le champ caché product_id
      quantity: [
        1, // Valeur par défaut
        [Validators.required, Validators.min(1), Validators.max(10000)], // Validations pour la quantité
      ],
    });
  }



onSubmit() {
  function errorHandler(error: any): void {
    console.error('Erreur lors de l\'appel à l\'API :', error);
    alert('Une erreur est survenue lors de l\'ajout au panier.');
  }

  if (this.cartForm.valid && this.selectedProduct) {
    const formData = this.cartForm.value;

    // 🔥 Récupérer l'ID client (depuis AuthService ou localStorage)
    const customerId = this.authService.getUserId(); // ou localStorage.getItem('user_id')
    if (customerId === null) {
      console.log(customerId);
      
  alert("Vous devez être connecté pour ajouter un produit au panier.");
  return;  // Stopper la fonction onSubmit
}

    this.cartService.addToCart(formData, this.selectedProduct, customerId, errorHandler).subscribe(
      (response: any) => {
        console.log('Réponse complète de l\'API:', response);

        if (Array.isArray(response)) {
          const cart = JSON.parse(localStorage.getItem('cart') || '[]');
          cart.push(response);
          localStorage.setItem('cart', JSON.stringify(cart));

          if (response.length > 0) {
            const lastProduct = response[response.length - 1];
            localStorage.setItem('lastApiResponseIndex', JSON.stringify(response.length - 1));
            console.warn('Réponse tableau – dernier produit:', lastProduct);
          } else {
            alert('Réponse vide reçue.');
          }
        } else if (typeof response === 'object' && response !== null) {
          const message = response.message ?? 'Message non disponible';
          const addedProduct = response.product ?? {};

          console.log('Message:', message);
          console.log('Produit ajouté:', addedProduct);

          if (Object.keys(addedProduct).length > 0) {
            alert(`${message}: ${addedProduct.name} au prix de ${addedProduct.current_price}`);
          } else {
            console.warn('Produit mal formé dans la réponse.');
          }
        } else {
          console.warn('Réponse inattendue de l\'API.');
        }
      },
      (error) => {
        console.log('Erreur serveur:', error);
        alert('Erreur lors de la communication avec le serveur.');
      }
    );
  } else {
    if (!this.selectedProduct) {
      alert('Aucun produit sélectionné.');
    } else if (!this.cartForm.valid) {
      alert('Formulaire invalide. Veuillez remplir tous les champs.');
    }
  }
}


}


