import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import axios from 'axios';

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

  async initiatePayment(data: any) {
    const response = await axios.post(`${this.API_URL}/payment`, data);
    return response.data;
  }

  async confirmTransaction(transactionId: string, token: string) {
    const response = await axios.post(`${this.API_URL}/confirm/${transactionId}`, { token });
    return response.data;
  }

  async getUserTransactions(userId: number) {
    const response = await axios.get(`${this.API_URL}/user/${userId}`);
    return response.data;
  }
}
