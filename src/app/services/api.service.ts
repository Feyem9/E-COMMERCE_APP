import { Injectable, Inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { HttpClient, HttpHeaders, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, retry } from 'rxjs/operators';
import { AuthService } from '../customers/auth.service';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private readonly baseUrl = 'https://e-commerce-app-1-islr.onrender.com';
  
  private httpOptions = {
    headers: new HttpHeaders({
      'Content-Type': 'application/json'
    })
  };

  constructor(
    private http: HttpClient,
    private authService: AuthService,
    @Inject(PLATFORM_ID) private platformId: Object
  ) { }

  /**
   * Get method
   */
  get<T>(endpoint: string): Observable<T> { 
    const headers = this.getAuthHeaders();
    const options = { headers };
    
    return this.http.get<T>(`${this.baseUrl}${endpoint}`, options)
      .pipe(
        retry(1),
        catchError(this.handleError)
      );
  }

  /**
   * Post method
   */
  post<T>(endpoint: string, data: any, options = {}): Observable<T> {
    const authHeaders = this.getAuthHeaders();
    const mergedOptions = { 
      headers: authHeaders,
      ...options 
    };
    return this.http.post<T>(`${this.baseUrl}${endpoint}`, data, mergedOptions)
      .pipe(
        retry(1),
        catchError(this.handleError)
      );
  }

  /**
   * Put method
   */
  put<T>(endpoint: string, data: any, options = {}): Observable<T> {
    const authHeaders = this.getAuthHeaders();
    const mergedOptions = { 
      headers: authHeaders,
      ...options 
    };
    return this.http.put<T>(`${this.baseUrl}${endpoint}`, data, mergedOptions)
      .pipe(
        retry(1),
        catchError(this.handleError)
      );
  }

  /**
   * Delete method
   */
  delete<T>(endpoint: string, options = {}): Observable<T> {
    const authHeaders = this.getAuthHeaders();
    const mergedOptions = { 
      headers: authHeaders,
      ...options 
    };
    return this.http.delete<T>(`${this.baseUrl}${endpoint}`, mergedOptions)
      .pipe(
        retry(1),
        catchError(this.handleError)
      );
  }

  /**
   * Get auth headers
   */
  getAuthHeaders(): HttpHeaders {
    const token = this.authService.getToken();
    if (token) {
      return new HttpHeaders({
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      });
    }
    return this.httpOptions.headers;
  }

  /**
   * Handle API errors
   */
  private handleError = (error: HttpErrorResponse) => {
    let errorMessage = 'Une erreur inconnue s\'est produite';
    
    // Check if we're in browser environment before using ErrorEvent
    if (isPlatformBrowser(this.platformId) && error.error instanceof ErrorEvent) {
      // Client-side error (only in browser)
      errorMessage = error.error.message;
    } else {
      // Server-side error or SSR environment
      switch (error.status) {
        case 400:
          errorMessage = 'Requête invalide';
          break;
        case 401:
          errorMessage = 'Non autorisé - Veuillez vous connecter';
          break;
        case 403:
          errorMessage = 'Accès refusé';
          break;
        case 404:
          errorMessage = 'Ressource non trouvée';
          break;
        case 500:
          errorMessage = 'Erreur serveur interne';
          break;
        default:
          errorMessage = `Erreur serveur: ${error.status}`;
      }
    }

    console.error('API Error:', error);
    return throwError(() => new Error(errorMessage));
  }

  /**
   * Check if user is authenticated
   */
  isAuthenticated(): boolean {
    return this.authService.isAuthenticated();
  }
}