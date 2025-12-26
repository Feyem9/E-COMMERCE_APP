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

      // Si nous avons un ID de transaction, générer un QR code pour validation
      if (this.transactionId) {
        // 🔐 Créer le JSON complet pour le QR code (pas juste le transaction_id)
        const qrData = {
          transaction_id: this.transactionId,
          reference: `CMD-${new Date().toISOString().split('T')[0].replace(/-/g, '')}-${this.transactionId.slice(-6)}`,
          amount: parseFloat(this.transactionAmount) || 0,
          currency: 'XAF',
          status: 'pending',
          timestamp: new Date().toISOString()
        };
        this.qrCodeValue = JSON.stringify(qrData);
        console.log('📱 QR Code généré (JSON complet):', this.qrCodeValue);
        
        this.validationMessage = 'Veuillez scanner ce QR code pour valider votre transaction.';
        
        // ❌ SUPPRIMÉ : Plus de validation automatique !
        // La validation se fait UNIQUEMENT quand le livreur scanne le QR code
        // via l'interface livreur.html
      }

      this.loading = false;
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