import { Injectable } from '@angular/core';
import { HttpInterceptor, HttpRequest, HttpHandler, HttpEvent, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { Router } from '@angular/router';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  
  constructor(private router: Router) {}

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    // Récupérer le token du localStorage
    const token = localStorage.getItem('access_token');

    // Si un token existe, l'ajouter aux headers
    if (token) {
      req = req.clone({
        setHeaders: {
          Authorization: `Bearer ${token}`
        }
      });
    }

    return next.handle(req).pipe(
      catchError((error: HttpErrorResponse) => {
        // Si erreur 401 ou 403, rediriger vers login
        if (error.status === 401) {
          localStorage.removeItem('access_token');
          localStorage.removeItem('user');
          this.router.navigate(['/login']);
        }
        
        if (error.status === 403) {
          // Accès refusé - rediriger vers l'accueil
          this.router.navigate(['/']);
        }

        return throwError(() => error);
      })
    );
  }
}
