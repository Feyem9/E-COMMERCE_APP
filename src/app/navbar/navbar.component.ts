import { Component } from '@angular/core';
import { CartService } from '../services/cart.service';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.scss'
})
export class NavbarComponent {

  cartCount = 0;

constructor(private cartService: CartService) {}

ngOnInit() {
  this.cartService.cartCount$.subscribe(count => {
    this.cartCount = count;
  });
}

}
