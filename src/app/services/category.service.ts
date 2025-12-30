import { Injectable } from '@angular/core';
import { ApiService } from './api.service';
import { Observable } from 'rxjs';

interface Category {
  id: number;
  name: string;
  created_at?: string;
}

interface CategoryResponse {
  categories: Category[];
}

@Injectable({
  providedIn: 'root'
})
export class CategoryService {
  
  constructor(private apiService: ApiService) { }

  /**
   * Get all categories from backend
   */
  getCategories(): Observable<Category[]> {
    return this.apiService.get<Category[]>('/category/');
  }

  /**
   * Get a specific category by ID
   */
  getCategoryById(id: number): Observable<Category> {
    return this.apiService.get<Category>(`/category/view_category/${id}`);
  }

  /**
   * Add a new category
   */
  addCategory(name: string): Observable<Category> {
    return this.apiService.post<Category>('/category/add_category', { name });
  }

  /**
   * Update a category
   */
  updateCategory(id: number, name: string): Observable<Category> {
    return this.apiService.post<Category>(`/category/update_category/${id}`, { name });
  }

  /**
   * Delete a category
   */
  deleteCategory(id: number): Observable<any> {
    return this.apiService.post(`/category/delete_category/${id}`, { delete: 'true' });
  }

  /**
   * Get categories with product counts (if backend supports it)
   */
  getCategoriesWithProductCounts(): Observable<any[]> {
    // This would need backend support to return product counts per category
    // For now, we'll use the basic categories endpoint
    return this.getCategories();
  }
}