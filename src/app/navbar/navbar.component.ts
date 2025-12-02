import { Component, OnInit, OnDestroy } from '@angular/core';
import { Router } from '@angular/router';
import { trigger, state, style, transition, animate } from '@angular/animations';
import { CartService } from '../services/cart.service';
import { AuthService } from '../customers/auth.service';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.scss',
  animations: [
    trigger('slideDown', [
      transition(':enter', [
        style({ transform: 'translateY(-100%)', opacity: 0 }),
        animate('300ms ease-in-out', style({ transform: 'translateY(0%)', opacity: 1 }))
      ]),
      transition(':leave', [
        animate('300ms ease-in-out', style({ transform: 'translateY(-100%)', opacity: 0 }))
      ])
    ])
  ]
})
export class NavbarComponent implements OnInit, OnDestroy {

  cartCount = 0;
  favoriteCount = 0;
  isLoggedIn = false;
  userName = '';
  searchQuery = '';
  showSearch = false;
  private destroy$ = new Subject<void>();

  constructor(
    private cartService: CartService,
    private router: Router,
    private authService: AuthService
  ) {}

  ngOnInit(): void {
    // Subscribe to cart count changes
    this.cartService.cartCount$
      .pipe(takeUntil(this.destroy$))
      .subscribe((count: number) => {
        this.cartCount = count;
      });

    // Subscribe to auth changes
    this.authService.isLoggedIn$
      .pipe(takeUntil(this.destroy$))
      .subscribe((isLoggedIn: boolean) => {
        this.isLoggedIn = isLoggedIn;
      });

    this.authService.user$
      .pipe(takeUntil(this.destroy$))
      .subscribe((user: any) => {
        this.userName = user ? user.name : '';
      });

    // Check if user is logged in
    this.checkLoginStatus();

    // Load initial cart items count if user is authenticated
    if (this.authService.isLoggedIn()) {
      this.cartService.getCartItems()
        .pipe(takeUntil(this.destroy$))
        .subscribe();
    }
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  checkLoginStatus(): void {
    const token = typeof localStorage !== 'undefined' ? localStorage.getItem('access_token') : null;
    const user = typeof localStorage !== 'undefined' ? localStorage.getItem('user') : null;
    
    this.isLoggedIn = !!token;
    if (user) {
      try {
        const userData = JSON.parse(user);
        this.userName = userData.name || userData.email || 'User';
      } catch (e) {
        this.userName = 'User';
      }
    }
  }

  toggleSearch(): void {
    this.showSearch = !this.showSearch;
  }

  onSearch(): void {
    if (this.searchQuery.trim()) {
      this.router.navigate(['/product'], { 
        queryParams: { search: this.searchQuery.trim() } 
      });
      this.searchQuery = '';
      this.showSearch = false;
    }
  }

  logout(): void {
    this.authService.logout().subscribe({
      next: () => {
        this.cartService.clearCart().subscribe();
        alert('You have been logged out successfully');
      },
      error: (error: any) => {
        console.error('Error during logout:', error);
        // Même en cas d'erreur, on déconnecte localement
        this.cartService.clearCart().subscribe();
        alert('You have been logged out successfully');
      }
    });
  }

  // Connexion temporaire pour les tests
  loginTemp(): void {
    // Utilise les credentials de test pour la démo
    const testCredentials = {
      email: 'test@example.com',
      password: 'password'
    };
    
    this.authService.login(testCredentials).subscribe({
      next: (response) => {
        alert('Connexion temporaire activée - Vous pouvez maintenant ajouter des produits au panier');
      },
      error: (error) => {
        console.error('Erreur de connexion temporaire:', error);
        // En cas d'erreur, on crée un token temporaire en localStorage
        if (typeof localStorage !== 'undefined') {
          localStorage.setItem('access_token', 'fake-token-for-testing');
          localStorage.setItem('user_data', JSON.stringify({
            id: 1,
            email: 'test@example.com',
            name: 'Test User'
          }));
          alert('Token temporaire créé pour les tests');
          window.location.reload();
        }
      }
    });
  }

  // Handle responsive navbar collapse
  closeNavbar(): void {
    const navbarToggler = document.querySelector('.navbar-toggler') as HTMLElement;
    const navbarCollapse = document.querySelector('.navbar-collapse') as HTMLElement;
    
    if (navbarCollapse && navbarCollapse.classList.contains('show')) {
      navbarToggler?.click();
    }
  }
}
