export interface Register{
    email: string;
    name: string;
    password: string;
    contact: string;
    address: string;
    role?: string;
  }
  
  export interface User{
    id: number;
    email: string;
    name: string;
    password: string;
    contact: string;
    address: string;
    role: string;
  }


  export interface Login{
    email: string;
    password: string;
  }