import { Component, Inject, PLATFORM_ID } from '@angular/core';
import { TransactionService } from '../services/transaction.service';
import { environment } from '../../environment/environment';
import { isPlatformBrowser } from '@angular/common';
import { AnalyticsService } from '../services/analytics.service';

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
    private analytics: AnalyticsService,
    @Inject(PLATFORM_ID) private platformId: Object
  ) { }
 
  startPayment() {
    this.loading = true;

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
        // 📊 Track checkout start
        this.analytics.trackEvent('begin_checkout', {
          total_amount: data.total_amount,
          currency: data.currency,
          payment_country: data.payment_country
        });

        
        this.paymentUrl = result.payment_url;
        this.transactionId = result.data.transaction_id;
        
        // 🔐 QR Code sécurisé avec signature - TOUJOURS utiliser qr_data
        if (result.data && result.data.qr_data) {
          this.qrCodeValue = JSON.stringify(result.data.qr_data);
        } else {
          // Si qr_data n'existe pas, créer le JSON manuellement
          console.warn('⚠️ qr_data absent, création manuelle du JSON');
          const qrData = {
            transaction_id: result.data.transaction_id,
            reference: result.data.reference || `CMD-${new Date().toISOString().split('T')[0]}-${result.data.transaction_id.slice(-6)}`,
            amount: result.data.total_amount || data.total_amount,
            currency: result.data.currency || data.currency,
            status: 'pending',
            timestamp: new Date().toISOString()
          };
          this.qrCodeValue = JSON.stringify(qrData);
        }
        
        // 📊 Track QR code generation
        this.analytics.trackEvent('qr_code_generated', {
          transaction_id: this.transactionId
        });
        
        this.loading = false;
      },
      error: (error: any) => { 
        console.error('Erreur paiement', error);
        this.loading = false;
      }
    });
  }
}
