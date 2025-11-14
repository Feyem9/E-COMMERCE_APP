import { Injectable } from '@angular/core';
import { Observable, BehaviorSubject } from 'rxjs';
import { map, tap } from 'rxjs/operators';
import { Product } from '../models/products';
import { ApiService } from '../services/api.service';

@Injectable({
  providedIn: 'root'
})
export class ProductsService {
  private productsSubject = new BehaviorSubject<Product[]>([]);
  public products$ = this.productsSubject.asObservable();
  
  private loadingSubject = new BehaviorSubject<boolean>(false);
  public loading$ = this.loadingSubject.asObservable();

  constructor(private apiService: ApiService) { }

  /**
   * Get all products
   */
  getProducts(): Observable<Product[]> {
    this.loadingSubject.next(true);
    return this.apiService.get<Product[]>('/product/')
      .pipe(
        tap(products => {
          this.productsSubject.next(products);
          this.loadingSubject.next(false);
        }),
        map(products => products || [])
      );
  }

  /**
   * Get product by ID
   */
  getProductById(id: number): Observable<Product> {
    return this.apiService.get<Product>(`/product/view-product/${id}`);
  }

  /**
   * Search products
   */
  searchProducts(query: string): Observable<Product[]> {
    return this.apiService.post<Product[]>('/product/search', { search: query });
  }

  /**
   * Get products from cache or fetch if not available
   */
  getProductsFromCache(): Product[] {
    return this.productsSubject.value;
  }

  /**
   * Refresh products
   */
  refreshProducts(): Observable<Product[]> {
    return this.getProducts();
  }
}
