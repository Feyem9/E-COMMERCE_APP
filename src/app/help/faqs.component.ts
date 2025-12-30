import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-faqs',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './faqs.component.html',
  styleUrls: ['./faqs.component.css']
})
export class FaqsComponent {
  faqs = [
    {
      category: 'Ordering',
      questions: [
        {
          question: 'How do I place an order?',
          answer: 'You can place an order by browsing our products, adding items to your cart, and proceeding to checkout. You\'ll need to create an account or log in to complete your purchase.',
          expanded: false
        },
        {
          question: 'Can I modify or cancel my order?',
          answer: 'You can modify or cancel your order within 1 hour of placing it. After this time, the order may have already been processed and shipped.',
          expanded: false
        },
        {
          question: 'What payment methods do you accept?',
          answer: 'We accept all major credit cards (Visa, MasterCard, American Express), PayPal, and Apple Pay.',
          expanded: false
        }
      ]
    },
    {
      category: 'Shipping & Delivery',
      questions: [
        {
          question: 'How long does shipping take?',
          answer: 'Standard shipping takes 3-5 business days. Express shipping takes 1-2 business days. Same-day delivery is available in select cities.',
          expanded: false
        },
        {
          question: 'Do you ship internationally?',
          answer: 'Currently, we only ship within the United States. We\'re working on expanding international shipping soon.',
          expanded: false
        },
        {
          question: 'How can I track my order?',
          answer: 'Once your order ships, you\'ll receive a tracking number via email. You can also track your order in your account dashboard.',
          expanded: false
        }
      ]
    },
    {
      category: 'Returns & Refunds',
      questions: [
        {
          question: 'What is your return policy?',
          answer: 'We offer a 30-day return policy for most items. Products must be in original condition with all packaging and accessories.',
          expanded: false
        },
        {
          question: 'How do I return an item?',
          answer: 'Log into your account, go to "My Orders", find your order, and click "Return Item". Print the prepaid shipping label and drop off at any authorized shipping location.',
          expanded: false
        },
        {
          question: 'When will I receive my refund?',
          answer: 'Refunds are processed within 5-7 business days after we receive your returned item. The refund will appear on your original payment method.',
          expanded: false
        }
      ]
    },
    {
      category: 'Account & Technical',
      questions: [
        {
          question: 'How do I create an account?',
          answer: 'Click "Register" in the top menu, fill out the required information, and verify your email address. You can then log in with your credentials.',
          expanded: false
        },
        {
          question: 'I forgot my password. How do I reset it?',
          answer: 'Click "Login" then "Forgot Password". Enter your email address and we\'ll send you a password reset link.',
          expanded: false
        },
        {
          question: 'How do I update my account information?',
          answer: 'Log into your account and click "Profile" to update your personal information, shipping addresses, and payment methods.',
          expanded: false
        }
      ]
    }
  ];

  toggleFaq(categoryIndex: number, questionIndex: number) {
    this.faqs[categoryIndex].questions[questionIndex].expanded = 
      !this.faqs[categoryIndex].questions[questionIndex].expanded;
  }
}