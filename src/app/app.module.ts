import { NgModule } from '@angular/core';
import { BrowserModule, provideClientHydration } from '@angular/platform-browser';
import { HttpClientModule, provideHttpClient, withFetch } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { NavbarComponent } from './navbar/navbar.component';

import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatMenuModule } from '@angular/material/menu';
import { MatSnackBarModule } from '@angular/material/snack-bar'; 
import { MatDivider } from "@angular/material/divider";
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatListModule } from '@angular/material/list';
import { MatCardModule } from '@angular/material/card'; 
import { ProductComponent } from './product/product.component';
import { CategoriesComponent } from './categories/categories.component';
import { TransactionComponent } from './transaction/transaction.component';
import { OrderedComponent } from './ordered/ordered.component';
import { FavoriteComponent } from './favorite/favorite.component';
import { CartComponent } from './cart/cart.component';
import { LoginComponent } from './customers/login/login.component';
import { RegisterComponent } from './customers/register/register.component';
import { HomeComponent } from './home/home.component';
import { ReactiveFormsModule } from '@angular/forms';
import { FormsModule } from '@angular/forms';
import { ProfileComponent } from './customers/profile/profile.component';
import { PaymentSuccessComponent } from './payment/payment-success/payment-success.component';
import { PaymentComponent } from './payment/payment.component';
import { TransactionHistoryComponent } from './transaction-history/transaction-history.component';  // Ajoutez cette ligne pour le ngModel

@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent,
    ProductComponent,
    TransactionComponent,
    CartComponent,
    LoginComponent,
    RegisterComponent,
    HomeComponent,
    ProfileComponent,
    PaymentSuccessComponent,
    PaymentComponent,
    TransactionHistoryComponent
  ],
  imports: [
    BrowserModule,
    CommonModule,
    RouterModule,
    ReactiveFormsModule,
    FormsModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MatToolbarModule,
    MatButtonModule,
    MatIconModule,
    MatMenuModule,
    MatSnackBarModule,
    MatDivider,
    MatSidenavModule,
    MatListModule,
    MatCardModule,
    HttpClientModule,
  ],
  providers: [
    provideClientHydration(),
    provideAnimationsAsync(),
    provideHttpClient(withFetch())  // Configure HttpClient pour utiliser fetch
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
