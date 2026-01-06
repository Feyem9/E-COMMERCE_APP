import { Injectable, Inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { BehaviorSubject, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class PushNotificationService {
  private permission$ = new BehaviorSubject<NotificationPermission>('default');
  private token$ = new BehaviorSubject<string | null>(null);
  private isBrowser: boolean;

  constructor(@Inject(PLATFORM_ID) platformId: Object) {
    this.isBrowser = isPlatformBrowser(platformId);
    if (this.isBrowser) {
      this.checkPermission();
    }
  }

  /**
   * Get current permission status
   */
  getPermission(): Observable<NotificationPermission> {
    return this.permission$.asObservable();
  }

  /**
   * Get FCM token
   */
  getToken(): Observable<string | null> {
    return this.token$.asObservable();
  }

  /**
   * Check current notification permission
   */
  private checkPermission(): void {
    if ('Notification' in window) {
      this.permission$.next(Notification.permission);
    }
  }

  /**
   * Request notification permission
   */
  async requestPermission(): Promise<boolean> {
    if (!this.isBrowser || !('Notification' in window)) {
      console.warn('Notifications not supported');
      return false;
    }

    try {
      const permission = await Notification.requestPermission();
      this.permission$.next(permission);
      
      if (permission === 'granted') {
        await this.initializeFirebase();
        return true;
      } else {
        return false;
      }
    } catch (error) {
      console.error('Error requesting permission:', error);
      return false;
    }
  }

  /**
   * Initialize Firebase Messaging (when config is set)
   */
  private async initializeFirebase(): Promise<void> {
    try {
      // Firebase will be initialized here once config is set
      // Import Firebase dynamically to avoid issues in SSR
      
      /* 
      // Uncomment when Firebase is configured:
      const { initializeApp } = await import('firebase/app');
      const { getMessaging, getToken, onMessage } = await import('firebase/messaging');
      const { firebaseConfig, vapidKey } = await import('../../environment/firebase.config');
      
      const app = initializeApp(firebaseConfig);
      const messaging = getMessaging(app);
      
      const token = await getToken(messaging, { vapidKey });
      this.token$.next(token);
      
      // Listen for messages when app is in foreground
      onMessage(messaging, (payload) => {
        this.showNotification(payload);
      });
      */
      
    } catch (error) {
      console.error('Firebase initialization error:', error);
    }
  }

  /**
   * Show a local notification
   */
  showNotification(options: {
    title: string;
    body: string;
    icon?: string;
    data?: any;
  }): void {
    if (!this.isBrowser || Notification.permission !== 'granted') {
      return;
    }

    // Note: 'vibrate' n'est pas dans le type standard NotificationOptions
    // mais est supporté par certains navigateurs mobiles
    const notificationOptions: NotificationOptions = {
      body: options.body,
      icon: options.icon || '/icons/icon-192x192.png',
      badge: '/icons/icon-72x72.png',
      data: options.data,
      silent: false
    };

    const notification = new Notification(options.title, notificationOptions);

    notification.onclick = () => {
      window.focus();
      notification.close();
    };
  }

  /**
   * Subscribe to a topic (server-side implementation needed)
   */
  async subscribeToTopic(topic: string): Promise<void> {
    const token = this.token$.value;
    if (!token) {
      console.warn('No FCM token available');
      return;
    }

    // Send to your backend to subscribe token to topic
    // TODO: Implement backend call
  }

  /**
   * Unsubscribe from a topic
   */
  async unsubscribeFromTopic(topic: string): Promise<void> {
    const token = this.token$.value;
    if (!token) return;

    // TODO: Implement backend call
  }
}
