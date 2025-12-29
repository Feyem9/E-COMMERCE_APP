import { Component, OnInit, OnDestroy } from '@angular/core';
import { AdminService, Order } from '../services/admin.service';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';

@Component({
  selector: 'app-admin-orders',
  templateUrl: './orders.component.html',
  styleUrls: ['./orders.component.scss']
})
export class OrdersComponent implements OnInit, OnDestroy {
  orders: Order[] = [];
  loading = true;
  error: string | null = null;
  
  currentPage = 1;
  perPage = 10;
  totalPages = 1;
  totalOrders = 0;
  
  statusFilter = '';
  statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled'];
  
  selectedOrder: Order | null = null;
  showModal = false;
  
  private destroy$ = new Subject<void>();

  constructor(private adminService: AdminService) {}

  ngOnInit(): void {
    this.loadOrders();
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  loadOrders(): void {
    this.loading = true;
    this.error = null;

    this.adminService.getOrders(this.currentPage, this.perPage, this.statusFilter)
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (response) => {
          this.orders = response.orders;
          this.totalPages = response.pagination.pages;
          this.totalOrders = response.pagination.total;
          this.loading = false;
        },
        error: (err) => {
          this.error = 'Erreur lors du chargement des commandes';
          this.loading = false;
          console.error(err);
        }
      });
  }

  onStatusFilterChange(event: Event): void {
    this.statusFilter = (event.target as HTMLSelectElement).value;
    this.currentPage = 1;
    this.loadOrders();
  }

  goToPage(page: number): void {
    if (page >= 1 && page <= this.totalPages) {
      this.currentPage = page;
      this.loadOrders();
    }
  }

  openStatusModal(order: Order): void {
    this.selectedOrder = { ...order };
    this.showModal = true;
  }

  closeModal(): void {
    this.showModal = false;
    this.selectedOrder = null;
  }

  updateStatus(newStatus: string): void {
    if (!this.selectedOrder) return;

    this.adminService.updateOrderStatus(this.selectedOrder.id, newStatus)
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: () => {
          this.closeModal();
          this.loadOrders();
        },
        error: (err) => {
          alert('Erreur: ' + (err.error?.error || 'Erreur inconnue'));
        }
      });
  }

  formatCurrency(amount: number): string {
    return new Intl.NumberFormat('fr-FR', {
      style: 'currency',
      currency: 'XAF'
    }).format(amount);
  }

  formatDate(dateStr: string): string {
    if (!dateStr) return '-';
    return new Date(dateStr).toLocaleDateString('fr-FR', {
      day: '2-digit',
      month: 'short',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  }

  getStatusClass(status: string): string {
    const classes: { [key: string]: string } = {
      'pending': 'status-warning',
      'processing': 'status-info',
      'shipped': 'status-primary',
      'delivered': 'status-success',
      'cancelled': 'status-danger'
    };
    return classes[status?.toLowerCase()] || 'status-default';
  }

  getStatusIcon(status: string): string {
    const icons: { [key: string]: string } = {
      'pending': '⏳',
      'processing': '🔄',
      'shipped': '🚚',
      'delivered': '✅',
      'cancelled': '❌'
    };
    return icons[status?.toLowerCase()] || '📋';
  }

  get pageNumbers(): number[] {
    const pages: number[] = [];
    const start = Math.max(1, this.currentPage - 2);
    const end = Math.min(this.totalPages, this.currentPage + 2);
    for (let i = start; i <= end; i++) pages.push(i);
    return pages;
  }
}
