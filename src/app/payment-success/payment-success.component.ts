import { Component, OnInit } from '@angular/core';
import { CartService } from '../services/cart.service';
import { ActivatedRoute } from '@angular/router';
import { AnalyticsService } from '../services/analytics.service';

@Component({
  selector: 'app-payment-success',
  templateUrl: './payment-success.component.html',
  styleUrl: './payment-success.component.scss'
})
export class PaymentSuccessComponent implements OnInit {
  transactionId: string | null = null;
  transactionAmount: string | null = null;

  constructor(
    private route: ActivatedRoute,
    private cartService: CartService,
    private analytics: AnalyticsService
  ) { }

  ngOnInit() {
    this.transactionId = this.route.snapshot.queryParamMap.get('transaction_id');
    this.transactionAmount = this.route.snapshot.queryParamMap.get('transaction_amount');

    // 📊 Track payment results
    const status = this.route.snapshot.queryParamMap.get('transaction_status');
    
    if (status === 'SUCCESS') {
      // ✅ Track successful purchase
      this.analytics.trackPurchase({
        transactionId: this.transactionId || 'TRANS-' + Date.now(),
        value: Number(this.transactionAmount) || 0,
        items: [] // On pourrait passer les items du panier ici si on les a encore
      });
      this.cartService.clearCart();
    } else {
      // ❌ Track failed/cancelled payment
      this.analytics.trackEvent('payment_failed', {
        transaction_id: this.transactionId,
        status: status
      });
    }
  }
}
