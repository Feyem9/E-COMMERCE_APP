import { Component } from '@angular/core';
import { CartService } from '../services/cart.service';

@Component({
  selector: 'app-payment-success',
  templateUrl: './payment-success.component.html',
  styleUrl: './payment-success.component.scss'
})
export class PaymentSuccessComponent {

constructor(private cartService: CartService) {}
  ngOnInit(): void {
  this.cartService.clearCart();
}
}
