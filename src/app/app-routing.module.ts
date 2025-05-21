import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { NavbarComponent } from './navbar/navbar.component';
import { CartComponent } from './cart/cart.component';
import { CategoriesComponent } from './categories/categories.component';
import { FavoriteComponent } from './favorite/favorite.component';
import { OrderedComponent } from './ordered/ordered.component';
import { ProductComponent } from './product/product.component';
import { TransactionComponent } from './transaction/transaction.component';
import { LoginComponent } from './customers/login/login.component';
import { RegisterComponent } from './customers/register/register.component';
import { HomeComponent } from './home/home.component';
import { ProfileComponent } from './customers/profile/profile.component';
import { PaymentSuccessComponent } from './payment-success/payment-success.component';

const routes: Routes = [
  // {path : '' , component : NavbarComponent},
  {path : '' , component : HomeComponent},
  {path : 'cart' , component : CartComponent},
  {path : 'categories' , component : CategoriesComponent},
  {path : 'favorites' , component : FavoriteComponent},
  {path : 'ordered' , component : OrderedComponent},
  {path : 'product' , component : ProductComponent},
  {path : 'transaction' , component : TransactionComponent},
  {path : 'payment-success' , component : PaymentSuccessComponent},
  {path : 'login' , component : LoginComponent},
  {path : 'register' , component : RegisterComponent},
  {path : 'profile' , component : ProfileComponent}
]; 

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
