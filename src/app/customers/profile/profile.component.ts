import { Component, OnInit, OnDestroy } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { User } from '../../models/user.model';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';
import { environment } from '../../../environment/environment';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss']
})
export class ProfileComponent implements OnInit, OnDestroy {
  user: User = {
    id: 0,
    email: '',
    name: '',
    password: '',
    contact: '',
    address: '',
    role: ''
  };
  private destroy$ = new Subject<void>();
  // private readonly apiBase = 'https://e-commerce-app-0hnw.onrender.com';
  private readonly apiBase = environment.apiUrl;

  constructor(private http: HttpClient) { }

  ngOnInit(): void {
    this.getUserProfile();
  }

  // getUserProfile(): void {
  //   const token = localStorage.getItem('token'); // ou depuis AuthService si tu en as un

  //   this.http.get<any>('http://localhost:5000/customer/profile', {
  //     headers: {
  //       Authorization: `Bearer ${token}`
  //     }
  //   }).subscribe({
  //     next: (data) => {
  //       this.user = data;
  //       console.log('✅ Profil reçu :', data);
  //     },
  //     error: (error) => {
  //       console.error('❌ Erreur lors du chargement du profil :', error);
  //     }
  //   });
  // }

  getUserProfile(): void {
    const token = localStorage.getItem('access_token'); // Assure-toi que c’est bien 'access_token'

    if (!token) {
      console.error('❌ Aucun token trouvé dans le localStorage.');
      return;
    }

    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    });

    this.http.get<any>(`${this.apiBase}/customer/profile`, { headers })
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (data) => {
          this.user = data;
          console.log('✅ Profil reçu :', data);
        },
        error: (error) => {
          console.error('❌ Erreur lors du chargement du profil :', error);
        }
      });
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

}
