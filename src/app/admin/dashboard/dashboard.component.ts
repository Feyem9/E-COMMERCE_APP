import { Component, OnInit, OnDestroy } from '@angular/core';
import { AdminService, DashboardStats, RevenueStats, RecentActivity, ChartsData, AdminNotification } from '../services/admin.service';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';

@Component({
  selector: 'app-admin-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit, OnDestroy {
  stats: DashboardStats | null = null;
  revenueStats: RevenueStats | null = null;
  recentActivity: RecentActivity | null = null;
  chartsData: ChartsData | null = null;
  notifications: AdminNotification[] = [];
  
  loading = true;
  error: string | null = null;
  exportingUsers = false;
  exportingOrders = false;
  exportingTransactions = false;
  
  private destroy$ = new Subject<void>();

  constructor(private adminService: AdminService) {}

  ngOnInit(): void {
    this.loadDashboardData();
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  loadDashboardData(): void {
    this.loading = true;
    this.error = null;

    // Charger les statistiques principales
    this.adminService.getDashboardStats()
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (data) => {
          this.stats = data;
          this.loading = false;
        },
        error: (err) => {
          this.error = 'Erreur lors du chargement des statistiques';
          this.loading = false;
          console.error(err);
        }
      });

    // Charger les statistiques de revenus
    this.adminService.getRevenueStats()
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (data) => {
          this.revenueStats = data;
        },
        error: (err) => console.error('Erreur revenus:', err)
      });

    // Charger l'activité récente
    this.adminService.getRecentActivity()
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (data) => {
          this.recentActivity = data;
        },
        error: (err) => console.error('Erreur activité:', err)
      });

    // Charger les données des graphiques avancés
    this.adminService.getChartsData()
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (data) => {
          this.chartsData = data;
        },
        error: (err) => console.error('Erreur charts:', err)
      });

    // Charger les notifications
    this.adminService.getNotifications()
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (data) => {
          this.notifications = data.notifications;
        },
        error: (err) => console.error('Erreur notifications:', err)
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
    const statusMap: { [key: string]: string } = {
      'completed': 'status-success',
      'pending': 'status-warning',
      'processing': 'status-info',
      'shipped': 'status-info',
      'delivered': 'status-success',
      'cancelled': 'status-danger',
      'failed': 'status-danger'
    };
    return statusMap[status?.toLowerCase()] || 'status-default';
  }

  refreshData(): void {
    this.loadDashboardData();
  }

  getBarHeight(amount: number): number {
    if (!this.revenueStats || !this.revenueStats.daily_revenue.length) return 10;
    
    const maxAmount = Math.max(...this.revenueStats.daily_revenue.map(d => d.amount || 0));
    if (maxAmount === 0) return 10;
    
    return Math.max(10, (amount / maxAmount) * 100);
  }

  // ============================================
  // EXPORT FUNCTIONS
  // ============================================
  exportUsers(): void {
    this.exportingUsers = true;
    this.adminService.exportUsersCSV()
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (blob) => {
          this.downloadFile(blob, 'users_export.csv');
          this.exportingUsers = false;
        },
        error: (err) => {
          console.error('Export users error:', err);
          alert('Erreur lors de l\'export des utilisateurs');
          this.exportingUsers = false;
        }
      });
  }

  exportOrders(): void {
    this.exportingOrders = true;
    this.adminService.exportOrdersCSV()
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (blob) => {
          this.downloadFile(blob, 'orders_export.csv');
          this.exportingOrders = false;
        },
        error: (err) => {
          console.error('Export orders error:', err);
          alert('Erreur lors de l\'export des commandes');
          this.exportingOrders = false;
        }
      });
  }

  exportTransactions(): void {
    this.exportingTransactions = true;
    this.adminService.exportTransactionsCSV()
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (blob) => {
          this.downloadFile(blob, 'transactions_export.csv');
          this.exportingTransactions = false;
        },
        error: (err) => {
          console.error('Export transactions error:', err);
          alert('Erreur lors de l\'export des transactions');
          this.exportingTransactions = false;
        }
      });
  }

  private downloadFile(blob: Blob, filename: string): void {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  }

  // Calculer les pourcentages pour les graphiques circulaires
  getPercentage(count: number, items: { count: number }[]): number {
    const total = items.reduce((sum, item) => sum + item.count, 0);
    return total > 0 ? Math.round((count / total) * 100) : 0;
  }

  getNotificationClass(type: string): string {
    return `notification-${type}`;
  }
}

