import { TestBed } from '@angular/core/testing';
import { of } from 'rxjs';
import { CategoryService } from './category.service';
import { ApiService } from './api.service';

describe('CategoryService', () => {
  let service: CategoryService;
  let apiServiceMock: any;

  beforeEach(() => {
    apiServiceMock = {
      get: jasmine.createSpy('get'),
      post: jasmine.createSpy('post')
    };

    TestBed.configureTestingModule({
      providers: [
        CategoryService,
        { provide: ApiService, useValue: apiServiceMock }
      ]
    });

    service = TestBed.inject(CategoryService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should get categories', () => {
    const mockCategories = [{ id: 1, name: 'Electronics' }];
    apiServiceMock.get.and.returnValue(of(mockCategories));

    service.getCategories().subscribe(categories => {
      expect(categories).toEqual(mockCategories);
    });

    expect(apiServiceMock.get).toHaveBeenCalledWith('/category/');
  });

  it('should get category by id', () => {
    const mockCategory = { id: 1, name: 'Electronics' };
    apiServiceMock.get.and.returnValue(of(mockCategory));

    service.getCategoryById(1).subscribe(category => {
      expect(category).toEqual(mockCategory);
    });

    expect(apiServiceMock.get).toHaveBeenCalledWith('/category/view_category/1');
  });

  it('should add category', () => {
    const mockCategory = { id: 1, name: 'New Category' };
    apiServiceMock.post.and.returnValue(of(mockCategory));

    service.addCategory('New Category').subscribe(category => {
      expect(category).toEqual(mockCategory);
    });

    expect(apiServiceMock.post).toHaveBeenCalledWith('/category/add_category', { name: 'New Category' });
  });

  it('should update category', () => {
    const mockCategory = { id: 1, name: 'Updated Category' };
    apiServiceMock.post.and.returnValue(of(mockCategory));

    service.updateCategory(1, 'Updated Category').subscribe(category => {
      expect(category).toEqual(mockCategory);
    });

    expect(apiServiceMock.post).toHaveBeenCalledWith('/category/update_category/1', { name: 'Updated Category' });
  });

  it('should delete category', () => {
    apiServiceMock.post.and.returnValue(of({}));

    service.deleteCategory(1).subscribe(result => {
      expect(result).toEqual({});
    });

    expect(apiServiceMock.post).toHaveBeenCalledWith('/category/delete_category/1', { delete: 'true' });
  });

  it('should get categories with product counts', () => {
    const mockCategories = [{ id: 1, name: 'Electronics' }];
    spyOn(service, 'getCategories').and.returnValue(of(mockCategories));

    service.getCategoriesWithProductCounts().subscribe(categories => {
      expect(categories).toEqual(mockCategories);
    });

    expect(service.getCategories).toHaveBeenCalled();
  });
});