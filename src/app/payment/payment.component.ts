import { Component } from '@angular/core';
import { TransactionService } from '../services/transaction.service';

@Component({
  selector: 'app-payment',
  templateUrl: './payment.component.html',
})
export class PaymentComponent {
  qrCodeValue: string = '';
  paymentUrl: string = '';
  loading = false;

  constructor(private transactionService: TransactionService) { }

  async startPayment() {
    this.loading = true;
    try {
      const data = {
        total_amount: 1000,
        currency: 'XAF',
        return_url: 'http://localhost:4200/payment-success',
        notify_url: 'http://127.0.0.1:5000/transactions/notify',
        payment_country: 'CM'
      };

      const result = await this.transactionService.initiatePayment(data);
      console.log('Paiement initié:', result);

      this.paymentUrl = result.payment_url;
      this.qrCodeValue = result.data.t_id; // QR = transaction ID ou token sécurisé
    } catch (error) {
      console.error('Erreur paiement', error);
    } finally {
      this.loading = false;
    }
  }
}
