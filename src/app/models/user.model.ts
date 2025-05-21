export interface Register{
    id:number,
    email:string,
    name:string,
    password:string,
    contact:string,
    address:string,
    role:['customer' | 'admin']
  }
  
  export interface User{
    id:number,
    email:string,
    name:string,
    password:string,
    contact:string,
    address:string,
    role:string
  }


  export interface Login{
    email:string,
    password:string
  }