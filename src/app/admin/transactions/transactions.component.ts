import { Component, OnInit, OnDestroy } from '@angular/core';
import { AdminService, Transaction } from '../services/admin.service';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';

@Component({
  selector: 'app-admin-transactions',
  templateUrl: './transactions.component.html',
  styleUrls: ['./transactions.component.scss']
})
export class TransactionsComponent implements OnInit, OnDestroy {
  transactions: Transaction[] = [];
  loading = true;
  error: string | null = null;
  
  currentPage = 1;
  perPage = 10;
  totalPages = 1;
  totalTransactions = 0;
  
  statusFilter = '';
  statuses = ['pending', 'completed', 'failed', 'cancelled'];
  
  selectedTransaction: Transaction | null = null;
  showModal = false;
  
  private destroy$ = new Subject<void>();

  constructor(private adminService: AdminService) {}

  ngOnInit(): void {
    this.loadTransactions();
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  loadTransactions(): void {
    this.loading = true;
    this.error = null;

    this.adminService.getTransactions(this.currentPage, this.perPage, this.statusFilter)
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (response) => {
          this.transactions = response.transactions;
          this.totalPages = response.pagination.pages;
          this.totalTransactions = response.pagination.total;
          this.loading = false;
        },
        error: (err) => {
          this.error = 'Erreur lors du chargement des transactions';
          this.loading = false;
          console.error(err);
        }
      });
  }

  onStatusFilterChange(event: Event): void {
    this.statusFilter = (event.target as HTMLSelectElement).value;
    this.currentPage = 1;
    this.loadTransactions();
  }

  goToPage(page: number): void {
    if (page >= 1 && page <= this.totalPages) {
      this.currentPage = page;
      this.loadTransactions();
    }
  }

  openDetailModal(transaction: Transaction): void {
    this.selectedTransaction = transaction;
    this.showModal = true;
  }

  closeModal(): void {
    this.showModal = false;
    this.selectedTransaction = null;
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
      'completed': 'status-success',
      'failed': 'status-danger',
      'cancelled': 'status-muted'
    };
    return classes[status?.toLowerCase()] || 'status-default';
  }

  getStatusIcon(status: string): string {
    const icons: { [key: string]: string } = {
      'pending': '⏳',
      'completed': '✅',
      'failed': '❌',
      'cancelled': '🚫'
    };
    return icons[status?.toLowerCase()] || '💳';
  }

  get pageNumbers(): number[] {
    const pages: number[] = [];
    const start = Math.max(1, this.currentPage - 2);
    const end = Math.min(this.totalPages, this.currentPage + 2);
    for (let i = start; i <= end; i++) pages.push(i);
    return pages;
  }
}
