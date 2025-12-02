import { Component, OnInit, OnDestroy } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ProductsService } from '../service/products.service';
import { CartService } from '../services/cart.service';
import { ImageMapperService } from '../services/image-mapper.service';
import { Product } from '../models/products';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';

@Component({
  selector: 'app-product',
  templateUrl: './product.component.html',
  styleUrl: './product.component.scss',
})
export class ProductComponent implements OnInit, OnDestroy {
  products: Product[] = [];
  filteredProducts: Product[] = [];
  loading = false;
  error: string | null = null;
  searchQuery = '';
  sortBy = 'name';
  sortOrder: 'asc' | 'desc' = 'asc';
  currentPage = 1;
  itemsPerPage = 12;
  totalPages = 0;
  placeholderImage = '/assets/images/placeholder.svg';
  private destroy$ = new Subject<void>();

  constructor(
    private productService: ProductsService,
    private cartService: CartService,
    private imageMapper: ImageMapperService,
    private route: ActivatedRoute,
    private router: Router
  ) { }

  ngOnInit(): void {
    this.loadProducts();
    this.handleRouteParams();
  }

  private handleRouteParams(): void {
    this.route.queryParams
      .pipe(takeUntil(this.destroy$))
      .subscribe(params => {
        if (params['search']) {
          this.searchQuery = params['search'];
          this.searchProducts();
        }
      });
  }

  loadProducts(): void {
    this.loading = true;
    this.error = null;

    this.productService.getProducts()
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (data: Product[]) => {
          this.products = data;
          this.filteredProducts = [...data];
          this.updatePagination();
          this.loading = false;
        },
        error: (error) => {
          console.error('Error loading products:', error);
          this.error = 'Erreur lors du chargement des produits';
          this.loading = false;
        }
      });
  }

  searchProducts(): void {
    if (!this.searchQuery.trim()) {
      this.filteredProducts = [...this.products];
    } else {
      const query = this.searchQuery.toLowerCase();
      this.filteredProducts = this.products.filter(product =>
        product.name.toLowerCase().includes(query) ||
        product.description.toLowerCase().includes(query)
      );
    }
    this.currentPage = 1;
    this.updatePagination();
  }

  sortProducts(): void {
    this.filteredProducts.sort((a, b) => {
      let comparison = 0;
      
      switch (this.sortBy) {
        case 'name':
          comparison = a.name.localeCompare(b.name);
          break;
        case 'price':
          comparison = (a.discount_price || a.current_price) - (b.discount_price || b.current_price);
          break;
        case 'discount':
          const discountA = a.current_price - (a.discount_price || a.current_price);
          const discountB = b.current_price - (b.discount_price || b.current_price);
          comparison = discountA - discountB;
          break;
      }

      return this.sortOrder === 'asc' ? comparison : -comparison;
    });
  }

  updatePagination(): void {
    this.totalPages = Math.ceil(this.filteredProducts.length / this.itemsPerPage);
  }

  get paginatedProducts(): Product[] {
    const startIndex = (this.currentPage - 1) * this.itemsPerPage;
    const endIndex = startIndex + this.itemsPerPage;
    return this.filteredProducts.slice(startIndex, endIndex);
  }

  get pages(): number[] {
    return Array.from({ length: this.totalPages }, (_, i) => i + 1);
  }

  changePage(page: number): void {
    if (page >= 1 && page <= this.totalPages) {
      this.currentPage = page;
    }
  }

  addToCart(product: Product, quantity: number = 1): void {
    this.cartService.addToCart(product.id, quantity)
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: () => {
          // Success handled in service
        },
        error: (error) => {
          console.error('Error adding to cart:', error);
        }
      });
  }

  viewProductDetails(product: Product): void {
    // Navigate to product detail page (to be implemented)
    console.log('View details for:', product.name);
  }

  getDiscountPercentage(product: Product): number {
    if (product.discount_price && product.discount_price < product.current_price) {
      return Math.round(((product.current_price - product.discount_price) / product.current_price) * 100);
    }
    return 0;
  }

  onSortChange(): void {
    this.sortProducts();
  }

  toggleSortOrder(): void {
    this.sortOrder = this.sortOrder === 'asc' ? 'desc' : 'asc';
    this.sortProducts();
  }

  clearSearch(): void {
    this.searchQuery = '';
    this.searchProducts();
  }

  retry(): void {
    this.loadProducts();
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