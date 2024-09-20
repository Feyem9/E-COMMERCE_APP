import { Component, OnInit } from '@angular/core';
import { ProductsService } from '../service/products.service';
import { Product } from '../models/products';

@Component({
  selector: 'app-product',
  templateUrl: './product.component.html',
  styleUrl: './product.component.scss'
})
export class ProductComponent implements OnInit {

  products: Product[] = []

  constructor(private productService: ProductsService) { }

  // base_url = "http://localhost:5000/"

  ngOnInit(): void {
    this.productService.getProducts().subscribe((data : Product[  ]) => {
      this.products = data;
    },
    (error) => {
      console.error('Erreur lors du chargement des produits', error);
    } 
   )
    
  }
}
