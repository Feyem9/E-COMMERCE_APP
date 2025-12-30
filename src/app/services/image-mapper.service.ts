import { Injectable } from '@angular/core';
import { Product } from '../models/products';

@Injectable({
  providedIn: 'root'
})
export class ImageMapperService {
  // Map product names/IDs to local images
  private localImageMap: { [key: string]: string } = {
    'iPhone 15 Pro': 'iphone.jpeg',
    'iPhone 15': 'iphone.jpeg',
    'iPhone 14': 'iphone.jpeg',
    'iPhone SE': 'iphone.jpeg',
    'Samsung Galaxy S24 Ultra': 'samsung.avif',
    'Samsung Galaxy S23': 'samsung.avif',
    'Google Pixel 8 Pro': 'smart.avif',
    'Google Pixel 8': 'smart.avif',
    'OnePlus 12': 'smart.avif',
    'Xiaomi 14': 'smart.avif',
    'infinix': 'infinix.jpeg',
  };

  // Rotation of images for products without specific mapping
  private rotationImages = [
    'iphone.jpeg',
    'samsung.avif',
    'smart.avif',
    'infinix.jpeg',
    'photo-1520189123429-6a76abfe7906.avif',
    'photo-1546054454-aa26e2b734c7.avif',
    'photo-1546868871-7041f2a55e12.avif',
  ];

  private imageIndex = 0;

  constructor() { }

  /**
   * Get local image path for product
   */
  getLocalImage(product: Product): string {
    // Try exact name match
    if (this.localImageMap[product.name]) {
      return `/` + this.localImageMap[product.name];
    }

    // Try partial match
    for (const [key, value] of Object.entries(this.localImageMap)) {
      if (product.name.toLowerCase().includes(key.toLowerCase())) {
        return `/` + value;
      }
    }

    // Use rotation
    const image = this.rotationImages[this.imageIndex % this.rotationImages.length];
    this.imageIndex++;
    return `/` + image;
  }

  /**
   * Get image with fallback
   */
  getImageUrl(product: Product): string {
    // Try Cloudinary URL first
    if (product.picture && this.isValidImageUrl(product.picture)) {
      return product.picture;
    }

    // Fallback to local image
    return this.getLocalImage(product);
  }

  /**
   * Check if URL is a valid image URL
   */
  private isValidImageUrl(url: string): boolean {
    // Check if it's a valid URL pattern
    try {
      new URL(url);
      return url.includes('.jpg') || url.includes('.jpeg') || 
             url.includes('.png') || url.includes('.webp') ||
             url.includes('.avif') || url.includes('.gif');
    } catch {
      return false;
    }
  }
}
