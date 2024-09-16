import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss'
})
export class HomeComponent implements OnInit {

  featuredProducts = [
    {
      name: 'Product 1',
      price: 29.99,
      image: "../../assets/59510c60866aaae1a7034ceb0be5476c.webp" 
    },
    {
      name: 'Product 2',
      price: 39.99,
      image: 'src/assets/40a01f385d06eb584d19f254704dc839.webp'
    },
    {
      name: 'Product 3',
      price: 19.99,
      image: 'src/assets/CAMON 20 Premier 5G_Six View_Day.webp'
    }
  ];

  constructor() { }

  ngOnInit(): void {
  } 
}
