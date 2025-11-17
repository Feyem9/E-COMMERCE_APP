import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class TransactionService {
  //  private apiUrl = 'http://localhost:5000/transaction/payment'; // Change selon ton URL
  private API_URL = 'http://localhost:5000/transaction'; // Base URL for transaction-related endpoints

  constructor(private http: HttpClient) { }

  // initiatePayment(paymentData: any) {
  //   return this.http.post<any>(this.apiUrl, paymentData);
  // }

  initiatePayment(data: any) {
    return this.http.post<any>(`${this.API_URL}/payment`, data);
  }

  confirmTransaction(transactionId: string, token: string) {
    return this.http.post<any>(`${this.API_URL}/confirm/${transactionId}`, { token });
  }

  getUserTransactions(userId: number) {
    return this.http.get<any>(`${this.API_URL}/user/${userId}`);
  }
}
