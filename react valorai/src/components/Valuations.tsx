import { useState } from 'react';

export default function Valuations() {
  const [step, setStep] = useState(1);
  const [view, setView] = useState<'wizard' | 'result'>('wizard');

  if (view === 'result') {
    return (
      <main className="w-full h-full flex flex-col overflow-y-auto overflow-x-hidden bg-background relative z-10 pb-20">
        <div className="ambient-glow"></div>
        <header className="w-full flex items-center justify-between p-4 z-20">
          <button onClick={() => setView('wizard')} className="w-10 h-10 flex items-center justify-center rounded-full bg-surface-container border border-white/5 text-on-surface-variant">
            <span className="material-symbols-outlined">arrow_back</span>
          </button>
          <div className="font-headline-md text-lg font-bold text-secondary">ValorAI Results</div>
          <div className="w-10 h-10"></div>
        </header>

        <div className="px-4 flex flex-col gap-6 z-10 relative mt-4">
          <section className="text-center relative">
            <div className="absolute inset-0 bg-secondary/5 blur-[100px] rounded-full pointer-events-none"></div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-surface-container/50 border border-secondary/20 mb-4 backdrop-blur-md">
              <span className="w-2 h-2 rounded-full bg-tertiary animate-pulse"></span>
              <span className="font-label-sm text-xs font-semibold text-tertiary">Live AI Valuation</span>
            </div>
            <h1 className="font-headline-lg text-4xl font-extrabold text-white brand-glow tracking-tight mb-2">
              $1,250,000
            </h1>
            <p className="font-body-lg text-sm text-on-surface-variant">Estimated Market Value for 3BHK Apartment</p>
          </section>

          {/* Confidence Score */}
          <section className="glass-panel border-secondary/20 rounded-xl p-5 relative overflow-hidden">
            <div className="absolute inset-0 ai-shimmer-bg opacity-20"></div>
            <div className="relative z-10 flex flex-col gap-2">
              <div className="flex justify-between items-end mb-2">
                <span className="font-label-md text-sm font-semibold">AI Confidence Score</span>
                <span className="font-headline-sm text-xl font-bold text-tertiary">94%</span>
              </div>
              <div className="h-2 w-full bg-surface-container-highest rounded-full overflow-hidden">
                <div className="h-full bg-gradient-to-r from-secondary to-tertiary w-[94%] rounded-full shadow-[0_0_10px_rgba(0,216,255,0.5)]"></div>
              </div>
            </div>
          </section>

          {/* AI Explanation */}
          <section className="glass-panel border-l-2 border-l-secondary rounded-xl p-5">
            <h2 className="font-headline-sm text-lg font-bold text-secondary mb-3 flex items-center gap-2">
              <span className="material-symbols-outlined">auto_awesome</span> Insights
            </h2>
            <p className="font-body-md text-sm text-on-surface opacity-90 leading-relaxed">
              This property commands a <strong>12% premium</strong> over neighborhood averages due to recent premium finishing. Consistent 4.5% YoY growth identified.
            </p>
          </section>

          {/* Map Preview */}
          <section className="glass-panel rounded-xl overflow-hidden h-48 relative border border-white/10">
            <div className="absolute inset-0 bg-cover bg-center opacity-60 mix-blend-luminosity filter contrast-125" style={{ backgroundImage: "url('https://lh3.googleusercontent.com/aida-public/AB6AXuBdys7VsPtrKY_-Ruzb2DIYtV7x4-XUt1AjvLIfd_X0QAr4_Udh2YkYQMIIFmwGsGudGb4BQQoSE20i7mYva-bgzMfiOu_oDAFUWFg_EkwmpURDo40iZhYTGqzW2u04PnYLqUwYX83o0k88Ewq7J2uBrBr6F4pwWr08pF1a4butZgPWLF--qbl0wsTi2osYvrl9bU5AucQ83F0ubxru7kMeGqRgRww-KHM9C_odYP0flPn38IQc0bpYQ0Sagl2mcwf2rHD6MLKF562B')" }}></div>
            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 flex flex-col items-center">
              <div className="bg-secondary text-background text-[10px] px-2 py-1 rounded font-bold mb-1">Subject</div>
              <div className="w-4 h-4 bg-secondary rounded-full border-2 border-background animate-pulse shadow-[0_0_15px_rgba(0,216,255,0.8)]"></div>
            </div>
          </section>
        </div>
      </main>
    );
  }

  // WIZARD
  return (
    <main className="w-full flex-1 h-full flex flex-col bg-background relative z-10 overflow-hidden pb-16">
      <header className="w-full flex justify-between items-center px-4 py-4 z-20 shrink-0">
        <button className="w-10 h-10 flex items-center justify-center rounded-full bg-surface-container-low border border-white/5 text-on-surface-variant">
          <span className="material-symbols-outlined">close</span>
        </button>
        <div className="font-headline-sm text-lg font-bold text-secondary flex items-center gap-2">
          <span className="material-symbols-outlined" style={{ fontVariationSettings: "'FILL' 1" }}>analytics</span>
          New Valuation
        </div>
        <div className="w-10 h-10"></div>
      </header>

      {/* Progress */}
      <div className="w-full px-4 mb-6 z-20 shrink-0">
        <div className="flex gap-1 w-full h-1.5 bg-surface-container-highest/30 rounded-full overflow-hidden">
          {[1,2,3,4,5].map(i => (
            <div key={i} className={`flex-1 transition-all rounded-full ${i <= step ? 'bg-secondary-container shadow-[0_0_10px_rgba(20,216,255,0.5)]' : 'bg-white/10'}`}></div>
          ))}
        </div>
      </div>

      <div className="flex-1 overflow-y-auto px-4 w-full flex flex-col items-center">
        <div className="w-full bg-surface-container/20 backdrop-blur-2xl border border-white/10 rounded-2xl p-6 relative overflow-hidden shadow-[0_20px_40px_-20px_rgba(0,0,0,0.5)] min-h-[400px] flex flex-col justify-center gap-6">
          <div className="text-center mb-2">
            <h2 className="font-headline-md text-xl font-bold text-on-surface mb-2">
              {step === 1 ? 'Select Category' : step === 2 ? 'Property Type' : step === 3 ? 'Refine Logic' : step === 4 ? 'Attributes' : 'Processing AI Insights'}
            </h2>
            <p className="font-body-md text-sm text-on-surface-variant">Choose the primary classification for your valuation.</p>
          </div>
          
          <div className="grid grid-cols-2 gap-3">
            {[1,2,3,4].map(idx => (
               <button key={idx} onClick={() => setStep(Math.min(5, step+1))} className="group flex flex-col items-center justify-center p-6 rounded-xl border border-white/10 bg-surface-container/40 hover:border-secondary-container hover:bg-secondary-container/10 transition-all text-center">
                 <span className="material-symbols-outlined text-[32px] text-primary-fixed-dim mb-2 group-hover:text-secondary group-hover:scale-110 transition-all font-light">home</span>
                 <span className="font-headline-sm text-sm font-semibold text-on-surface">Option {idx}</span>
               </button>
            ))}
          </div>
        </div>
      </div>

      <footer className="w-full px-4 py-4 flex justify-between items-center z-20 shrink-0 bg-background pt-2">
        <button onClick={() => setStep(Math.max(1, step-1))} className={`px-6 py-2 border border-secondary text-secondary rounded-full text-sm font-semibold ${step === 1 ? 'opacity-0' : 'opacity-100'}`}>Back</button>
        <button onClick={() => { if (step < 5) setStep(step+1); else setView('result'); }} className="px-8 py-2 bg-secondary-container text-on-secondary-fixed font-bold rounded-full text-sm flex items-center gap-2 shadow-[0_0_20px_rgba(20,216,255,0.2)]">
          {step === 5 ? 'Analyze Property' : 'Continue'} <span className="material-symbols-outlined text-[18px]">arrow_forward</span>
        </button>
      </footer>
    </main>
  );
}
