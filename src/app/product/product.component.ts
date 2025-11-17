import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ProductsService } from '../service/products.service';
import { CartService } from '../services/cart.service';
import { Product } from '../models/products';

@Component({
  selector: 'app-product',
  templateUrl: './product.component.html',
  styleUrl: './product.component.scss',
})
export class ProductComponent implements OnInit {
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
  placeholderImage = 'assets/images/placeholder.svg';

  constructor(
    private productService: ProductsService,
    private cartService: CartService,
    private route: ActivatedRoute,
    private router: Router
  ) { }

  ngOnInit(): void {
    this.loadProducts();
    this.handleRouteParams();
  }

  private handleRouteParams(): void {
    this.route.queryParams.subscribe(params => {
      if (params['search']) {
        this.searchQuery = params['search'];
        this.searchProducts();
      }
    });
  }

  loadProducts(): void {
    this.loading = true;
    this.error = null;

    this.productService.getProducts().subscribe({
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
    this.cartService.addToCart(product.id, quantity).subscribe({
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
    event.target.src = this.placeholderImage;
  }
}