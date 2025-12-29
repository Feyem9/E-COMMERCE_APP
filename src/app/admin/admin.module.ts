import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';

import { AdminRoutingModule } from './admin-routing.module';

// Components
import { DashboardComponent } from './dashboard/dashboard.component';
import { UsersComponent } from './users/users.component';
import { ProductsComponent } from './products/products.component';
import { OrdersComponent } from './orders/orders.component';
import { TransactionsComponent } from './transactions/transactions.component';

// Services
import { AdminService } from './services/admin.service';
import { AuthInterceptor } from './services/auth.interceptor';

// Guards
import { AdminGuard } from './guards/admin.guard';

@NgModule({
  declarations: [
    DashboardComponent,
    UsersComponent,
    ProductsComponent,
    OrdersComponent,
    TransactionsComponent
  ],
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    RouterModule,
    HttpClientModule,
    AdminRoutingModule
  ],
  providers: [
    AdminService,
    AdminGuard,
    {
      provide: HTTP_INTERCEPTORS,
      useClass: AuthInterceptor,
      multi: true
    }
  ]
})
export class AdminModule { }
