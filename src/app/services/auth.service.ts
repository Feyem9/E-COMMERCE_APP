import { Injectable, Inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { BehaviorSubject, Observable } from 'rxjs';
import { ApiService } from './api.service';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private isLoggedInSubject = new BehaviorSubject<boolean>(false);
  public isLoggedIn$ = this.isLoggedInSubject.asObservable();

  private userSubject = new BehaviorSubject<any>(null);
  public user$ = this.userSubject.asObservable();

  constructor(
    @Inject(PLATFORM_ID) private platformId: Object
  ) {
    this.checkAuthStatus();
  }

  /**
   * Vérifie le statut d'authentification au démarrage
   */
  private checkAuthStatus(): void {
    if (isPlatformBrowser(this.platformId)) {
      const token = localStorage.getItem('access_token');
      const user = localStorage.getItem('user');
      
      if (token && user) {
        this.isLoggedInSubject.next(true);
        this.userSubject.next(JSON.parse(user));
      }
    }
  }

  /**
   * Connexion temporaire pour les tests
   */
  loginTemp(email: string = 'test@example.com', password: string = 'password'): void {
    if (isPlatformBrowser(this.platformId)) {
      // Simule un token d'authentification
      const fakeToken = 'fake-jwt-token-for-testing';
      const fakeUser = {
        id: 1,
        email: email,
        name: 'Test User'
      };

      localStorage.setItem('access_token', fakeToken);
      localStorage.setItem('user', JSON.stringify(fakeUser));
      
      this.isLoggedInSubject.next(true);
      this.userSubject.next(fakeUser);
      
      console.log('Connexion temporaire activée');
    }
  }

  /**
   * Déconnexion
   */
  logout(): void {
    if (isPlatformBrowser(this.platformId)) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
    }
    
    this.isLoggedInSubject.next(false);
    this.userSubject.next(null);
  }

  /**
   * Vérifie si l'utilisateur est connecté
   */
  isAuthenticated(): boolean {
    return this.isLoggedInSubject.value;
  }

  /**
   * Obtient le token d'accès
   */
  getToken(): string | null {
    if (isPlatformBrowser(this.platformId)) {
      return localStorage.getItem('access_token');
    }
    return null;
  }

  /**
   * Obtient les informations de l'utilisateur
   */
  getUser(): any {
    return this.userSubject.value;
  }
}