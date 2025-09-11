import { Component, OnInit } from '@angular/core';
import { CartService } from '../services/cart.service';
import { ActivatedRoute } from '@angular/router';

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
    private cartService: CartService
  ) { }

  ngOnInit() {
    this.transactionId = this.route.snapshot.queryParamMap.get('transaction_id');
    this.transactionAmount = this.route.snapshot.queryParamMap.get('transaction_amount');

    // Vider le panier seulement si paiement réussi
    const status = this.route.snapshot.queryParamMap.get('transaction_status');
    if (status === 'SUCCESS') {
      this.cartService.clearCart();
    }
  }
}
