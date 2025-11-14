import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-order-tracking',
  standalone: true,
  imports: [CommonModule, RouterModule, FormsModule],
  templateUrl: './order-tracking.component.html',
  styleUrls: ['./order-tracking.component.css']
})
export class OrderTrackingComponent {
  orderNumber: string = '';
  email: string = '';
  orderData: any = null;
  loading: boolean = false;

  searchOrder() {
    if (!this.orderNumber.trim()) {
      return;
    }

    this.loading = true;
    
    // Simuler une requête API
    setTimeout(() => {
      this.orderData = {
        orderNumber: this.orderNumber,
        status: 'In Transit',
        estimatedDelivery: '2025-11-16',
        items: [
          { name: 'iPhone 15 Pro', quantity: 1, price: 999 },
          { name: 'AirPods Pro', quantity: 1, price: 249 }
        ],
        total: 1248,
        trackingSteps: [
          { status: 'Order Placed', date: '2025-11-12', completed: true },
          { status: 'Processing', date: '2025-11-13', completed: true },
          { status: 'Shipped', date: '2025-11-14', completed: true },
          { status: 'In Transit', date: '2025-11-15', completed: true },
          { status: 'Out for Delivery', date: '2025-11-16', completed: false },
          { status: 'Delivered', date: '2025-11-16', completed: false }
        ]
      };
      this.loading = false;
    }, 1500);
  }

  resetSearch() {
    this.orderData = null;
    this.orderNumber = '';
    this.email = '';
  }
}