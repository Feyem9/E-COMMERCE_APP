import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { PLATFORM_ID } from '@angular/core';
import { ApiService } from './api.service';
import { AuthService } from '../customers/auth.service';

describe('ApiService', () => {
  let service: ApiService;
  let httpMock: HttpTestingController;
  let authServiceMock: any;

  beforeEach(() => {
    authServiceMock = {
      getToken: () => 'fake-token',
      isAuthenticated: () => true
    };

    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [
        ApiService,
        { provide: AuthService, useValue: authServiceMock },
        { provide: PLATFORM_ID, useValue: 'browser' }
      ]
    });

    service = TestBed.inject(ApiService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should get data', () => {
    const testData = { message: 'test' };

    service.get('/test').subscribe(data => {
      expect(data).toEqual(testData);
    });

    const req = httpMock.expectOne('http://localhost:5000/test');
    expect(req.request.method).toBe('GET');
    expect(req.request.headers.get('Authorization')).toBe('Bearer fake-token');
    req.flush(testData);
  });

  it('should post data', () => {
    const testData = { name: 'test' };
    const responseData = { id: 1, name: 'test' };

    service.post('/test', testData).subscribe(data => {
      expect(data).toEqual(responseData);
    });

    const req = httpMock.expectOne('http://localhost:5000/test');
    expect(req.request.method).toBe('POST');
    expect(req.request.body).toEqual(testData);
    expect(req.request.headers.get('Authorization')).toBe('Bearer fake-token');
    req.flush(responseData);
  });

  it('should put data', () => {
    const testData = { name: 'updated' };
    const responseData = { id: 1, name: 'updated' };

    service.put('/test/1', testData).subscribe(data => {
      expect(data).toEqual(responseData);
    });

    const req = httpMock.expectOne('http://localhost:5000/test/1');
    expect(req.request.method).toBe('PUT');
    expect(req.request.body).toEqual(testData);
    req.flush(responseData);
  });

  it('should delete data', () => {
    service.delete('/test/1').subscribe(data => {
      expect(data).toEqual({});
    });

    const req = httpMock.expectOne('http://localhost:5000/test/1');
    expect(req.request.method).toBe('DELETE');
    req.flush({});
  });

  it('should get auth headers with token', () => {
    const headers = service.getAuthHeaders();
    expect(headers.get('Authorization')).toBe('Bearer fake-token');
    expect(headers.get('Content-Type')).toBe('application/json');
  });

  it('should get auth headers without token', () => {
    authServiceMock.getToken = () => null;
    const headers = service.getAuthHeaders();
    expect(headers.get('Authorization')).toBeNull();
    expect(headers.get('Content-Type')).toBe('application/json');
  });

  it('should check if authenticated', () => {
    expect(service.isAuthenticated()).toBe(true);
    authServiceMock.isAuthenticated = () => false;
    expect(service.isAuthenticated()).toBe(false);
  });

  it('should handle 401 error', () => {
    service.get('/test').subscribe({
      next: () => fail('should have failed'),
      error: (error) => {
        expect(error.message).toBe('Non autorisé - Veuillez vous connecter');
      }
    });

    const req = httpMock.expectOne('http://localhost:5000/test');
    req.flush('Unauthorized', { status: 401, statusText: 'Unauthorized' });
  });

  it('should handle 404 error', () => {
    service.get('/test').subscribe({
      next: () => fail('should have failed'),
      error: (error) => {
        expect(error.message).toBe('Ressource non trouvée');
      }
    });

    const req = httpMock.expectOne('http://localhost:5000/test');
    req.flush('Not Found', { status: 404, statusText: 'Not Found' });
  });
});