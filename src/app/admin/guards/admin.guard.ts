import { Injectable, Inject, PLATFORM_ID } from '@angular/core';
import { CanActivate, Router, ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';
import { Observable } from 'rxjs';
import { isPlatformBrowser } from '@angular/common';

@Injectable({
  providedIn: 'root'
})
export class AdminGuard implements CanActivate {
  
  constructor(
    private router: Router,
    @Inject(PLATFORM_ID) private platformId: Object
  ) {}

  canActivate(
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot
  ): Observable<boolean> | boolean {
    // Vérifier si on est côté navigateur (pas SSR)
    if (!isPlatformBrowser(this.platformId)) {
      return false;
    }

    // Vérifier si l'utilisateur est connecté et est admin
    const token = localStorage.getItem('access_token');
    const userStr = localStorage.getItem('user');
    
    if (!token || !userStr) {
      this.router.navigate(['/login'], { queryParams: { returnUrl: state.url } });
      return false;
    }

    try {
      const user = JSON.parse(userStr);
      
      if (user.role !== 'admin') {
        // Rediriger vers la page d'accueil si l'utilisateur n'est pas admin
        this.router.navigate(['/']);
        return false;
      }
      
      return true;
    } catch (e) {
      this.router.navigate(['/login']);
      return false;
    }
  }
}
