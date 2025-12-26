import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { TransactionService } from '../../services/transaction.service';
import { CartService } from '../../services/cart.service';

@Component({
  selector: 'app-payment-success',
  templateUrl: './payment-success.component.html',
  styleUrls: ['./payment-success.component.scss']
})
export class PaymentSuccessComponent implements OnInit {  
  transactionId: string = '';
  transactionStatus: string = 'pending'; // Statut initial toujours "pending"
  transactionAmount: string = '';
  transactionGateway: string = '';
  loading: boolean = true;
  validationMessage: string = '';
  validationSuccess: boolean = false;
  qrCodeValue: string = '';
   
  constructor( 
    private route: ActivatedRoute,
    private transactionService: TransactionService,
    private cartService: CartService
  ) { }

  ngOnInit(): void {
    // Récupérer les paramètres de l'URL
    this.route.queryParams.subscribe(params => {
      this.transactionId = params['transaction_id'] || '';
      // Ne pas utiliser le statut des paramètres, toujours commencer par "pending"
      this.transactionAmount = params['transaction_amount'] || '';
      this.transactionGateway = params['transaction_gateway'] || '';

      // Si nous avons un ID de transaction, récupérer les données complètes depuis le backend
      if (this.transactionId) {
        this.loadTransactionData();
      } else {
        this.loading = false;
      }
    });
  }

  // Récupérer les données de la transaction depuis le backend (avec signature)
  loadTransactionData(): void {
    this.transactionService.getTransaction(this.transactionId).subscribe({
      next: (transaction: any) => {
        console.log('📦 Transaction récupérée:', transaction);
        
        // 🔐 Créer le JSON complet pour le QR code AVEC la signature du backend
        const qrData = {
          transaction_id: transaction.transaction_id,
          reference: transaction.reference || `CMD-${new Date().toISOString().split('T')[0].replace(/-/g, '')}-${this.transactionId.slice(-6)}`,
          amount: transaction.total_amount || parseFloat(this.transactionAmount) || 0,
          currency: transaction.currency || 'XAF',
          status: transaction.status || 'pending',
          timestamp: transaction.qr_timestamp || transaction.created_at || new Date().toISOString(),  // 🔐 Utiliser qr_timestamp
          signature: transaction.qr_signature || ''  // 🔐 SIGNATURE du backend
        };
        
        this.qrCodeValue = JSON.stringify(qrData);
        console.log('📱 QR Code généré (avec signature):', this.qrCodeValue);
        
        this.transactionStatus = transaction.status || 'pending';
        this.validationMessage = 'Veuillez scanner ce QR code pour valider votre transaction.';
        this.loading = false;
      },
      error: (error: any) => {
        console.error('❌ Erreur récupération transaction:', error);
        
        // Fallback: créer QR sans signature (pour compatibilité ancien format)
        const qrData = {
          transaction_id: this.transactionId,
          reference: `CMD-${new Date().toISOString().split('T')[0].replace(/-/g, '')}-${this.transactionId.slice(-6)}`,
          amount: parseFloat(this.transactionAmount) || 0,
          currency: 'XAF',
          status: 'pending',
          timestamp: new Date().toISOString()
        };
        this.qrCodeValue = JSON.stringify(qrData);
        console.log('⚠️ QR Code généré (sans signature - fallback):', this.qrCodeValue);
        
        this.validationMessage = 'Veuillez scanner ce QR code pour valider votre transaction.';
        this.loading = false;
      }
    });
  }

  // Méthode pour valider manuellement après scan du QR code
  validateTransaction(): void {
    if (!this.qrCodeValue) {
      this.validationMessage = 'Aucun QR code disponible pour validation';
      this.validationSuccess = false;
      return;
    }

    this.validationMessage = 'Validation en cours... Merci de patienter.';

    // Appeler le backend pour valider la transaction
    this.transactionService.validateTransaction(this.qrCodeValue).subscribe({
      next: (response: any) => {
        this.validationMessage = 'Félicitations ! Votre transaction a été validée avec succès. Vous pouvez maintenant quitter cette page.';
        this.validationSuccess = true;
        this.transactionStatus = 'completed'; // Mettre à jour le statut localement

        // Vider le panier après validation réussie
        this.cartService.clearCart();
      },
      error: (error: any) => {
        this.validationMessage = 'Nous rencontrons un problème technique. Votre transaction sera validée dans quelques instants. Merci de votre patience.';
        this.validationSuccess = false;
        console.error('Erreur de validation:', error);
      }
    });
  }
}