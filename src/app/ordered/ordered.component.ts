import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

interface Order {
  id: string;
  date: string;
  status: 'Processing' | 'Shipped' | 'Delivered' | 'Cancelled';
  total: number;
  items: number;
  trackingNumber?: string;
}

interface OrderItem {
  id: number;
  name: string;
  price: number;
  quantity: number;
  image: string;
}

@Component({
  selector: 'app-ordered',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './ordered.component.html',
  styleUrl: './ordered.component.scss'
})
export class OrderedComponent implements OnInit {
  orders: Order[] = [];
  selectedOrder: Order | null = null;
  orderDetails: OrderItem[] = [];
  loading: boolean = true;
  error: string | null = null;
  showDetails: boolean = false;

  ngOnInit(): void {
    this.loadOrders();
  }

  loadOrders(): void {
    // Simuler le chargement des commandes
    setTimeout(() => {
      this.orders = [
        {
          id: 'ORD-2023-001',
          date: '2023-11-15',
          status: 'Delivered',
          total: 1249.98,
          items: 2,
          trackingNumber: 'UP123456789US'
        },
        {
          id: 'ORD-2023-002',
          date: '2023-10-28',
          status: 'Shipped',
          total: 899.99,
          items: 1,
          trackingNumber: 'FD987654321US'
        },
        {
          id: 'ORD-2023-003',
          date: '2023-09-12',
          status: 'Processing',
          total: 249.99,
          items: 1
        },
        {
          id: 'ORD-2023-004',
          date: '2023-08-05',
          status: 'Delivered',
          total: 1999.99,
          items: 1,
          trackingNumber: 'UP555123456US'
        }
      ];
      this.loading = false;
    }, 1200);
  }

  viewOrderDetails(order: Order): void {
    this.selectedOrder = order;
    this.showDetails = true;

    // Simuler le chargement des détails de commande
    setTimeout(() => {
      this.orderDetails = [
        {
          id: 1,
          name: 'iPhone 15 Pro Max',
          price: 1199.99,
          quantity: 1,
          image: 'https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/iphone-15-pro-model-unselect-gallery-1-202309?wid=5120&hei=2880&fmt=p-jpg&qlt=80&.v=1692931459062'
        },
        {
          id: 2,
          name: 'AirPods Pro 2nd Gen',
          price: 249.99,
          quantity: 1,
          image: 'https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/airpods-pro-2nd-gen-hero-202209?wid=2000&hei=2000&fmt=jpeg&qlt=90&.v=1661743961000'
        }
      ];
    }, 500);
  }

  backToOrders(): void {
    this.showDetails = false;
    this.selectedOrder = null;
    this.orderDetails = [];
  }

  getStatusBadgeClass(status: string): string {
    switch (status) {
      case 'Delivered': return 'bg-success';
      case 'Shipped': return 'bg-info';
      case 'Processing': return 'bg-warning';
      case 'Cancelled': return 'bg-danger';
      default: return 'bg-secondary';
    }
  }

  trackOrder(trackingNumber: string): void {
    // Logique pour suivre la commande
  }

  reorder(orderId: string): void {
    // Logique pour passer une nouvelle commande
  }
}
