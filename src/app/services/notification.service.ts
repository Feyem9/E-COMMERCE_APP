import { Injectable, Inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { BehaviorSubject, Observable } from 'rxjs';

export interface Notification {
  id: string;
  type: 'success' | 'error' | 'warning' | 'info';
  title: string;
  message: string;
  timestamp: Date;
  read: boolean;
  action?: string;
  icon?: string;
}

@Injectable({
  providedIn: 'root'
})
export class NotificationService {
  private notifications$ = new BehaviorSubject<Notification[]>([]);
  private unreadCount$ = new BehaviorSubject<number>(0);
  private isBrowser: boolean;

  constructor(@Inject(PLATFORM_ID) platformId: Object) {
    this.isBrowser = isPlatformBrowser(platformId);
    this.loadStoredNotifications();
  }

  // Récupérer toutes les notifications
  getNotifications(): Observable<Notification[]> {
    return this.notifications$.asObservable();
  }

  // Récupérer le nombre de non-lues
  getUnreadCount(): Observable<number> {
    return this.unreadCount$.asObservable();
  }

  // Ajouter une notification
  addNotification(notification: Omit<Notification, 'id' | 'timestamp' | 'read'>): void {
    const newNotification: Notification = {
      ...notification,
      id: this.generateId(),
      timestamp: new Date(),
      read: false
    };

    const current = this.notifications$.value;
    const updated = [newNotification, ...current].slice(0, 50); // Max 50 notifications
    
    this.notifications$.next(updated);
    this.updateUnreadCount(updated);
    this.saveNotifications(updated);
    
    // Afficher une notification navigateur si autorisé
    this.showBrowserNotification(notification);
  }

  // Notifications prédéfinies
  notifyOrderStatusChange(reference: string, status: string): void {
    const statusConfig = this.getStatusConfig(status);
    this.addNotification({
      type: statusConfig.type,
      title: statusConfig.title,
      message: `La commande ${reference} est maintenant ${statusConfig.label}`,
      icon: statusConfig.icon,
      action: '/order-tracking'
    });
  }

  notifyPaymentSuccess(amount: number, currency: string = 'XAF'): void {
    this.addNotification({
      type: 'success',
      title: 'Paiement confirmé',
      message: `Votre paiement de ${amount.toLocaleString()} ${currency} a été reçu`,
      icon: '💳',
      action: '/profile'
    });
  }

  notifyDeliveryComplete(reference: string): void {
    this.addNotification({
      type: 'success',
      title: 'Livraison effectuée',
      message: `Votre commande ${reference} a été livrée avec succès !`,
      icon: '📦',
      action: '/profile'
    });
  }

  notifyNewProduct(productName: string): void {
    this.addNotification({
      type: 'info',
      title: 'Nouveau produit',
      message: `${productName} est maintenant disponible !`,
      icon: '✨',
      action: '/product'
    });
  }

  notifyLowStock(productName: string, quantity: number): void {
    this.addNotification({
      type: 'warning',
      title: 'Stock faible',
      message: `Plus que ${quantity} unités de ${productName} disponibles`,
      icon: '⚠️'
    });
  }

  // Marquer comme lu
  markAsRead(notificationId: string): void {
    const current = this.notifications$.value;
    const updated = current.map(n => 
      n.id === notificationId ? { ...n, read: true } : n
    );
    
    this.notifications$.next(updated);
    this.updateUnreadCount(updated);
    this.saveNotifications(updated);
  }

  // Marquer toutes comme lues
  markAllAsRead(): void {
    const current = this.notifications$.value;
    const updated = current.map(n => ({ ...n, read: true }));
    
    this.notifications$.next(updated);
    this.updateUnreadCount(updated);
    this.saveNotifications(updated);
  }

  // Supprimer une notification
  removeNotification(notificationId: string): void {
    const current = this.notifications$.value;
    const updated = current.filter(n => n.id !== notificationId);
    
    this.notifications$.next(updated);
    this.updateUnreadCount(updated);
    this.saveNotifications(updated);
  }

  // Effacer toutes les notifications
  clearAll(): void {
    this.notifications$.next([]);
    this.unreadCount$.next(0);
    this.saveNotifications([]);
  }

  // Demander la permission pour les notifications navigateur
  requestPermission(): void {
    if (this.isBrowser && 'Notification' in window) {
      Notification.requestPermission();
    }
  }

  // ========== PRIVATE METHODS ==========

  private generateId(): string {
    return `notif_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  private updateUnreadCount(notifications: Notification[]): void {
    const count = notifications.filter(n => !n.read).length;
    this.unreadCount$.next(count);
  }

  private loadStoredNotifications(): void {
    if (this.isBrowser) {
      try {
        const stored = localStorage.getItem('notifications');
        if (stored) {
          const parsed = JSON.parse(stored) as Notification[];
          // Convertir les dates
          const notifications = parsed.map(n => ({
            ...n,
            timestamp: new Date(n.timestamp)
          }));
          this.notifications$.next(notifications);
          this.updateUnreadCount(notifications);
        }
      } catch (e) {
        console.error('Error loading notifications:', e);
      }
    }
  }

  private saveNotifications(notifications: Notification[]): void {
    if (this.isBrowser) {
      try {
        localStorage.setItem('notifications', JSON.stringify(notifications));
      } catch (e) {
        console.error('Error saving notifications:', e);
      }
    }
  }

  private showBrowserNotification(notification: { title: string; message: string; icon?: string }): void {
    if (this.isBrowser && 'Notification' in window && Notification.permission === 'granted') {
      new Notification(notification.title, {
        body: notification.message,
        icon: '/assets/icons/icon-192x192.png',
        badge: '/assets/icons/badge-72x72.png'
      });
    }
  }

  private getStatusConfig(status: string): { type: 'success' | 'info' | 'warning'; title: string; label: string; icon: string } {
    const configs: Record<string, { type: 'success' | 'info' | 'warning'; title: string; label: string; icon: string }> = {
      'pending': { type: 'info', title: 'Commande en attente', label: 'en attente de traitement', icon: '🕐' },
      'confirmed': { type: 'info', title: 'Commande confirmée', label: 'confirmée', icon: '✅' },
      'processing': { type: 'info', title: 'En préparation', label: 'en cours de préparation', icon: '📦' },
      'shipped': { type: 'info', title: 'Commande expédiée', label: 'expédiée', icon: '🚚' },
      'delivered': { type: 'success', title: 'Commande livrée', label: 'livrée', icon: '🎉' },
      'cancelled': { type: 'warning', title: 'Commande annulée', label: 'annulée', icon: '❌' }
    };
    
    return configs[status] || { type: 'info', title: 'Mise à jour commande', label: status, icon: '📋' };
  }
}
