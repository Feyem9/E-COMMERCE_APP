import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

interface Product {
  id: number;
  name: string;
  price: number;
  image: string;
  category: string;
  rating: number;
}

@Component({
  selector: 'app-favorite',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './favorite.component.html',
  styleUrl: './favorite.component.scss'
})
export class FavoriteComponent implements OnInit {
  favoriteProducts: Product[] = [];
  loading: boolean = true;
  error: string | null = null;

  ngOnInit(): void {
    this.loadFavoriteProducts();
  }

  loadFavoriteProducts(): void {
    // Simuler le chargement des produits favoris
    setTimeout(() => {
      this.favoriteProducts = [
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
          name: 'AirPods Pro 2nd Generation',
          price: 249.99,
          image: 'https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/airpods-pro-2nd-gen-hero-202209?wid=2000&hei=2000&fmt=jpeg&qlt=90&.v=1661743961000',
          category: 'Accessories',
          rating: 4.7
        }
      ];
      this.loading = false;
    }, 1000);
  }

  removeFromFavorites(productId: number): void {
    this.favoriteProducts = this.favoriteProducts.filter(product => product.id !== productId);
  }

  addToCart(productId: number): void {
    // Logique pour ajouter au panier
    // Ici vous pourriez appeler un service pour ajouter au panier
  }
}
