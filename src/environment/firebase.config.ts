/**
 * 🔔 Firebase Cloud Messaging Configuration
 * 
 * Steps to enable push notifications:
 * 
 * 1. Go to Firebase Console: https://console.firebase.google.com
 * 2. Create a new project or use existing one
 * 3. Add a web app to get your config
 * 4. Enable Cloud Messaging
 * 5. Replace the config below with your Firebase project config
 * 6. Get your VAPID key from Project Settings > Cloud Messaging
 */

export const firebaseConfig = {
  apiKey: "YOUR_API_KEY",
  authDomain: "YOUR_PROJECT.firebaseapp.com",
  projectId: "YOUR_PROJECT_ID",
  storageBucket: "YOUR_PROJECT.appspot.com",
  messagingSenderId: "YOUR_SENDER_ID",
  appId: "YOUR_APP_ID",
  measurementId: "G-XXXXXXXXXX"
};

// VAPID key for push notifications
export const vapidKey = "YOUR_VAPID_KEY";

/**
 * Instructions to get VAPID key:
 * 1. Firebase Console > Project Settings
 * 2. Cloud Messaging tab
 * 3. Web Push certificates section
 * 4. Generate key pair (or use existing)
 * 5. Copy the key pair
 */
