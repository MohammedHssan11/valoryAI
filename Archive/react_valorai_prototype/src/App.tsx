import { useState, useEffect } from 'react';
import AuthFlow from './components/Auth';
import MainLayout from './components/MainLayout';

export default function App() {
  const [view, setView] = useState<'splash' | 'onboarding' | 'auth' | 'main'>('splash');

  useEffect(() => {
    // Artificial splash delay
    if (view === 'splash') {
      const timer = setTimeout(() => setView('onboarding'), 2500);
      return () => clearTimeout(timer);
    }
  }, [view]);

  return (
    <div className="w-full min-h-screen bg-background text-on-surface font-body-md overflow-hidden selection:bg-secondary-fixed/30 selection:text-secondary-fixed flex flex-col md:max-w-[480px] md:mx-auto md:border-x md:border-white/10 md:shadow-2xl relative shadow-black">
      {view === 'splash' && <AuthFlow view="splash" onNext={() => setView('onboarding')} />}
      {view === 'onboarding' && <AuthFlow view="onboarding" onNext={() => setView('auth')} />}
      {view === 'auth' && <AuthFlow view="auth" onNext={() => setView('main')} />}
      {view === 'main' && <MainLayout onLogout={() => setView('auth')} />}
    </div>
  );
}
