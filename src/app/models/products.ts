export interface Product {
  id: number;
  name: string;
  description: string;
  current_price: number;
  discount_price: number;
  quantity: number;
  picture: string;
  category?: string;  // 🔍 Catégorie du produit
}

export interface Cart {
  id: number;
  product_id: number;
  product_name: string;
  product_description: string;
  product_image: string;
  current_price: number;
  discount_price: number;
  quantity: number;
}

export interface ApiResponse<T> {
  message: string;
  data?: T;
  error?: string;
}

export interface Customer {
  id: number;
  name: string;
  email: string;
}