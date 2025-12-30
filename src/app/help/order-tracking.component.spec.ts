import { ComponentFixture, TestBed, fakeAsync, tick } from '@angular/core/testing';
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { OrderTrackingComponent } from './order-tracking.component';

describe('OrderTrackingComponent', () => {
  let component: OrderTrackingComponent;
  let fixture: ComponentFixture<OrderTrackingComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [
        RouterModule.forRoot([]),
        FormsModule,
        OrderTrackingComponent // Since it's standalone
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(OrderTrackingComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should initialize with default values', () => {
    expect(component.orderNumber).toBe('');
    expect(component.email).toBe('');
    expect(component.orderData).toBe(null);
    expect(component.loading).toBe(false);
  });

  it('should not search if orderNumber is empty', () => {
    component.orderNumber = '   ';
    component.searchOrder();
    expect(component.loading).toBe(false);
    expect(component.orderData).toBe(null);
  });

  it('should search order and set data after timeout', fakeAsync(() => {
    component.orderNumber = '12345';
    component.searchOrder();

    expect(component.loading).toBe(true);
    expect(component.orderData).toBe(null);

    tick(1500);

    expect(component.loading).toBe(false);
    expect(component.orderData).toBeDefined();
    expect(component.orderData.orderNumber).toBe('12345');
    expect(component.orderData.status).toBe('In Transit');
    expect(component.orderData.items.length).toBe(2);
    expect(component.orderData.total).toBe(1248);
  }));

  it('should reset search', () => {
    component.orderNumber = '12345';
    component.email = 'test@example.com';
    component.orderData = { test: 'data' };
    component.loading = true;

    component.resetSearch();

    expect(component.orderData).toBe(null);
    expect(component.orderNumber).toBe('');
    expect(component.email).toBe('');
    expect(component.loading).toBe(false);
  });
});