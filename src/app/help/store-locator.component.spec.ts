import { ComponentFixture, TestBed } from '@angular/core/testing';
import { RouterModule } from '@angular/router';
import { StoreLocatorComponent } from './store-locator.component';

describe('StoreLocatorComponent', () => {
  let component: StoreLocatorComponent;
  let fixture: ComponentFixture<StoreLocatorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [
        RouterModule.forRoot([]),
        StoreLocatorComponent // Since it's standalone
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(StoreLocatorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should initialize stores with correct data', () => {
    expect(component.stores).toBeDefined();
    expect(component.stores.length).toBe(3);
    expect(component.stores[0].name).toBe('Tech Market Downtown');
    expect(component.stores[0].address).toBe('123 Main Street, Downtown');
    expect(component.stores[0].phone).toBe('+1 (555) 123-4567');
    expect(component.stores[0].hours).toBe('Mon-Sat: 9AM-9PM, Sun: 11AM-7PM');
    expect(component.stores[0].distance).toBe('0.5 miles');
  });

  it('should have all required store properties', () => {
    component.stores.forEach(store => {
      expect(store.name).toBeDefined();
      expect(store.address).toBeDefined();
      expect(store.phone).toBeDefined();
      expect(store.hours).toBeDefined();
      expect(store.distance).toBeDefined();
    });
  });
});