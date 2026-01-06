// src/app/services/auth.service.ts
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';  // pour les requêtes HTTP :contentReference[oaicite:0]{index=0}
import { BehaviorSubject, Observable, tap } from 'rxjs';
import { Register, Login } from '../models/user.model'
import { environment } from '../../environment/environment';


export interface AuthResponse {
  access_token: string;
  user: {
    id: number;
    email: string;
    name: string;
    role: string;
  };
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  // Déclaration explicite de la base URL (production)
  private readonly apiBase = environment.apiUrl;

  // Subject pour suivre l'état de l'authentification
  private authSub = new BehaviorSubject<AuthResponse | null>(null);
  public authState$ = this.authSub.asObservable();

  // Observables pour le login status et user
  private loggedInSub = new BehaviorSubject<boolean>(false);
  public isLoggedIn$ = this.loggedInSub.asObservable();

  private userSub = new BehaviorSubject<any>(null);
  public user$ = this.userSub.asObservable();

  constructor(private http: HttpClient) {
    this.checkInitialAuthState();
  }

  /** Vérifier l'état initial de l'authentification */
  private checkInitialAuthState(): void {
    const token = typeof localStorage !== 'undefined' ? localStorage.getItem('access_token') : null;
    if (token) {
      this.loggedInSub.next(true);
      const user = typeof localStorage !== 'undefined' ? localStorage.getItem('user') : null;
      if (user) {
        try {
          this.userSub.next(JSON.parse(user));
        } catch (e) {
          this.userSub.next(null);
        }
      }
    }
  }

  /** Vérifier si l'utilisateur est authentifié */
  isAuthenticated(): boolean {
    if (typeof localStorage === 'undefined') return false;
    return !!localStorage.getItem('access_token');
  }

  /** Obtenir l'utilisateur actuel */
  getCurrentUser(): any {
    if (typeof localStorage === 'undefined') return null;
    const user = localStorage.getItem('user');
    try {
      return user ? JSON.parse(user) : null;
    } catch {
      return null;
    }
  }

  /** Inscription */
  register(payload: Register): Observable<any> {
    const url = `${this.apiBase}/customer/register`;
    return this.http.post<any>(url, payload, {
      headers: new HttpHeaders({ 'Content-Type': 'application/json' }),
      withCredentials: true  // Assurez-vous d'inclure les informations d'authentification
    });
  }

  /** Connexion */
  login(payload: Login): Observable<AuthResponse> {
    const url = `${this.apiBase}/customer/login`;
    return this.http
      .post<AuthResponse>(url, payload, {
        headers: new HttpHeaders({ 'Content-Type': 'application/json' })
      })
      .pipe(
        tap(res => {
          if (typeof localStorage !== 'undefined') {
            localStorage.setItem('access_token', res.access_token);
            localStorage.setItem('user', JSON.stringify(res.user));
          }
          this.authSub.next(res);
          this.loggedInSub.next(true);
          this.userSub.next(res.user);
        })
      );
  }

  /** Déconnexion */
  logout(): Observable<void> {
    const url = `${this.apiBase}/customer/logout`;
    const token = this.getToken();
    
    return new Observable(observer => {
      if (typeof localStorage !== 'undefined') {
        localStorage.removeItem('access_token');
        localStorage.removeItem('user');
      }
      this.authSub.next(null);
      this.loggedInSub.next(false);
      this.userSub.next(null);
      observer.next();
      observer.complete();
    });
  }

  /** Récupérer le token stocké */
  getToken(): string | null {
    if (typeof localStorage === 'undefined') {
      return null; // SSR environment
    }
    return localStorage.getItem('access_token');
  }

  /** Vérifier si l'utilisateur est connecté */
  isLoggedIn(): boolean {
    return !!this.getToken();
  }

  profile(): Observable<any> {
    const url = `${this.apiBase}/customer/profile`;
    const token = this.getToken();


    return this.http.get<any>(url, {
      headers
        : new HttpHeaders({ 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` }),
      withCredentials: false  // Assurez-vous d'inclure les informations d'authentification
    });
  } 

  getUserId(): number | null {
    if (typeof localStorage === 'undefined') {
      return null; // SSR environment
    }
    
    // Try to get from user object first
    const user = this.userSub.value;
    if (user?.id) {
      return user.id;
    }
    
    // Fallback to stored identity
    const id = localStorage.getItem('identity');
    return id ? parseInt(id, 10) : null;
  }
}
