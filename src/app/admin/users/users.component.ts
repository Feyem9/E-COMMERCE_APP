import { Component, OnInit, OnDestroy } from '@angular/core';
import { AdminService, User } from '../services/admin.service';
import { Subject } from 'rxjs';
import { takeUntil, debounceTime, distinctUntilChanged } from 'rxjs/operators';

@Component({
  selector: 'app-admin-users',
  templateUrl: './users.component.html',
  styleUrls: ['./users.component.scss']
})
export class UsersComponent implements OnInit, OnDestroy {
  users: User[] = [];
  loading = true;
  error: string | null = null;
  
  // Pagination
  currentPage = 1;
  perPage = 10;
  totalPages = 1;
  totalUsers = 0;
  
  // Filters
  searchTerm = '';
  roleFilter = '';
  
  // Modal
  selectedUser: User | null = null;
  showModal = false;
  modalAction: 'view' | 'edit' | 'delete' = 'view';
  
  // Search subject for debounce
  private searchSubject = new Subject<string>();
  private destroy$ = new Subject<void>();

  constructor(private adminService: AdminService) {}

  ngOnInit(): void {
    this.loadUsers();
    
    // Setup search debounce
    this.searchSubject.pipe(
      debounceTime(400),
      distinctUntilChanged(),
      takeUntil(this.destroy$)
    ).subscribe(() => {
      this.currentPage = 1;
      this.loadUsers();
    });
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  loadUsers(): void {
    this.loading = true;
    this.error = null;

    this.adminService.getUsers(this.currentPage, this.perPage, this.searchTerm, this.roleFilter)
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (response) => {
          this.users = response.users;
          this.totalPages = response.pagination.pages;
          this.totalUsers = response.pagination.total;
          this.loading = false;
        },
        error: (err) => {
          this.error = 'Erreur lors du chargement des utilisateurs';
          this.loading = false;
          console.error(err);
        }
      });
  }

  onSearch(event: Event): void {
    const value = (event.target as HTMLInputElement).value;
    this.searchTerm = value;
    this.searchSubject.next(value);
  }

  onRoleFilterChange(event: Event): void {
    this.roleFilter = (event.target as HTMLSelectElement).value;
    this.currentPage = 1;
    this.loadUsers();
  }

  goToPage(page: number): void {
    if (page >= 1 && page <= this.totalPages) {
      this.currentPage = page;
      this.loadUsers();
    }
  }

  openModal(user: User, action: 'view' | 'edit' | 'delete'): void {
    this.selectedUser = { ...user };
    this.modalAction = action;
    this.showModal = true;
  }

  closeModal(): void {
    this.showModal = false;
    this.selectedUser = null;
  }

  toggleUserActive(): void {
    if (!this.selectedUser) return;

    const newStatus = !this.selectedUser.is_active;
    this.adminService.updateUserStatus(this.selectedUser.id, { is_active: newStatus })
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: () => {
          this.closeModal();
          this.loadUsers();
        },
        error: (err) => {
          console.error('Erreur mise à jour:', err);
          alert('Erreur lors de la mise à jour');
        }
      });
  }

  changeUserRole(role: string): void {
    if (!this.selectedUser) return;

    this.adminService.updateUserStatus(this.selectedUser.id, { role })
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: () => {
          this.closeModal();
          this.loadUsers();
        },
        error: (err) => {
          console.error('Erreur changement rôle:', err);
          alert('Erreur lors du changement de rôle');
        }
      });
  }

  deleteUser(): void {
    if (!this.selectedUser) return;

    if (confirm(`Êtes-vous sûr de vouloir supprimer ${this.selectedUser.name} ?`)) {
      this.adminService.deleteUser(this.selectedUser.id)
        .pipe(takeUntil(this.destroy$))
        .subscribe({
          next: () => {
            this.closeModal();
            this.loadUsers();
          },
          error: (err) => {
            console.error('Erreur suppression:', err);
            alert(err.error?.error || 'Erreur lors de la suppression');
          }
        });
    }
  }

  formatDate(dateStr: string): string {
    if (!dateStr) return '-';
    return new Date(dateStr).toLocaleDateString('fr-FR', {
      day: '2-digit',
      month: 'short',
      year: 'numeric'
    });
  }

  get pageNumbers(): number[] {
    const pages: number[] = [];
    const start = Math.max(1, this.currentPage - 2);
    const end = Math.min(this.totalPages, this.currentPage + 2);
    
    for (let i = start; i <= end; i++) {
      pages.push(i);
    }
    return pages;
  }
}
