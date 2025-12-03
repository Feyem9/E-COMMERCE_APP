import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../auth.service';
import { Register } from '../../models/user.model'

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss']
})
export class RegisterComponent implements OnInit {
  registerForm!: FormGroup;
  errorMsg: string = '';
  isSubmitting: boolean = false;
 
  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.initForm();
  }

  private initForm(): void {
    this.registerForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      name: ['', [Validators.required, Validators.minLength(2)]],
      password: ['', [Validators.required, Validators.minLength(6)]],
      contact: ['', [Validators.required]],
      address: ['', [Validators.required]],
      role: ['customer', [Validators.required]]
    });
  }

  onSubmit(): void {
    if (this.registerForm.invalid) {
      this.errorMsg = 'Please fill in all required fields correctly.';
      return;
    }

    this.isSubmitting = true;
    const payload: Register = this.registerForm.value;

    this.authService.register(payload).subscribe({
      next: () => {
        this.isSubmitting = false;
        // Redirect to login page on success
        this.router.navigate(['/login']);
      },
      error: (err: any) => {
       this.isSubmitting = false;
       // Display server error message with more details
       if (err.error?.error) {
         this.errorMsg = err.error.error;
         if (err.error.details) {
           this.errorMsg += `: ${err.error.details}`;
         }
         if (err.error.missing_fields) {
           this.errorMsg += `. Missing: ${err.error.missing_fields.join(', ')}`;
         }
       } else if (err.error?.message) {
         this.errorMsg = err.error.message;
       } else if (err.message) {
         this.errorMsg = err.message;
       } else {
         this.errorMsg = 'Registration failed. Please try again.';
       }
       console.error('Registration error:', err);
     }
    });
  }

  // Helper getters for easy access in template
  get email() { return this.registerForm.get('email'); }
  get name() { return this.registerForm.get('name'); }
  get password() { return this.registerForm.get('password'); }
  get contact() { return this.registerForm.get('contact'); }
  get address() { return this.registerForm.get('address'); }
  get role() { return this.registerForm.get('role'); }
}
