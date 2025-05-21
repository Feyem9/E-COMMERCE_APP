// src/app/services/auth.service.ts
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';  // pour les requêtes HTTP :contentReference[oaicite:0]{index=0}
import { BehaviorSubject, Observable, tap } from 'rxjs';
import { Register, Login } from '../models/user.model'


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
  // Déclaration explicite de la base URL (pas d'environment) :contentReference[oaicite:1]{index=1}
  private readonly apiBase = 'http://127.0.0.1:5000';

  // Subject pour suivre l’état de l’authentification
  private authSub = new BehaviorSubject<AuthResponse | null>(null);
  public authState$ = this.authSub.asObservable();

  constructor(private http: HttpClient) { }

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
          console.log('✅ Réponse login reçue :', res);
          localStorage.setItem('access_token', res.access_token);
          this.authSub.next(res);
        })
      );
  }

  /** Déconnexion */
  logout(): void {
    localStorage.removeItem('access_token');
    this.authSub.next(null);
  }

  /** Récupérer le token stocké */
  getToken(): string | null {
    return localStorage.getItem('access_token');
  }

  /** Vérifier si l’utilisateur est connecté */
  isLoggedIn(): boolean {
    return !!this.getToken();
  }

  profile(): Observable<any> {
    const url = `${this.apiBase}/customer/profile`;
    const token = this.getToken();


    return this.http.get<any>(url, {
      headers
        : new HttpHeaders({ 'Content-Type': 'application/json' , 'Authorization': `Bearer ${token}`}),
      withCredentials: false  // Assurez-vous d'inclure les informations d'authentification
    });
  }

  getUserId(): number | null {
  const data = this.authSub.getValue();
  return data?.user?.id || null;
}
}
