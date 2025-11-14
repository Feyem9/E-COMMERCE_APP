import { Component, OnInit } from '@angular/core';
import { Product } from '../models/products';
import { ProductsService } from '../service/products.service';
import { CartService } from '../services/cart.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss'
})
export class HomeComponent implements OnInit {

  featuredProducts: Product[] = [];
  loading = false;
  error: string | null = null;

  constructor(
    private productsService: ProductsService,
    private cartService: CartService,
    private router: Router
  ) { }

  ngOnInit(): void {
    this.loadFeaturedProducts();
  }

  loadFeaturedProducts(): void {
    this.loading = true;
    this.error = null;
    
    this.productsService.getProducts().subscribe({
      next: (products) => {
        // Take first 6 products as featured
        this.featuredProducts = products.slice(0, 6);
        this.loading = false;
      },
      error: (error) => {
        console.error('Error loading products:', error);
        this.error = 'Erreur lors du chargement des produits';
        this.loading = false;
      }
    });
  }

  addToCart(product: Product): void {
    this.cartService.addToCart(product.id, 1).subscribe({
      next: () => {
        // Product added successfully, handled in service
      },
      error: (error) => {
        console.error('Error adding to cart:', error);
      }
    });
  }

  navigateToProducts(): void {
    this.router.navigate(['/product']);
  }

  navigateToProduct(productId: number): void {
    this.router.navigate(['/product', productId]);
  }

  onNewsletterSubmit(): void {
    // Newsletter subscription logic would go here
    alert('Thank you for subscribing to our newsletter!');
  }
}
