import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { CategoryService } from '../services/category.service';
import { ProductsService } from '../service/products.service';
import { CartService } from '../services/cart.service';
import { catchError, of } from 'rxjs';
import { Product as BackendProduct } from '../models/products';

interface Category {
  id: number;
  name: string;
  image?: string;
  productCount?: number;
}

interface FeaturedProduct {
  id: number;
  name: string;
  price: number;
  image?: string;
  category?: string;
  rating?: number;
}

@Component({
  selector: 'app-categories',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './categories.component.html',
  styleUrl: './categories.component.scss'
})
export class CategoriesComponent implements OnInit {
  categories: Category[] = [];
  featuredProducts: FeaturedProduct[] = [];
  loading: boolean = true;
  error: string | null = null;
  selectedCategory: string | null = null;

  constructor(
    private categoryService: CategoryService,
    private productService: ProductsService,
    private cartService: CartService
  ) {}

  ngOnInit(): void {
    this.loadCategories();
    this.loadFeaturedProducts();
  }

  loadCategories(): void {
    this.loading = true;
    this.error = null;
    
    this.categoryService.getCategories().pipe(
      catchError(error => {
        console.error('Error loading categories:', error);
        this.error = 'Failed to load categories. Using fallback data.';
        // Fallback to mock data if backend fails
        return of(this.getMockCategories());
      })
    ).subscribe(categories => {
      // Map backend categories to include images and product counts
      this.categories = categories.map(category => ({
        ...category,
        image: this.getCategoryImage(category.name),
        productCount: this.getRandomProductCount()
      }));
      this.loading = false;
    });
  }

  loadFeaturedProducts(): void {
    // Load real products from backend
    this.productService.getProducts().pipe(
      catchError(error => {
        console.error('Error loading featured products:', error);
        // Fallback to mock data if backend fails
        return of(this.getMockProducts());
      })
    ).subscribe(products => {
      // Take first 4 products as featured
      this.featuredProducts = (products as BackendProduct[]).slice(0, 4).map((product: BackendProduct) => ({
        id: product.id,
        name: product.name,
        price: product.discount_price || product.current_price,
        image: this.getProductImage(product),
        category: 'Unknown', // Backend products don't have category field
        rating: this.getRandomRating()
      }));
    });
  }

  getCategoryImage(categoryName: string): string {
    // Use local assets instead of external URLs to avoid CORS/network issues
    const images: {[key: string]: string} = {
      'Smartphones': '/assets/images/smartphone-category.jpg',
      'Tablets': '/assets/images/tablet-category.jpg',
      'Laptops': '/assets/images/laptop-category.jpg',
      'Accessories': '/assets/images/accessories-category.jpg',
      'Audio': '/assets/images/audio-category.jpg',
      'Wearables': '/assets/images/wearables-category.jpg'
    };
    return images[categoryName] || '/assets/images/default-category.jpg';
  }

  getProductImage(product: any): string {
    // Use the image mapper service or fallback to local assets
    if (product.image_url) {
      return product.image_url;
    }
    // Fallback to local assets to avoid external URL issues
    return '/assets/images/product-placeholder.jpg';
  }

  getRandomProductCount(): number {
    return Math.floor(Math.random() * 50) + 10; // 10-60 products per category
  }

  getRandomRating(): number {
    return Math.round((Math.random() * 2 + 3) * 10) / 10; // 3.0-5.0 rating
  }

  getMockCategories(): Category[] {
    // Fallback mock data if backend fails
    return [
      { id: 1, name: 'Smartphones' },
      { id: 2, name: 'Tablets' },
      { id: 3, name: 'Laptops' },
      { id: 4, name: 'Accessories' },
      { id: 5, name: 'Audio' },
      { id: 6, name: 'Wearables' }
    ];
  }

  getMockProducts(): FeaturedProduct[] {
    // Fallback mock data if backend fails
    return [
      {
        id: 1,
        name: 'iPhone 15 Pro Max',
        price: 1199.99,
        category: 'Smartphones'
      },
      {
        id: 2,
        name: 'Samsung Galaxy S23 Ultra',
        price: 999.99,
        category: 'Smartphones'
      },
      {
        id: 3,
        name: 'MacBook Pro M2',
        price: 1999.99,
        category: 'Laptops'
      },
      {
        id: 4,
        name: 'AirPods Pro 2nd Gen',
        price: 249.99,
        category: 'Accessories'
      }
    ];
  }

  selectCategory(categoryName: string): void {
    this.selectedCategory = categoryName;
    // Here you could filter products by category
    // or navigate to a category-specific page
  }

  addToCart(productId: number): void {
    this.cartService.addToCart(productId, 1).subscribe({
      next: () => {
        console.log(`Product ${productId} added to cart successfully`);
        // You could show a toast notification here
      },
      error: (error) => {
        console.error(`Failed to add product ${productId} to cart:`, error);
      }
    });
  }

  addToFavorites(productId: number): void {
    console.log(`Product ${productId} added to favorites`);
    // Logic for adding to favorites
  }
}
