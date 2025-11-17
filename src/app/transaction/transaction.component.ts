import { Component } from '@angular/core';
import { TransactionService } from '../services/transaction.service';
import { CartService } from '../services/cart.service';

@Component({
  selector: 'app-transaction',
  templateUrl: './transaction.component.html',
  styleUrl: './transaction.component.scss'
})
export class TransactionComponent {
  constructor(private transactionService: TransactionService, private cartService: CartService) { }

  payer() {
    const paymentData = {
      amount: 1000,
      currency: 'XAF',
      description: 'Paiement cours de guitare',
      // Ajoute d'autres champs si nécessaires
    };

    this.transactionService.initiatePayment(paymentData).subscribe({
      next: (response: any) => {
        if (response && response.payment_url) {
          window.location.href = response.payment_url;
          this.cartService.clearCart();
        } else {
          alert('Erreur de redirection vers PayUnit.');
        }
      },
      error: (err: any) => {
        console.error('Erreur paiement :', err);
        alert('Erreur lors du paiement.');
      }
    });
  }
}
