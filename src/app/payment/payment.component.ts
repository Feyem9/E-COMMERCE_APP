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
        
        // 🔐 QR Code sécurisé avec signature
        if (result.data.qr_data) {
          this.qrCodeValue = JSON.stringify(result.data.qr_data);
          console.log('📱 QR Code sécurisé généré:', this.qrCodeValue);
        } else {
          // Fallback si qr_data absent
          this.qrCodeValue = result.data.transaction_id;
        }
        
        this.transactionId = result.data.transaction_id;
        this.loading = false;
      },
      error: (error: any) => { 
        console.error('Erreur paiement', error);
        this.loading = false;
      }
    });
  }
}
