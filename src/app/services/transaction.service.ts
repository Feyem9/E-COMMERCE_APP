import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '../../environment/environment';

@Injectable({
  providedIn: 'root'
})
export class TransactionService {
  //  private apiUrl = 'https://e-commerce-app-1-islr.onrender.com/transaction/payment'; // Production URL
  // private API_URL = 'https://e-commerce-app-0hnw.onrender.com/transaction'; // Base URL for transaction-related endpoints
  private API_URL = `${environment.apiUrl}/transaction`; // Base URL for transaction-related endpoints

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

  validateTransaction(qrCodeValue: string) {
    return this.http.post<any>(`${this.API_URL}/validate`, { qr_code: qrCodeValue });
  }

  getUserTransactions(userId: number) {
    return this.http.get<any>(`${this.API_URL}/user/${userId}`);
  }
}
