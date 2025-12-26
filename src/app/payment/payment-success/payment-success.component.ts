import { Component, OnInit, OnDestroy } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { TransactionService } from '../../services/transaction.service';
import { CartService } from '../../services/cart.service';
import { Subscription, interval } from 'rxjs';

@Component({
  selector: 'app-payment-success',
  templateUrl: './payment-success.component.html',
  styleUrls: ['./payment-success.component.scss']
})
export class PaymentSuccessComponent implements OnInit, OnDestroy {  
  transactionId: string = '';
  transactionStatus: string = 'pending'; // Statut initial toujours "pending"
  transactionAmount: string = '';
  transactionGateway: string = '';
  loading: boolean = true;
  validationMessage: string = '';
  validationSuccess: boolean = false;
  qrCodeValue: string = '';
  
  // 🔄 Polling pour rafraîchir le status automatiquement
  private pollingSubscription: Subscription | null = null;
   
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
        this.startPolling();  // 🔄 Démarrer le polling
      } else {
        this.loading = false;
      }
    });
  }

  ngOnDestroy(): void {
    // Arrêter le polling quand on quitte la page
    this.stopPolling();
  }

  // 🔄 Démarrer le polling (vérifier le status toutes les 5 secondes)
  startPolling(): void {
    this.pollingSubscription = interval(5000).subscribe(() => {
      if (this.transactionStatus !== 'success' && this.transactionStatus !== 'completed') {
        this.checkTransactionStatus();
      } else {
        this.stopPolling();  // Arrêter quand la transaction est validée
      }
    });
    console.log('🔄 Polling démarré - vérification du status toutes les 5 secondes');
  }

  // 🔄 Arrêter le polling
  stopPolling(): void {
    if (this.pollingSubscription) {
      this.pollingSubscription.unsubscribe();
      this.pollingSubscription = null;
      console.log('⏹️ Polling arrêté');
    }
  }

  // 🔄 Vérifier le status de la transaction
  checkTransactionStatus(): void {
    this.transactionService.getTransaction(this.transactionId).subscribe({
      next: (transaction: any) => {
        console.log('🔄 Status vérifié:', transaction.status);
        
        if (transaction.status === 'success' || transaction.status === 'completed') {
          // 🎉 La transaction a été validée par le livreur !
          this.transactionStatus = 'success';
          this.validationSuccess = true;
          this.validationMessage = '🎉 Félicitations ! Votre commande a été livrée avec succès !';
          this.stopPolling();
          
          // Vider le panier
          this.cartService.clearCart();
          
          console.log('✅ Transaction validée ! Status:', transaction.status);
        }
      },
      error: (error: any) => {
        console.error('❌ Erreur vérification status:', error);
        // Ne pas stopper le polling en cas d'erreur (réessayer)
      }
    });
  }

  // Récupérer les données de la transaction depuis le backend (avec signature)
  loadTransactionData(): void {
    this.transactionService.getTransaction(this.transactionId).subscribe({
      next: (transaction: any) => {
        console.log('📦 Transaction récupérée:', transaction);
        
        // Vérifier si déjà validée
        if (transaction.status === 'success' || transaction.status === 'completed') {
          this.transactionStatus = 'success';
          this.validationSuccess = true;
          this.validationMessage = '🎉 Votre commande a déjà été livrée !';
          this.loading = false;
          this.stopPolling();
          return;
        }
        
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
        this.stopPolling();

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