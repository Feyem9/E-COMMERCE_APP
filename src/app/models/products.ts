export interface Product {
    product: any;
    message: any;
    id: number;
    product_id:number;
    product_name: string;
    current_price: number;
    quantity: number;
    discount_price: number;
    picture: string;
    product_description: string;
    product_image:string;
    description:string;
  }


  export interface Cart{
    product_description: any;
    product_name: any;
    id: number;
    picture:string;
    description:string;
    current_price:number;
    quantity: number;
    product_image:string;

  }