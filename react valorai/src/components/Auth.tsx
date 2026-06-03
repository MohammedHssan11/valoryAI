import { useState } from 'react';

export default function AuthFlow({ view, onNext }: { view: string; onNext: () => void }) {
  const [authStep, setAuthStep] = useState<'login' | 'signup' | 'reset'>('login');

  if (view === 'splash') {
    return (
      <main className="w-full h-full flex flex-col items-center justify-center relative animate-fade-in z-10 flex-1">
        <div className="absolute inset-0 z-0 flex items-center justify-center pointer-events-none">
          <div className="w-[300px] h-[300px] bg-secondary-container/10 rounded-full blur-[80px] animate-pulse-slow"></div>
        </div>
        <div className="relative z-10 flex flex-col items-center">
          <h1 className="font-headline-lg text-[40px] text-on-surface tracking-tighter brand-glow mb-xl select-none font-bold">
            ValorAI
          </h1>
          <div className="flex flex-col items-center gap-sm">
            <div className="w-32 h-1 bg-surface-container-high rounded-full overflow-hidden relative">
              <div className="absolute top-0 left-0 h-full w-1/3 bg-secondary-container rounded-full animate-shimmer indicator-glow"></div>
            </div>
            <p className="font-label-sm text-sm text-secondary-fixed/70 tracking-[0.2em] uppercase animate-pulse-slow select-none mt-4">
              Synchronizing Core
            </p>
          </div>
        </div>
      </main>
    );
  }

  if (view === 'onboarding') {
    return (
      <main className="w-full h-full flex flex-col relative overflow-hidden flex-1 z-10">
        <div className="absolute top-[-10%] left-[-10%] w-[50vw] h-[50vw] bg-secondary-container/5 rounded-full blur-[100px] pointer-events-none"></div>
        <div className="flex-1 flex flex-col z-10 px-margin-mobile pt-xl pb-2xl md:p-2xl w-full relative h-full justify-between">
          <div className="flex justify-between items-center pt-sm w-full">
            <span className="font-headline-sm text-lg text-secondary font-bold tracking-tight">ValorAI</span>
            <button onClick={onNext} className="font-label-md text-on-surface-variant hover:text-secondary-fixed transition-colors">Skip</button>
          </div>
          
          <div className="flex-1 flex flex-col items-center justify-center space-y-2xl w-full py-8">
            <div className="relative w-full aspect-square max-w-[280px] rounded-full flex items-center justify-center p-md group">
              <div className="absolute inset-0 rounded-full border border-secondary-fixed-dim/30 bg-surface-container/20 backdrop-blur-xl shadow-[0_0_40px_-10px_rgba(20,216,255,0.15)] transition-all duration-700 ease-in-out"></div>
              <div className="absolute inset-2 rounded-full border border-tertiary-fixed-dim/20"></div>
              <div className="w-full h-full rounded-full bg-cover bg-center z-10 relative overflow-hidden flex items-center justify-center" style={{ backgroundImage: "url('https://lh3.googleusercontent.com/aida-public/AB6AXuBtWgIRi2AS4pzl5eoVDW6Tn-4WKlhxjaaXyIoDr8EmC4JchgMmpKoRFw-u8UZkIRxDeAvjfL1EEyLuO2NgMu-AZmRQ4Ni-6Bu8MbscPPg29glXv2v0TKNTZvC_blJQq43fmPHJe2cJXvhsOXkI9syKxZ3afgAo1UoX8MfOTlU4cUd41doimV1M_cFa21VivAp-0pONRYmpyTL136YS8SEgd5-gdJwrPUG4O6sZIO-sS9xVIC5nlaQkH00eDq5jR_bWXTDs1LFFzBQS')", backgroundBlendMode: 'luminosity', backgroundColor: 'rgba(0, 54, 65, 0.6)' }}>
                <span className="material-symbols-outlined text-[80px] text-secondary-fixed-dim/80 absolute drop-shadow-[0_0_15px_rgba(20,216,255,0.5)]" style={{ fontVariationSettings: "'FILL' 0" }}>domain</span>
              </div>
            </div>
            <div className="flex flex-col items-center text-center space-y-md w-full pt-8">
              <h1 className="font-headline-lg text-3xl font-bold text-on-surface mb-2">Precision Intelligence.</h1>
              <p className="font-body-lg text-on-surface-variant max-w-[300px]">
                Access real-time AI-driven valuations for any property with unparalleled accuracy.
              </p>
            </div>
          </div>
          
          <div className="w-full flex flex-col items-center space-y-lg pt-xl">
            <div className="flex items-center justify-center space-x-sm mb-4">
              <div className="w-8 h-2 rounded-full bg-secondary-fixed-dim shadow-[0_0_12px_rgba(20,216,255,0.4)]"></div>
              <div className="w-2 h-2 rounded-full bg-surface-variant"></div>
            </div>
            <button onClick={onNext} className="w-full relative overflow-hidden group bg-secondary-fixed-dim text-on-secondary-fixed rounded-xl py-4 font-label-md flex items-center justify-center transition-transform active:scale-[0.98] shadow-[0_8px_30px_-10px_rgba(20,216,255,0.25)]">
              <span className="relative z-10 font-bold tracking-wide">Next</span>
              <span className="material-symbols-outlined ml-2 relative z-10 text-[18px]">arrow_forward</span>
            </button>
          </div>
        </div>
      </main>
    );
  }

  // Auth View (Login, Signup, Reset)
  return (
    <main className="w-full h-full flex flex-col relative overflow-hidden flex-1 z-10 bg-background items-center justify-center p-4">
      <div className="absolute top-[40%] left-[60%] w-[30vw] h-[30vw] bg-secondary-fixed/5 rounded-full blur-[100px] pointer-events-none"></div>
      
      <div className="w-full max-w-[420px] bg-surface-container/10 backdrop-blur-[20px] rounded-2xl border border-white/10 shadow-[0_20px_50px_-12px_rgba(0,0,0,0.5)] p-6 z-10">
        <div className="text-center mb-8">
          <div className="flex items-center justify-center gap-2 mb-4 text-secondary-container">
            <span className="material-symbols-outlined text-[32px]" style={{ fontVariationSettings: "'FILL' 1" }}>view_in_ar</span>
            <h1 className="font-headline-sm tracking-tight text-on-surface text-xl font-bold">ValorAI</h1>
          </div>
          <h2 className="font-headline-md text-2xl text-on-surface font-bold mb-2">
            {authStep === 'login' ? 'Welcome Back' : authStep === 'signup' ? 'Join ValorAI' : 'Reset Password'}
          </h2>
          <p className="font-body-md text-on-surface-variant">
            {authStep === 'login' ? 'Sign in to access your intelligence dashboard.' : authStep === 'signup' ? 'Elite Intelligence for Real Estate' : 'Enter your email to receive a recovery link.'}
          </p>
        </div>
        
        <form className="space-y-4" onSubmit={(e) => { e.preventDefault(); onNext(); }}>
          {authStep === 'signup' && (
            <div className="relative group">
              <label className="block font-label-sm text-on-surface-variant mb-1">Full Name</label>
              <div className="relative">
                <span className="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-on-surface-variant/50">person</span>
                <input type="text" placeholder="John Doe" required className="w-full bg-surface-container-lowest text-on-surface pl-12 pr-4 py-3 rounded-t border-b border-white/10 focus:border-secondary-container focus:outline-none transition-colors" />
              </div>
            </div>
          )}
          
          <div className="relative group">
            <label className="block font-label-sm text-on-surface-variant mb-1">Email Address</label>
            <div className="relative">
              <span className="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-on-surface-variant/50">mail</span>
              <input type="email" placeholder="you@example.com" required className="w-full bg-surface-container-lowest text-on-surface pl-12 pr-4 py-3 rounded-t border-b border-white/10 focus:border-secondary-container focus:outline-none transition-colors" />
            </div>
          </div>
          
          {authStep !== 'reset' && (
            <div className="relative group">
              <label className="block font-label-sm text-on-surface-variant mb-1">Password</label>
              <div className="relative">
                <span className="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-on-surface-variant/50">lock</span>
                <input type="password" placeholder="••••••••" required className="w-full bg-surface-container-lowest text-on-surface pl-12 pr-4 py-3 rounded-t border-b border-white/10 focus:border-secondary-container focus:outline-none transition-colors" />
              </div>
              {authStep === 'login' && (
                <div className="flex justify-end mt-2">
                  <button type="button" onClick={() => setAuthStep('reset')} className="font-label-sm text-secondary-container hover:text-secondary-fixed transition-colors">Forgot Password?</button>
                </div>
              )}
            </div>
          )}

          <button type="submit" className="w-full mt-8 bg-secondary-container text-on-secondary-fixed font-bold py-3 rounded-lg flex items-center justify-center gap-2 shadow-[0_0_20px_-5px_rgba(20,216,255,0.3)] hover:shadow-[0_0_30px_-5px_rgba(20,216,255,0.6)] transition-all">
            <span>{authStep === 'login' ? 'Login' : authStep === 'signup' ? 'Sign Up' : 'Send Link'}</span>
            <span className="material-symbols-outlined text-[18px]">arrow_forward</span>
          </button>
        </form>

        <div className="mt-8 text-center text-on-surface-variant">
          {authStep === 'login' ? (
            <p>Don't have an account? <button onClick={() => setAuthStep('signup')} className="text-secondary-container font-bold hover:text-secondary-fixed">Create Account</button></p>
          ) : authStep === 'signup' ? (
            <p>Already have an account? <button onClick={() => setAuthStep('login')} className="text-secondary-container font-bold hover:text-secondary-fixed">Login</button></p>
          ) : (
            <p><button onClick={() => setAuthStep('login')} className="text-secondary-container font-bold hover:text-secondary-fixed">Back to Login</button></p>
          )}
        </div>
      </div>
    </main>
  );
}
