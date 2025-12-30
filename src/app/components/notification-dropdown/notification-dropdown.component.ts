import { Component, OnInit, OnDestroy, HostListener, ElementRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';
import { NotificationService, Notification } from '../../services/notification.service';

@Component({
  selector: 'app-notification-dropdown',
  standalone: true,
  imports: [CommonModule, RouterModule],
  template: `
    <div class="notification-container">
      <!-- Bell Icon with Badge -->
      <button class="notification-bell" (click)="toggleDropdown()">
        <i class="fas fa-bell"></i>
        <span class="badge" *ngIf="unreadCount > 0">{{ unreadCount > 9 ? '9+' : unreadCount }}</span>
      </button>

      <!-- Dropdown -->
      <div class="notification-dropdown" *ngIf="isOpen" [@fadeIn]>
        <div class="dropdown-header">
          <h4>🔔 Notifications</h4>
          <button 
            class="mark-all-btn" 
            *ngIf="unreadCount > 0"
            (click)="markAllRead()">
            Tout marquer lu
          </button>
        </div>

        <div class="notification-list" *ngIf="notifications.length > 0">
          <div 
            *ngFor="let notif of notifications" 
            class="notification-item"
            [class.unread]="!notif.read"
            (click)="handleNotificationClick(notif)">
            
            <div class="notif-icon" [ngClass]="'type-' + notif.type">
              {{ notif.icon || getDefaultIcon(notif.type) }}
            </div>
            
            <div class="notif-content">
              <div class="notif-title">{{ notif.title }}</div>
              <div class="notif-message">{{ notif.message }}</div>
              <div class="notif-time">{{ getTimeAgo(notif.timestamp) }}</div>
            </div>
            
            <button 
              class="notif-close" 
              (click)="removeNotification(notif.id, $event)">
              ✕
            </button>
          </div>
        </div>

        <div class="empty-state" *ngIf="notifications.length === 0">
          <i class="fas fa-bell-slash"></i>
          <p>Aucune notification</p>
        </div>

        <div class="dropdown-footer" *ngIf="notifications.length > 0">
          <button class="clear-all-btn" (click)="clearAll()">
            Effacer tout
          </button>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .notification-container {
      position: relative;
      display: inline-block;
    }

    .notification-bell {
      background: transparent;
      border: none;
      cursor: pointer;
      position: relative;
      padding: 8px;
      font-size: 1.2rem;
      color: #64748b;
      transition: color 0.2s ease;

      &:hover {
        color: #334155;
      }

      .badge {
        position: absolute;
        top: 2px;
        right: 2px;
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        font-size: 0.65rem;
        font-weight: 700;
        padding: 2px 5px;
        border-radius: 10px;
        min-width: 16px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(239, 68, 68, 0.4);
      }
    }

    .notification-dropdown {
      position: absolute;
      top: 100%;
      right: 0;
      width: 340px;
      max-height: 450px;
      background: white;
      border-radius: 16px;
      box-shadow: 0 20px 60px rgba(15, 23, 42, 0.15);
      z-index: 1000;
      overflow: hidden;
      border: 1px solid rgba(148, 163, 184, 0.2);
    }

    .dropdown-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 16px 20px;
      border-bottom: 1px solid #e2e8f0;
      background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);

      h4 {
        margin: 0;
        font-size: 1rem;
        font-weight: 700;
        color: #1e293b;
      }

      .mark-all-btn {
        background: none;
        border: none;
        color: #3b82f6;
        font-size: 0.8rem;
        cursor: pointer;
        font-weight: 600;

        &:hover {
          text-decoration: underline;
        }
      }
    }

    .notification-list {
      max-height: 320px;
      overflow-y: auto;
    }

    .notification-item {
      display: flex;
      align-items: flex-start;
      gap: 12px;
      padding: 14px 20px;
      cursor: pointer;
      transition: background 0.2s ease;
      border-bottom: 1px solid #f1f5f9;
      position: relative;

      &:hover {
        background: #f8fafc;
      }

      &.unread {
        background: linear-gradient(135deg, #eff6ff 0%, #f0f9ff 100%);
        
        &::before {
          content: '';
          position: absolute;
          left: 0;
          top: 0;
          bottom: 0;
          width: 4px;
          background: linear-gradient(180deg, #3b82f6 0%, #2563eb 100%);
        }
      }

      .notif-icon {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.1rem;
        flex-shrink: 0;

        &.type-success { background: #dcfce7; }
        &.type-error { background: #fee2e2; }
        &.type-warning { background: #fef3c7; }
        &.type-info { background: #dbeafe; }
      }

      .notif-content {
        flex: 1;
        min-width: 0;

        .notif-title {
          font-weight: 600;
          font-size: 0.9rem;
          color: #1e293b;
          margin-bottom: 2px;
        }

        .notif-message {
          font-size: 0.8rem;
          color: #64748b;
          line-height: 1.4;
          overflow: hidden;
          text-overflow: ellipsis;
          display: -webkit-box;
          -webkit-line-clamp: 2;
          -webkit-box-orient: vertical;
        }

        .notif-time {
          font-size: 0.7rem;
          color: #94a3b8;
          margin-top: 4px;
        }
      }

      .notif-close {
        background: none;
        border: none;
        color: #94a3b8;
        cursor: pointer;
        padding: 4px;
        font-size: 0.8rem;
        opacity: 0;
        transition: opacity 0.2s ease;

        &:hover {
          color: #ef4444;
        }
      }

      &:hover .notif-close {
        opacity: 1;
      }
    }

    .empty-state {
      padding: 40px 20px;
      text-align: center;
      color: #94a3b8;

      i {
        font-size: 2.5rem;
        margin-bottom: 12px;
        display: block;
      }

      p {
        margin: 0;
        font-size: 0.9rem;
      }
    }

    .dropdown-footer {
      padding: 12px 20px;
      border-top: 1px solid #e2e8f0;
      background: #f8fafc;
      text-align: center;

      .clear-all-btn {
        background: none;
        border: none;
        color: #ef4444;
        font-size: 0.85rem;
        cursor: pointer;
        font-weight: 600;

        &:hover {
          text-decoration: underline;
        }
      }
    }
  `]
})
export class NotificationDropdownComponent implements OnInit, OnDestroy {
  notifications: Notification[] = [];
  unreadCount = 0;
  isOpen = false;
  private destroy$ = new Subject<void>();

  constructor(
    private notificationService: NotificationService,
    private elementRef: ElementRef
  ) {}

  ngOnInit(): void {
    this.notificationService.getNotifications()
      .pipe(takeUntil(this.destroy$))
      .subscribe(notifications => {
        this.notifications = notifications;
      });

    this.notificationService.getUnreadCount()
      .pipe(takeUntil(this.destroy$))
      .subscribe(count => {
        this.unreadCount = count;
      });

    // Demander la permission pour les notifications navigateur
    this.notificationService.requestPermission();
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  @HostListener('document:click', ['$event'])
  onDocumentClick(event: Event): void {
    if (!this.elementRef.nativeElement.contains(event.target)) {
      this.isOpen = false;
    }
  }

  toggleDropdown(): void {
    this.isOpen = !this.isOpen;
  }

  markAllRead(): void {
    this.notificationService.markAllAsRead();
  }

  handleNotificationClick(notification: Notification): void {
    if (!notification.read) {
      this.notificationService.markAsRead(notification.id);
    }
    
    if (notification.action) {
      // Navigation sera gérée par le routerLink
      this.isOpen = false;
    }
  }

  removeNotification(id: string, event: Event): void {
    event.stopPropagation();
    this.notificationService.removeNotification(id);
  }

  clearAll(): void {
    this.notificationService.clearAll();
  }

  getDefaultIcon(type: string): string {
    const icons: Record<string, string> = {
      success: '✅',
      error: '❌',
      warning: '⚠️',
      info: 'ℹ️'
    };
    return icons[type] || '📢';
  }

  getTimeAgo(date: Date): string {
    const now = new Date();
    const diff = now.getTime() - new Date(date).getTime();
    
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(diff / 3600000);
    const days = Math.floor(diff / 86400000);

    if (minutes < 1) return "À l'instant";
    if (minutes < 60) return `Il y a ${minutes} min`;
    if (hours < 24) return `Il y a ${hours}h`;
    if (days < 7) return `Il y a ${days}j`;
    
    return new Date(date).toLocaleDateString('fr-FR', {
      day: '2-digit',
      month: 'short'
    });
  }
}
