import { initializeApp, getApp, getApps, type FirebaseOptions } from "firebase/app";
import {
  browserLocalPersistence,
  createUserWithEmailAndPassword,
  getAuth,
  onAuthStateChanged,
  sendPasswordResetEmail,
  setPersistence,
  signInWithEmailAndPassword,
  signOut,
  updateProfile,
  type Auth,
  type User,
} from "firebase/auth";
import { appConfig } from "@/core/config";

export interface FirebaseUserLike {
  uid: string;
  email: string | null;
  displayName: string | null;
  getIdToken(forceRefresh?: boolean): Promise<string>;
}

function configuredFirebaseOptions(): FirebaseOptions | null {
  const { firebase } = appConfig;
  if (!firebase.apiKey || !firebase.authDomain || !firebase.projectId || !firebase.appId) {
    return null;
  }

  return {
    apiKey: firebase.apiKey,
    authDomain: firebase.authDomain,
    projectId: firebase.projectId,
    appId: firebase.appId,
    storageBucket: firebase.storageBucket || undefined,
    messagingSenderId: firebase.messagingSenderId || undefined,
    measurementId: firebase.measurementId || undefined,
  };
}

export function isFirebaseConfigured(): boolean {
  return configuredFirebaseOptions() !== null;
}

function firebaseAuth(): Auth {
  const options = configuredFirebaseOptions();
  if (!options) {
    throw new Error("Firebase web authentication is not configured.");
  }

  const app = getApps().length > 0 ? getApp() : initializeApp(options);
  return getAuth(app);
}

let persistenceSetup: Promise<void> | null = null;

async function configuredAuth(): Promise<Auth> {
  const auth = firebaseAuth();
  persistenceSetup ??= setPersistence(auth, browserLocalPersistence);
  await persistenceSetup;
  return auth;
}

export async function getCurrentFirebaseUser(): Promise<FirebaseUserLike | null> {
  if (!isFirebaseConfigured()) return null;

  const auth = firebaseAuth();
  if (auth.currentUser) return auth.currentUser;

  return new Promise((resolve) => {
    const unsubscribe = onAuthStateChanged(
      auth,
      (user) => {
        unsubscribe();
        resolve(user);
      },
      () => {
        unsubscribe();
        resolve(null);
      },
    );
  });
}

export async function signInFirebase(email: string, password: string): Promise<FirebaseUserLike> {
  const auth = await configuredAuth();
  const credential = await signInWithEmailAndPassword(auth, email, password);
  return credential.user;
}

export async function signUpFirebase(
  email: string,
  password: string,
  displayName?: string,
): Promise<FirebaseUserLike> {
  const auth = await configuredAuth();
  const credential = await createUserWithEmailAndPassword(auth, email, password);
  const trimmedName = displayName?.trim();
  if (trimmedName) {
    await updateProfile(credential.user as User, { displayName: trimmedName });
  }
  return credential.user;
}

export async function sendFirebasePasswordReset(email: string): Promise<void> {
  const auth = await configuredAuth();
  await sendPasswordResetEmail(auth, email);
}

export async function signOutFirebase(): Promise<void> {
  if (!isFirebaseConfigured()) return;
  await signOut(firebaseAuth());
}
