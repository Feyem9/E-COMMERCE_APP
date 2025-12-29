import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environment/environment';

export interface DashboardStats {
  users: { total: number; new_today: number };
  products: { total: number; low_stock: number };
  orders: { total: number; pending: number };
  transactions: { total: number; completed: number };
  revenue: { total: number; today: number; monthly: number };
} 

export interface RevenueStats {
  daily_revenue: { date: string; amount: number; count: number }[];
  period: { start: string; end: string };
}

export interface RecentActivity {
  recent_transactions: any[];
  recent_users: any[];
  recent_orders: any[];
}

export interface PaginatedResponse<T> {
  data: T[];
  pagination: {
    page: number;
    per_page: number;
    total: number;
    pages: number;
    has_next: boolean;
    has_prev: boolean;
  };
}

export interface User {
  id: number;
  name: string;
  email: string;
  contact: string;
  address: string;
  role: string;
  confirmed: boolean;
  is_active: boolean;
  created_at: string;
}

export interface Product {
  id: number;
  name: string;
  description: string;
  current_price: number;
  discount_price: number;
  quantity: number;
  picture: string;
  created_at: string;
}

export interface Order {
  id: number;
  quantity: number;
  price: number;
  status: string;
  cart_id: number;
  created_at: string;
}

export interface Transaction {
  transaction_id: string;
  status: string;
  total_amount: number;
  currency: string;
  redirect_url: string;
  customer_latitude: number;
  customer_longitude: number;
  delivery_distance_km: number;
  delivery_map_url: string;
  reference: string;
  created_at: string;
}

@Injectable({
  providedIn: 'root'
})
export class AdminService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  // ============================================
  // DASHBOARD STATISTICS
  // ============================================
  getDashboardStats(): Observable<DashboardStats> {
    return this.http.get<DashboardStats>(`${this.apiUrl}/admin/stats`);
  }

  getRevenueStats(): Observable<RevenueStats> {
    return this.http.get<RevenueStats>(`${this.apiUrl}/admin/stats/revenue`);
  }

  getRecentActivity(): Observable<RecentActivity> {
    return this.http.get<RecentActivity>(`${this.apiUrl}/admin/activity/recent`);
  }

  // ============================================
  // USER MANAGEMENT
  // ============================================
  getUsers(page: number = 1, perPage: number = 10, search: string = '', role: string = ''): Observable<any> {
    let params = new HttpParams()
      .set('page', page.toString())
      .set('per_page', perPage.toString());
    
    if (search) params = params.set('search', search);
    if (role) params = params.set('role', role);

    return this.http.get<any>(`${this.apiUrl}/admin/users`, { params });
  }

  getUserById(userId: number): Observable<User> {
    return this.http.get<User>(`${this.apiUrl}/admin/users/${userId}`);
  }

  updateUserStatus(userId: number, data: { is_active?: boolean; role?: string; confirmed?: boolean }): Observable<any> {
    return this.http.patch<any>(`${this.apiUrl}/admin/users/${userId}/status`, data);
  }

  deleteUser(userId: number): Observable<any> {
    return this.http.delete<any>(`${this.apiUrl}/admin/users/${userId}`);
  }

  // ============================================
  // PRODUCT MANAGEMENT
  // ============================================
  getProducts(page: number = 1, perPage: number = 10, search: string = ''): Observable<any> {
    let params = new HttpParams()
      .set('page', page.toString())
      .set('per_page', perPage.toString());
    
    if (search) params = params.set('search', search);

    return this.http.get<any>(`${this.apiUrl}/admin/products`, { params });
  }

  createProduct(product: Partial<Product>): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/admin/products`, product);
  }

  updateProduct(productId: number, product: Partial<Product>): Observable<any> {
    return this.http.put<any>(`${this.apiUrl}/admin/products/${productId}`, product);
  }

  deleteProduct(productId: number): Observable<any> {
    return this.http.delete<any>(`${this.apiUrl}/admin/products/${productId}`);
  }

  // ============================================
  // ORDER MANAGEMENT
  // ============================================
  getOrders(page: number = 1, perPage: number = 10, status: string = ''): Observable<any> {
    let params = new HttpParams()
      .set('page', page.toString())
      .set('per_page', perPage.toString());
    
    if (status) params = params.set('status', status);

    return this.http.get<any>(`${this.apiUrl}/admin/orders`, { params });
  }

  updateOrderStatus(orderId: number, status: string): Observable<any> {
    return this.http.patch<any>(`${this.apiUrl}/admin/orders/${orderId}/status`, { status });
  }

  // ============================================
  // TRANSACTION MANAGEMENT
  // ============================================
  getTransactions(page: number = 1, perPage: number = 10, status: string = ''): Observable<any> {
    let params = new HttpParams()
      .set('page', page.toString())
      .set('per_page', perPage.toString());
    
    if (status) params = params.set('status', status);

    return this.http.get<any>(`${this.apiUrl}/admin/transactions`, { params });
  }

  // ============================================
  // EXPORT CSV
  // ============================================
  exportUsersCSV(): Observable<Blob> {
    return this.http.get(`${this.apiUrl}/admin/export/users`, { responseType: 'blob' });
  }

  exportOrdersCSV(): Observable<Blob> {
    return this.http.get(`${this.apiUrl}/admin/export/orders`, { responseType: 'blob' });
  }

  exportTransactionsCSV(): Observable<Blob> {
    return this.http.get(`${this.apiUrl}/admin/export/transactions`, { responseType: 'blob' });
  }

  // ============================================
  // ADVANCED CHARTS DATA
  // ============================================
  getChartsData(): Observable<ChartsData> {
    return this.http.get<ChartsData>(`${this.apiUrl}/admin/charts`);
  }

  // ============================================
  // NOTIFICATIONS
  // ============================================
  getNotifications(): Observable<NotificationsResponse> {
    return this.http.get<NotificationsResponse>(`${this.apiUrl}/admin/notifications`);
  }
}

// Interfaces pour les nouvelles fonctionnalités
export interface ChartsData {
  orders_by_status: { status: string; count: number }[];
  users_by_role: { role: string; count: number }[];
  top_products: { name: string; total_sold: number }[];
  monthly_revenue: { month: string; amount: number }[];
  weekly_signups: { week: string; count: number }[];
}

export interface AdminNotification {
  type: 'warning' | 'info' | 'success' | 'danger';
  icon: string;
  title: string;
  message: string;
  action: string;
  priority: 'high' | 'medium' | 'low';
}

export interface NotificationsResponse {
  notifications: AdminNotification[];
  count: number;
}
