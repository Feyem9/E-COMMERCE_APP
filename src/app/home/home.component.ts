import { Component, OnInit, OnDestroy } from '@angular/core';
import { Product } from '../models/products';
import { ProductsService } from '../service/products.service';
import { CartService } from '../services/cart.service';
import { ImageMapperService } from '../services/image-mapper.service';
import { Router } from '@angular/router';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss'
})
export class HomeComponent implements OnInit, OnDestroy {

  featuredProducts: Product[] = [];
  loading = false;
  error: string | null = null;
  placeholderImage = '/assets/images/placeholder.svg';
  private destroy$ = new Subject<void>();

  constructor(
    private productsService: ProductsService,
    private cartService: CartService,
    private imageMapper: ImageMapperService,
    private router: Router
  ) { }

  ngOnInit(): void {
    this.loadFeaturedProducts();
  }

  loadFeaturedProducts(): void {
    this.loading = true;
    this.error = null;
    
    this.productsService.getProducts()
      .pipe(takeUntil(this.destroy$))
      .subscribe({
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
    this.cartService.addToCart(product.id, 1)
      .pipe(takeUntil(this.destroy$))
      .subscribe({
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

  onImageError(event: any): void {
    // Set a CSS background instead of an image to avoid LCP issues
    event.target.style.display = 'none';
    event.target.parentElement.style.backgroundColor = '#e0e0e0';
    event.target.parentElement.style.minHeight = '300px';
    event.target.parentElement.style.display = 'flex';
    event.target.parentElement.style.alignItems = 'center';
    event.target.parentElement.style.justifyContent = 'center';
    
    // Add placeholder text
    const placeholder = document.createElement('div');
    placeholder.innerHTML = '📷 No Image Available';
    placeholder.style.fontSize = '24px';
    placeholder.style.color = '#999';
    placeholder.style.textAlign = 'center';
    event.target.parentElement.appendChild(placeholder);
  }

  getProductImage(product: Product): string {
    return this.imageMapper.getImageUrl(product);
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }
}
