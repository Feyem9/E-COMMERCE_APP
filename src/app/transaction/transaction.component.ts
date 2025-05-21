import { Component } from '@angular/core';
import { TransactionService } from '../services/transaction.service';

@Component({
  selector: 'app-transaction',
  templateUrl: './transaction.component.html',
  styleUrl: './transaction.component.scss'
})
export class TransactionComponent {
  constructor(private transactionService: TransactionService) {}

  payer() {
    const paymentData = {
      amount: 1000,
      currency: 'XAF',
      description: 'Paiement cours de guitare',
      // Ajoute d'autres champs si nécessaires
    };

    this.transactionService.initiatePayment(paymentData).subscribe({
      next: (response) => {
        if (response && response.payment_url) {
          window.location.href = response.payment_url; // Redirige vers la page de paiement PayUnit
        } else {
          alert('Erreur de redirection vers PayUnit.');
        }
      },
      error: (err) => {
        console.error('Erreur paiement :', err);
        alert('Erreur lors du paiement.');
      },
    });
  }
}
