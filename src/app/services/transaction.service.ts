import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class TransactionService {
 private apiUrl = 'http://localhost:5000/transaction/payment'; // Change selon ton URL

  constructor(private http: HttpClient) {}

  initiatePayment(paymentData: any) {
    return this.http.post<any>(this.apiUrl, paymentData);
  }
}
