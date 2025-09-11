import { Component } from '@angular/core';
import { TransactionService } from '../services/transaction.service';

@Component({
  selector: 'app-transaction-history',
  templateUrl: './transaction-history.component.html',
  styleUrl: './transaction-history.component.scss'
})
export class TransactionHistoryComponent {
  transactions: any[] = [];

  constructor(private transactionService: TransactionService) { }

  async ngOnInit() {
    const userId = 1; // récupéré depuis ton auth service
    this.transactions = await this.transactionService.getUserTransactions(userId);
  }
}
