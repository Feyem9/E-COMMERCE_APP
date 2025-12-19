import { ComponentFixture, TestBed } from '@angular/core/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { RouterTestingModule } from '@angular/router/testing';

import { OrderedComponent } from './ordered.component';

describe('OrderedComponent', () => {
  let component: OrderedComponent;
  let fixture: ComponentFixture<OrderedComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [OrderedComponent, HttpClientTestingModule, RouterTestingModule]
    })
    .compileComponents();

    fixture = TestBed.createComponent(OrderedComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
