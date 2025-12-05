import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

interface Category {
  id: number;
  name: string;
  image: string;
  productCount: number;
}

interface Product {
  id: number;
  name: string;
  price: number;
  image: string;
  category: string;
  rating: number;
}

@Component({
  selector: 'app-categories',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './categories.component.html',
  styleUrl: './categories.component.scss'
})
export class CategoriesComponent implements OnInit {
  categories: Category[] = [];
  featuredProducts: Product[] = [];
  loading: boolean = true;
  error: string | null = null;
  selectedCategory: string | null = null;

  ngOnInit(): void {
    this.loadCategories();
    this.loadFeaturedProducts();
  }

  loadCategories(): void {
    // Simuler le chargement des catégories
    setTimeout(() => {
      this.categories = [
        {
          id: 1,
          name: 'Smartphones',
          image: 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=200&h=200&fit=crop',
          productCount: 42
        },
        {
          id: 2,
          name: 'Tablets',
          image: 'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=200&h=200&fit=crop',
          productCount: 18
        },
        {
          id: 3,
          name: 'Laptops',
          image: 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=200&h=200&fit=crop',
          productCount: 25
        },
        {
          id: 4,
          name: 'Accessories',
          image: 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=200&h=200&fit=crop',
          productCount: 37
        },
        {
          id: 5,
          name: 'Audio',
          image: 'https://images.unsplash.com/photo-1583394838336-acd977736f90?w=200&h=200&fit=crop',
          productCount: 22
        },
        {
          id: 6,
          name: 'Wearables',
          image: 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=200&h=200&fit=crop',
          productCount: 15
        }
      ];
      this.loading = false;
    }, 800);
  }

  loadFeaturedProducts(): void {
    // Simuler le chargement des produits en vedette
    setTimeout(() => {
      this.featuredProducts = [
        {
          id: 1,
          name: 'iPhone 15 Pro Max',
          price: 1199.99,
          image: 'https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/iphone-15-pro-model-unselect-gallery-1-202309?wid=5120&hei=2880&fmt=p-jpg&qlt=80&.v=1692931459062',
          category: 'Smartphones',
          rating: 4.9
        },
        {
          id: 2,
          name: 'Samsung Galaxy S23 Ultra',
          price: 999.99,
          image: 'https://images.samsung.com/is/image/samsung/assets/us/smartphones/galaxy-s23-ultra/buy/Galaxy_S23_Ultra_Color_Selection_PhantomBlack_MO.jpg',
          category: 'Smartphones',
          rating: 4.8
        },
        {
          id: 3,
          name: 'MacBook Pro M2',
          price: 1999.99,
          image: 'https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/mbp14-spacegray-select-202301?wid=904&hei=840&fmt=jpeg&qlt=90&.v=1671767482209',
          category: 'Laptops',
          rating: 4.9
        },
        {
          id: 4,
          name: 'AirPods Pro 2nd Gen',
          price: 249.99,
          image: 'https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/airpods-pro-2nd-gen-hero-202209?wid=2000&hei=2000&fmt=jpeg&qlt=90&.v=1661743961000',
          category: 'Accessories',
          rating: 4.7
        }
      ];
    }, 1000);
  }

  selectCategory(categoryName: string): void {
    this.selectedCategory = categoryName;
    // Ici vous pourriez filtrer les produits par catégorie
    // ou naviguer vers une page de catégorie spécifique
  }

  addToCart(productId: number): void {
    console.log(`Product ${productId} added to cart`);
    // Logique pour ajouter au panier
  }

  addToFavorites(productId: number): void {
    console.log(`Product ${productId} added to favorites`);
    // Logique pour ajouter aux favoris
  }
}
