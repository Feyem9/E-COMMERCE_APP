import { TestBed } from '@angular/core/testing';
import { ImageMapperService } from './image-mapper.service';
import { Product } from '../models/products';

describe('ImageMapperService', () => {
  let service: ImageMapperService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ImageMapperService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should get local image for exact match', () => {
    const product: Product = { id: 1, name: 'iPhone 15 Pro', description: '', current_price: 1000, discount_price: 900, quantity: 10, picture: '' };
    const image = service.getLocalImage(product);
    expect(image).toBe('/iphone.jpeg');
  });

  it('should get local image for partial match', () => {
    const product: Product = { id: 1, name: 'Samsung Galaxy S24', description: '', current_price: 1000, discount_price: 900, quantity: 10, picture: '' };
    const image = service.getLocalImage(product);
    expect(image).toBe('/samsung.avif');
  });

  it('should get rotation image for no match', () => {
    const product: Product = { id: 1, name: 'Unknown Product', description: '', current_price: 1000, discount_price: 900, quantity: 10, picture: '' };
    const image = service.getLocalImage(product);
    expect(image).toBe('/iphone.jpeg'); // First in rotation
  });

  it('should rotate images for multiple unknown products', () => {
    const product1: Product = { id: 1, name: 'Unknown 1', description: '', current_price: 1000, discount_price: 900, quantity: 10, picture: '' };
    const product2: Product = { id: 2, name: 'Unknown 2', description: '', current_price: 1000, discount_price: 900, quantity: 10, picture: '' };

    const image1 = service.getLocalImage(product1);
    const image2 = service.getLocalImage(product2);

    expect(image1).toBe('/iphone.jpeg');
    expect(image2).toBe('/samsung.avif');
  });

  it('should return Cloudinary URL if valid', () => {
    const product: Product = {
      id: 1,
      name: 'Test Product',
      description: '',
      current_price: 1000,
      discount_price: 900,
      quantity: 10,
      picture: 'https://cloudinary.com/image.jpg'
    };
    const image = service.getImageUrl(product);
    expect(image).toBe('https://cloudinary.com/image.jpg');
  });

  it('should fallback to local image if Cloudinary URL invalid', () => {
    const product: Product = {
      id: 1,
      name: 'iPhone 15 Pro',
      description: '',
      current_price: 1000,
      discount_price: 900,
      quantity: 10,
      picture: 'invalid-url'
    };
    const image = service.getImageUrl(product);
    expect(image).toBe('/iphone.jpeg');
  });

  it('should validate image URLs correctly', () => {
    expect((service as any).isValidImageUrl('https://example.com/image.jpg')).toBe(true);
    expect((service as any).isValidImageUrl('https://example.com/image.jpeg')).toBe(true);
    expect((service as any).isValidImageUrl('https://example.com/image.png')).toBe(true);
    expect((service as any).isValidImageUrl('https://example.com/image.webp')).toBe(true);
    expect((service as any).isValidImageUrl('https://example.com/image.avif')).toBe(true);
    expect((service as any).isValidImageUrl('https://example.com/image.gif')).toBe(true);
    expect((service as any).isValidImageUrl('https://example.com/document.pdf')).toBe(false);
    expect((service as any).isValidImageUrl('invalid-url')).toBe(false);
  });
});