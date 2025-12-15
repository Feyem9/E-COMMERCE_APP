import { ComponentFixture, TestBed } from '@angular/core/testing';
import { RouterModule } from '@angular/router';
import { FaqsComponent } from './faqs.component';

describe('FaqsComponent', () => {
  let component: FaqsComponent;
  let fixture: ComponentFixture<FaqsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [
        RouterModule.forRoot([]),
        FaqsComponent // Since it's standalone
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(FaqsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should initialize faqs with correct structure', () => {
    expect(component.faqs).toBeDefined();
    expect(component.faqs.length).toBe(4);
    expect(component.faqs[0].category).toBe('Ordering');
    expect(component.faqs[0].questions.length).toBe(3);
    expect(component.faqs[0].questions[0].expanded).toBe(false);
  });

  it('should toggle faq expansion', () => {
    // Initially false
    expect(component.faqs[0].questions[0].expanded).toBe(false);

    // Toggle to true
    component.toggleFaq(0, 0);
    expect(component.faqs[0].questions[0].expanded).toBe(true);

    // Toggle back to false
    component.toggleFaq(0, 0);
    expect(component.faqs[0].questions[0].expanded).toBe(false);
  });

  it('should not affect other faqs when toggling', () => {
    component.toggleFaq(0, 0);
    expect(component.faqs[0].questions[0].expanded).toBe(true);
    expect(component.faqs[0].questions[1].expanded).toBe(false);
    expect(component.faqs[1].questions[0].expanded).toBe(false);
  });
});