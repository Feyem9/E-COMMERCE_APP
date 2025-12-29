import { Component, OnInit, OnDestroy, Inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser, CommonModule } from '@angular/common';

@Component({
  selector: 'app-pwa-install',
  standalone: true,
  imports: [CommonModule],
  template: `
    <!-- Install Banner (bottom of screen) -->
    <div class="pwa-install-banner" *ngIf="showInstallBanner && !isInstalled">
      <div class="banner-content">
        <div class="banner-icon">📱</div>
        <div class="banner-text">
          <strong>Installer Theck Market</strong>
          <span>Accédez rapidement depuis votre écran d'accueil</span>
        </div>
      </div>
      <div class="banner-actions">
        <button class="btn-install" (click)="installPwa()">
          <i class="fas fa-download me-1"></i>
          Installer
        </button>
        <button class="btn-dismiss" (click)="dismissBanner()">
          Plus tard
        </button>
      </div>
    </div>

    <!-- iOS Instructions Modal -->
    <div class="pwa-ios-modal" *ngIf="showIosInstructions">
      <div class="modal-backdrop" (click)="hideIosInstructions()"></div>
      <div class="modal-content">
        <button class="modal-close" (click)="hideIosInstructions()">✕</button>
        <div class="modal-icon">📱</div>
        <h3>Installer sur iPhone/iPad</h3>
        <ol>
          <li>
            <span class="step-icon">📤</span>
            Appuyez sur le bouton <strong>Partager</strong>
          </li>
          <li>
            <span class="step-icon">➕</span>
            Sélectionnez <strong>"Sur l'écran d'accueil"</strong>
          </li>
          <li>
            <span class="step-icon">✅</span>
            Appuyez sur <strong>Ajouter</strong>
          </li>
        </ol>
        <button class="btn-got-it" (click)="hideIosInstructions()">
          J'ai compris
        </button>
      </div>
    </div>
  `,
  styles: [`
    .pwa-install-banner {
      position: fixed;
      bottom: 0;
      left: 0;
      right: 0;
      background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
      color: white;
      padding: 16px 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.2);
      z-index: 9999;
      animation: slideUp 0.3s ease-out;

      @keyframes slideUp {
        from {
          transform: translateY(100%);
        }
        to {
          transform: translateY(0);
        }
      }

      .banner-content {
        display: flex;
        align-items: center;
        gap: 12px;

        .banner-icon {
          font-size: 2rem;
        }

        .banner-text {
          display: flex;
          flex-direction: column;

          strong {
            font-size: 1rem;
          }

          span {
            font-size: 0.8rem;
            opacity: 0.8;
          }
        }
      }

      .banner-actions {
        display: flex;
        gap: 8px;

        .btn-install {
          background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
          color: white;
          border: none;
          padding: 10px 20px;
          border-radius: 8px;
          font-weight: 600;
          cursor: pointer;
          transition: transform 0.2s ease;

          &:hover {
            transform: scale(1.05);
          }
        }

        .btn-dismiss {
          background: transparent;
          color: white;
          border: 1px solid rgba(255, 255, 255, 0.3);
          padding: 10px 16px;
          border-radius: 8px;
          cursor: pointer;

          &:hover {
            background: rgba(255, 255, 255, 0.1);
          }
        }
      }
    }

    .pwa-ios-modal {
      position: fixed;
      inset: 0;
      z-index: 10000;
      display: flex;
      align-items: center;
      justify-content: center;

      .modal-backdrop {
        position: absolute;
        inset: 0;
        background: rgba(0, 0, 0, 0.6);
        backdrop-filter: blur(4px);
      }

      .modal-content {
        position: relative;
        background: white;
        padding: 32px;
        border-radius: 20px;
        max-width: 340px;
        width: 90%;
        text-align: center;
        animation: zoomIn 0.3s ease-out;

        @keyframes zoomIn {
          from {
            transform: scale(0.8);
            opacity: 0;
          }
          to {
            transform: scale(1);
            opacity: 1;
          }
        }

        .modal-close {
          position: absolute;
          top: 12px;
          right: 12px;
          background: #f1f5f9;
          border: none;
          width: 32px;
          height: 32px;
          border-radius: 50%;
          cursor: pointer;
        }

        .modal-icon {
          font-size: 3rem;
          margin-bottom: 16px;
        }

        h3 {
          margin: 0 0 20px;
          color: #1e293b;
        }

        ol {
          text-align: left;
          padding-left: 0;
          list-style: none;
          margin: 0 0 24px;

          li {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 12px 0;
            border-bottom: 1px solid #e2e8f0;

            &:last-child {
              border-bottom: none;
            }

            .step-icon {
              font-size: 1.5rem;
            }
          }
        }

        .btn-got-it {
          background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
          color: white;
          border: none;
          padding: 12px 32px;
          border-radius: 8px;
          font-weight: 600;
          cursor: pointer;
          width: 100%;
        }
      }
    }

    @media (max-width: 576px) {
      .pwa-install-banner {
        flex-direction: column;
        gap: 12px;
        padding: 16px;

        .banner-actions {
          width: 100%;

          .btn-install, .btn-dismiss {
            flex: 1;
          }
        }
      }
    }
  `]
})
export class PwaInstallComponent implements OnInit, OnDestroy {
  showInstallBanner = false;
  showIosInstructions = false;
  isInstalled = false;
  private deferredPrompt: any;
  private isBrowser: boolean;

  constructor(@Inject(PLATFORM_ID) platformId: Object) {
    this.isBrowser = isPlatformBrowser(platformId);
  }

  ngOnInit(): void {
    if (!this.isBrowser) return;

    // Check if already installed
    this.isInstalled = window.matchMedia('(display-mode: standalone)').matches;
    
    if (this.isInstalled) {
      console.log('📱 App already installed as PWA');
      return;
    }

    // Check if user dismissed banner recently
    const dismissed = localStorage.getItem('pwa-banner-dismissed');
    if (dismissed) {
      const dismissedDate = new Date(dismissed);
      const daysSinceDismissed = (Date.now() - dismissedDate.getTime()) / (1000 * 60 * 60 * 24);
      if (daysSinceDismissed < 7) {
        console.log('📱 Banner dismissed recently');
        return;
      }
    }

    // Listen for install prompt (Chrome/Edge Android)
    window.addEventListener('beforeinstallprompt', (e: any) => {
      console.log('📱 beforeinstallprompt event received');
      e.preventDefault();
      this.deferredPrompt = e;
      this.showInstallBanner = true;
    });

    // For iOS Safari - show after delay
    if (this.isIos() && !this.isInStandaloneMode()) {
      console.log('📱 iOS detected - showing banner after delay');
      setTimeout(() => {
        this.showInstallBanner = true;
      }, 3000);
    }
    
    // For desktop browsers that support PWA but don't trigger beforeinstallprompt immediately
    // Show a subtle prompt after 10 seconds if no event was triggered
    setTimeout(() => {
      if (!this.showInstallBanner && !this.isInstalled && this.canInstall()) {
        console.log('📱 Showing install prompt after timeout');
        this.showInstallBanner = true;
      }
    }, 10000);
  }

  private isInStandaloneMode(): boolean {
    return window.matchMedia('(display-mode: standalone)').matches ||
           (window.navigator as any).standalone === true;
  }

  private canInstall(): boolean {
    // Check if the browser supports PWA installation
    return 'serviceWorker' in navigator && 
           window.matchMedia('(display-mode: browser)').matches;
  }

  ngOnDestroy(): void {
    // Cleanup if needed
  }

  installPwa(): void {
    if (this.isIos()) {
      this.showIosInstructions = true;
      return;
    }

    if (this.deferredPrompt) {
      this.deferredPrompt.prompt();
      this.deferredPrompt.userChoice.then((choiceResult: any) => {
        if (choiceResult.outcome === 'accepted') {
          console.log('✅ PWA installed');
          this.isInstalled = true;
        }
        this.deferredPrompt = null;
        this.showInstallBanner = false;
      });
    } else {
      // If no native prompt, show instructions for manual install
      alert('Pour installer l\'application : \n\nSur Chrome : Cliquez sur l\'icône "Installer" dans la barre d\'adresse.\nSur mobile : Cliquez sur le menu (3 points) puis "Installer l\'application".');
      this.showInstallBanner = false;
    }
  }

  dismissBanner(): void {
    this.showInstallBanner = false;
    if (this.isBrowser) {
      localStorage.setItem('pwa-banner-dismissed', new Date().toISOString());
    }
  }

  hideIosInstructions(): void {
    this.showIosInstructions = false;
    this.dismissBanner();
  }

  private isIos(): boolean {
    if (!this.isBrowser) return false;
    const userAgent = window.navigator.userAgent.toLowerCase();
    return /iphone|ipad|ipod/.test(userAgent);
  }
}
