import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-store-locator',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './store-locator.component.html',
  styleUrls: ['./store-locator.component.css']
})
export class StoreLocatorComponent {
  stores = [
    {
      name: 'Tech Market Downtown',
      address: '123 Main Street, Downtown',
      phone: '+1 (555) 123-4567',
      hours: 'Mon-Sat: 9AM-9PM, Sun: 11AM-7PM',
      distance: '0.5 miles'
    },
    {
      name: 'Tech Market Mall',
      address: '456 Shopping Center, Mall District',
      phone: '+1 (555) 234-5678',
      hours: 'Mon-Sat: 10AM-10PM, Sun: 12PM-8PM',
      distance: '2.1 miles'
    },
    {
      name: 'Tech Market Express',
      address: '789 Quick Stop Ave, Express Lane',
      phone: '+1 (555) 345-6789',
      hours: 'Daily: 8AM-11PM',
      distance: '3.7 miles'
    }
  ];
}