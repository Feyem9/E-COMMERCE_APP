import { ComponentFixture, TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { NavbarComponent } from './navbar.component';
import { CartService } from '../services/cart.service';
import { AuthService } from '../customers/auth.service';
import { of, Subject } from 'rxjs';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

describe('NavbarComponent', () => {
  let component: NavbarComponent;
  let fixture: ComponentFixture<NavbarComponent>;
  let cartServiceMock: any;
  let authServiceMock: any;

  beforeEach(async () => {
    // Mock CartService
    cartServiceMock = {
      cartCount$: of(0),
      getCartItems: () => of([]),
      clearCart: () => of({})
    };

    // Mock AuthService
    authServiceMock = {
      isLoggedIn$: of(false),
      user$: of(null),
      isLoggedIn: () => false,
      logout: () => of({}),
      login: () => of({})
    };

    await TestBed.configureTestingModule({
      imports: [
        RouterTestingModule,
        BrowserAnimationsModule
      ],
      declarations: [NavbarComponent],
      providers: [
        { provide: CartService, useValue: cartServiceMock },
        { provide: AuthService, useValue: authServiceMock }
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(NavbarComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should initialize with default values', () => {
    expect(component.cartCount).toBe(0);
    expect(component.favoriteCount).toBe(0);
    expect(component.isLoggedIn).toBe(false);
    expect(component.userName).toBe('');
    expect(component.searchQuery).toBe('');
    expect(component.showSearch).toBe(false);
  });

  it('should toggle search visibility', () => {
    component.toggleSearch();
    expect(component.showSearch).toBe(true);
    component.toggleSearch();
    expect(component.showSearch).toBe(false);
  });

  it('should navigate on search', () => {
    const routerSpy = spyOn(component['router'], 'navigate');
    component.searchQuery = 'test';
    component.onSearch();
    expect(routerSpy).toHaveBeenCalledWith(['/product'], { queryParams: { search: 'test' } });
    expect(component.searchQuery).toBe('');
    expect(component.showSearch).toBe(false);
  });

  it('should not navigate if search query is empty', () => {
    const routerSpy = spyOn(component['router'], 'navigate');
    component.searchQuery = '   ';
    component.onSearch();
    expect(routerSpy).not.toHaveBeenCalled();
  });

  it('should call logout and clear cart', () => {
    const logoutSpy = spyOn(authServiceMock, 'logout').and.returnValue(of({}));
    const clearCartSpy = spyOn(cartServiceMock, 'clearCart').and.returnValue(of({}));
    spyOn(window, 'alert');

    component.logout();

    expect(logoutSpy).toHaveBeenCalled();
    expect(clearCartSpy).toHaveBeenCalled();
    expect(window.alert).toHaveBeenCalledWith('You have been logged out successfully');
  });

  it('should handle logout error', () => {
    const logoutSpy = spyOn(authServiceMock, 'logout').and.returnValue(of({ error: 'error' }));
    const clearCartSpy = spyOn(cartServiceMock, 'clearCart').and.returnValue(of({}));
    spyOn(window, 'alert');

    component.logout();

    expect(logoutSpy).toHaveBeenCalled();
    expect(clearCartSpy).toHaveBeenCalled();
    expect(window.alert).toHaveBeenCalledWith('You have been logged out successfully');
  });

  it('should call loginTemp', () => {
    const loginSpy = spyOn(authServiceMock, 'login').and.returnValue(of({}));
    spyOn(window, 'alert');

    component.loginTemp();

    expect(loginSpy).toHaveBeenCalledWith({
      email: 'test@example.com',
      password: 'password'
    });
    expect(window.alert).toHaveBeenCalledWith('Connexion temporaire activée - Vous pouvez maintenant ajouter des produits au panier');
  });

  it('should handle loginTemp error', () => {
    const loginSpy = spyOn(authServiceMock, 'login').and.returnValue(of({ error: 'error' }));
    spyOn(localStorage, 'setItem');
    spyOn(window, 'alert');

    component.loginTemp();

    expect(loginSpy).toHaveBeenCalled();
    expect(localStorage.setItem).toHaveBeenCalled();
    expect(window.alert).toHaveBeenCalledWith('Token temporaire créé pour les tests');
  });

  it('should close navbar if it is open', () => {
    const navbarToggler = document.createElement('button');
    navbarToggler.className = 'navbar-toggler';
    const navbarCollapse = document.createElement('div');
    navbarCollapse.className = 'navbar-collapse show';

    spyOn(document, 'querySelector').and.callFake((selector: string) => {
      if (selector === '.navbar-toggler') return navbarToggler;
      if (selector === '.navbar-collapse') return navbarCollapse;
      return null;
    });

    spyOn(navbarToggler, 'click');

    component.closeNavbar();

    expect(document.querySelector).toHaveBeenCalledWith('.navbar-toggler');
    expect(document.querySelector).toHaveBeenCalledWith('.navbar-collapse');
    expect(navbarToggler.click).toHaveBeenCalled();
  });

  it('should not close navbar if it is not open', () => {
    const navbarToggler = document.createElement('button');
    navbarToggler.className = 'navbar-toggler';
    const navbarCollapse = document.createElement('div');
    navbarCollapse.className = 'navbar-collapse';

    spyOn(document, 'querySelector').and.callFake((selector: string) => {
      if (selector === '.navbar-toggler') return navbarToggler;
      if (selector === '.navbar-collapse') return navbarCollapse;
      return null;
    });

    spyOn(navbarToggler, 'click');

    component.closeNavbar();

    expect(document.querySelector).toHaveBeenCalledWith('.navbar-toggler');
    expect(document.querySelector).toHaveBeenCalledWith('.navbar-collapse');
    expect(navbarToggler.click).not.toHaveBeenCalled();
  });
});
