import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { User } from '../../models/user.model';


@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss']
})
export class ProfileComponent implements OnInit {
  user: User = {
     id:0,
    email:'',
    name:'',
    password:'',
    contact:'',
    address:'',
    role:''
  };

  constructor(private http: HttpClient) {}

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

  this.http.get<any>('http://localhost:5000/customer/profile', { headers })
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

}
