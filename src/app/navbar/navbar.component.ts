import { Component , ViewChild} from '@angular/core';
import { CartService } from '../services/cart.service';
import { MatSidenav } from '@angular/material/sidenav';


@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.scss'
})
export class NavbarComponent {

  cartCount = 0;

   @ViewChild('sidenav') sidenav!: MatSidenav;

constructor(private cartService: CartService) {}

ngOnInit() {
  this.cartService.cartCount$.subscribe(count => {
    this.cartCount = count;
  });
}

}
