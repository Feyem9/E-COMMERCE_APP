import { Component, OnInit, OnDestroy } from '@angular/core';
import { AdminService, DashboardStats, RevenueStats, RecentActivity } from '../services/admin.service';
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
  
  loading = true;
  error: string | null = null;
  
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
}
