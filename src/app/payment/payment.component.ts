import { Component } from '@angular/core';
import { TransactionService } from '../services/transaction.service';
import { environment } from '../../environment/environment';
import { Inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';

@Component({
  selector: 'app-payment',
  templateUrl: './payment.component.html',
})
export class PaymentComponent {
  qrCodeValue: string = '';
  paymentUrl: string = '';
  transactionId: string = '';
  loading = false;
  validationMessage: string = '';
  validationSuccess: boolean = false;

  constructor(
    private transactionService: TransactionService,
    @Inject(PLATFORM_ID) private platformId: Object
  ) { }
 
  startPayment() {
    this.loading = true; 
    this.validationMessage = '';
    this.validationSuccess = false;

    // Determine current host for return_url
    let returnUrl = 'https://staging-market.vercel.app/payment-success'; // Fallback staging
    if (isPlatformBrowser(this.platformId)) {
        returnUrl = `${window.location.origin}/payment-success`;
    }

    const data = {
      total_amount: 1000,
      currency: 'XAF',
      // return_url: 'https://e-commerce-app-0hnw.onrender.com/payment-success',
      // notify_url: 'https://e-commerce-app-0hnw.onrender.com/transactions/notify',
      return_url: returnUrl,
      notify_url: `${environment.apiUrl}/transactions/notify`,
      payment_country: 'CM'
    };

    this.transactionService.initiatePayment(data).subscribe({
      next: (result: any) => {
        console.log('Paiement initié:', result);
        this.paymentUrl = result.payment_url;
        this.qrCodeValue = result.data.t_id; // QR = transaction ID ou token sécurisé
        this.transactionId = result.data.transaction_id;
        this.loading = false;
      },
      error: (error: any) => { 
        console.error('Erreur paiement', error);
        this.loading = false;
      }
    });
  }

  validateTransaction() {
    if (!this.qrCodeValue) {
      this.validationMessage = 'Aucun QR code disponible pour validation';
      this.validationSuccess = false;
      return;
    }

    this.loading = true;
    this.validationMessage = 'Validation en cours...';

    // Appeler le backend pour valider la transaction
    this.transactionService.validateTransaction(this.qrCodeValue).subscribe({
      next: (response: any) => {
        this.validationMessage = 'Transaction validée avec succès !';
        this.validationSuccess = true;
        this.loading = false;
      },
      error: (error: any) => {
        this.validationMessage = 'Échec de la validation: ' + (error.error?.message || 'Erreur inconnue');
        this.validationSuccess = false;
        this.loading = false;
      }
    });
  }
}
