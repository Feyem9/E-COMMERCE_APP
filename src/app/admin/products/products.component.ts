import { Component, OnInit, OnDestroy } from '@angular/core';
import { AdminService, Product } from '../services/admin.service';
import { Subject } from 'rxjs';
import { takeUntil, debounceTime, distinctUntilChanged } from 'rxjs/operators';

@Component({
  selector: 'app-admin-products',
  templateUrl: './products.component.html',
  styleUrls: ['./products.component.scss']
})
export class ProductsComponent implements OnInit, OnDestroy {
  products: Product[] = [];
  loading = true;
  error: string | null = null;
  
  // Pagination
  currentPage = 1;
  perPage = 12;
  totalPages = 1;
  totalProducts = 0;
  
  // Search
  searchTerm = '';
  
  // Modal
  selectedProduct: Product | null = null;
  showModal = false;
  modalAction: 'create' | 'edit' | 'delete' = 'create';
  
  // Form
  productForm: Partial<Product> = {
    name: '',
    description: '',
    current_price: 0,
    discount_price: 0,
    quantity: 0,
    picture: ''
  };
  
  private searchSubject = new Subject<string>();
  private destroy$ = new Subject<void>();

  constructor(private adminService: AdminService) {}

  ngOnInit(): void {
    this.loadProducts();
    
    this.searchSubject.pipe(
      debounceTime(400),
      distinctUntilChanged(),
      takeUntil(this.destroy$)
    ).subscribe(() => {
      this.currentPage = 1;
      this.loadProducts();
    });
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  loadProducts(): void {
    this.loading = true;
    this.error = null;

    this.adminService.getProducts(this.currentPage, this.perPage, this.searchTerm)
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (response) => {
          this.products = response.products;
          this.totalPages = response.pagination.pages;
          this.totalProducts = response.pagination.total;
          this.loading = false;
        },
        error: (err) => {
          this.error = 'Erreur lors du chargement des produits';
          this.loading = false;
          console.error(err);
        }
      });
  }

  onSearch(event: Event): void {
    const value = (event.target as HTMLInputElement).value;
    this.searchTerm = value;
    this.searchSubject.next(value);
  }

  goToPage(page: number): void {
    if (page >= 1 && page <= this.totalPages) {
      this.currentPage = page;
      this.loadProducts();
    }
  }

  openCreateModal(): void {
    this.productForm = {
      name: '',
      description: '',
      current_price: 0,
      discount_price: 0,
      quantity: 0,
      picture: ''
    };
    this.modalAction = 'create';
    this.showModal = true;
  }

  openEditModal(product: Product): void {
    this.selectedProduct = product;
    this.productForm = { ...product };
    this.modalAction = 'edit';
    this.showModal = true;
  }

  openDeleteModal(product: Product): void {
    this.selectedProduct = product;
    this.modalAction = 'delete';
    this.showModal = true;
  }

  closeModal(): void {
    this.showModal = false;
    this.selectedProduct = null;
  }

  saveProduct(): void {
    if (!this.validateForm()) return;

    if (this.modalAction === 'create') {
      this.adminService.createProduct(this.productForm)
        .pipe(takeUntil(this.destroy$))
        .subscribe({
          next: () => {
            this.closeModal();
            this.loadProducts();
          },
          error: (err) => {
            alert('Erreur lors de la création: ' + (err.error?.error || 'Erreur inconnue'));
          }
        });
    } else if (this.modalAction === 'edit' && this.selectedProduct) {
      this.adminService.updateProduct(this.selectedProduct.id, this.productForm)
        .pipe(takeUntil(this.destroy$))
        .subscribe({
          next: () => {
            this.closeModal();
            this.loadProducts();
          },
          error: (err) => {
            alert('Erreur lors de la mise à jour: ' + (err.error?.error || 'Erreur inconnue'));
          }
        });
    }
  }

  deleteProduct(): void {
    if (!this.selectedProduct) return;

    this.adminService.deleteProduct(this.selectedProduct.id)
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: () => {
          this.closeModal();
          this.loadProducts();
        },
        error: (err) => {
          alert('Erreur lors de la suppression: ' + (err.error?.error || 'Erreur inconnue'));
        }
      });
  }

  validateForm(): boolean {
    if (!this.productForm.name?.trim()) {
      alert('Le nom est requis');
      return false;
    }
    if (!this.productForm.description?.trim()) {
      alert('La description est requise');
      return false;
    }
    if (!this.productForm.current_price || this.productForm.current_price <= 0) {
      alert('Le prix doit être supérieur à 0');
      return false;
    }
    if (!this.productForm.picture?.trim()) {
      alert('L\'URL de l\'image est requise');
      return false;
    }
    return true;
  }

  formatCurrency(amount: number): string {
    return new Intl.NumberFormat('fr-FR', {
      style: 'currency',
      currency: 'XAF'
    }).format(amount);
  }

  getDiscount(product: Product): number {
    if (!product.current_price || !product.discount_price) return 0;
    return Math.round((1 - product.discount_price / product.current_price) * 100);
  }

  get pageNumbers(): number[] {
    const pages: number[] = [];
    const start = Math.max(1, this.currentPage - 2);
    const end = Math.min(this.totalPages, this.currentPage + 2);
    
    for (let i = start; i <= end; i++) {
      pages.push(i);
    }
    return pages;
  }
}
