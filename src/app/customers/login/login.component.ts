import { Component } from '@angular/core';
import { Login } from '../../models/user.model'
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../auth.service';


@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrl: './login.component.scss'
})
export class LoginComponent {

  loginForm!: FormGroup;
  errorMsg: string = '';
  isSubmitting: boolean = false;
  showPassword: boolean = false;

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router
  ) { }

  ngOnInit(): void {
    this.initForm();
  }

  private initForm(): void {
    this.loginForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]],
    });
  }

  // onSubmit(): void {
  //   if (this.loginForm.invalid) {
  //     this.errorMsg = 'Please fill in all required fields correctly.';
  //     return;
  //   }

  //   this.isSubmitting = true;
  //   const payload: Login = this.loginForm.value;

  //   this.authService.login(payload).subscribe({
  //     next: () => {
  //       this.isSubmitting = false;
  //       // Redirect to login page on success
  //       this.router.navigate(['/profile']);
  //     },
  //     error: (err: { error: { message: string; }; }) => {
  //       this.isSubmitting = false;
  //       // Display server error message if available
  //       this.errorMsg = err.error?.message || 'Login failed. Please check your credentials.';
  //     }
  //   });
  //   // Exemple fetch
  // fetch('http://localhost:5000/customer/profile', {
  //   method: 'GET',
  //   credentials: 'include'
  // });

  // }

  onSubmit(): void {
    if (this.loginForm.invalid) {
      this.errorMsg = 'Please fill in all required fields correctly.';
      return;
    }

    this.isSubmitting = true;
    const payload: Login = this.loginForm.value;

    this.authService.login(payload).subscribe({
      next: (res) => {
        console.log('🎉 Connexion réussie', res);
        localStorage.setItem('access_token', res.access_token);
        localStorage.setItem('identity', res.user.id.toString());
        localStorage.setItem('email', res.user.email);
        localStorage.setItem('name', res.user.name);
        localStorage.setItem('role', res.user.role);
        this.authService.profile().subscribe({
          next: (profileData) => {
            this.isSubmitting = false;
            console.log('Profile:', profileData);
            this.router.navigate(['/profile']);
          },
          error: (err: any) => {
            this.isSubmitting = false;
            this.errorMsg = 'Could not fetch profile after login.';
          }
        });
      },
      error: (err: { error: { message: string } }) => {
        this.isSubmitting = false;
        this.errorMsg = err.error?.message || 'Login failed. Please check your credentials.';
      }
    });
  }


  // Helper getters for easy access in template
  get email() { return this.loginForm.get('email'); }
  get password() { return this.loginForm.get('password'); }

  togglePassword(): void {
    this.showPassword = !this.showPassword;
  }
}
