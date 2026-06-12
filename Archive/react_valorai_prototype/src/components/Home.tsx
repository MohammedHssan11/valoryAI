export default function Home({ onNavigate }: { onNavigate: (v: any) => void }) {
  return (
    <main className="flex-1 pt-6 pb-[100px] px-6 flex flex-col gap-6 overflow-x-hidden overflow-y-auto w-full h-full relative z-10">
      {/* TopAppBar */}
      <header className="w-full flex justify-between items-center h-16 shrink-0 z-50">
        <button className="text-on-surface-variant hover:text-secondary-fixed transition-colors">
          <span className="material-symbols-outlined">menu</span>
        </button>
        <h1 className="font-headline-md text-xl font-bold text-secondary">ValorAI</h1>
        <button className="rounded-full w-8 h-8 bg-surface-container-high border border-white/10 overflow-hidden flex items-center justify-center relative">
          <span className="material-symbols-outlined text-on-surface-variant text-[20px]">person</span>
          <span className="absolute top-1 right-1 w-2 h-2 bg-secondary rounded-full shadow-[0_0_8px_#afecff]"></span>
        </button>
      </header>

      {/* Greeting Section */}
      <section className="flex flex-col gap-1 animate-fade-in mt-2">
        <h2 className="font-headline-lg text-3xl text-on-surface tracking-tight font-bold">Good Evening,</h2>
        <p className="font-headline-md text-xl text-secondary/80 font-semibold">Mohammed</p>
      </section>

      {/* Quick Actions Grid */}
      <section className="grid grid-cols-2 gap-4">
        <button onClick={() => onNavigate('valuations')} className="relative overflow-hidden group bg-secondary text-on-secondary rounded-xl p-4 flex flex-col items-start gap-2 shadow-[0_4px_20px_-5px_rgba(175,236,255,0.3)] transition-transform active:scale-95">
          <div className="absolute inset-0 bg-gradient-to-b from-white/20 to-transparent opacity-50"></div>
          <span className="material-symbols-outlined text-[28px] relative z-10" style={{ fontVariationSettings: "'FILL' 1" }}>add_circle</span>
          <span className="font-label-md font-bold text-sm relative z-10">New Valuation</span>
        </button>
        <button onClick={() => onNavigate('copilot')} className="bg-surface-container-low/40 backdrop-blur-xl border border-tertiary/30 text-tertiary rounded-xl p-4 flex flex-col items-start gap-2 transition-transform active:scale-95 hover:bg-surface-container-low/60 shadow-[0_4px_15px_-5px_rgba(27,224,178,0.1)]">
          <span className="material-symbols-outlined text-[28px]" style={{ fontVariationSettings: "'FILL' 1" }}>smart_toy</span>
          <span className="font-label-md text-sm font-semibold">Ask Copilot</span>
        </button>
      </section>

      {/* AI Insight */}
      <section className="relative rounded-xl p-[1px] bg-gradient-to-br from-secondary/50 via-surface-container to-surface-container shadow-[0_8px_30px_-10px_rgba(175,236,255,0.15)]">
        <div className="bg-surface-container-low/90 backdrop-blur-2xl rounded-xl p-5 flex flex-col gap-3 h-full">
          <div className="flex items-center gap-2 text-secondary">
            <span className="material-symbols-outlined animate-pulse">auto_awesome</span>
            <span className="font-label-md text-xs uppercase tracking-widest text-secondary/80 font-bold">AI Insight</span>
          </div>
          <p className="font-body-lg text-[15px] text-on-surface leading-relaxed">
            Properties in <span className="text-secondary font-medium">New Cairo</span> increased <span className="text-tertiary font-medium">3.2%</span> over the last 30 days. Consider reviewing your saved valuations.
          </p>
        </div>
      </section>

      {/* Portfolio Bento */}
      <section className="flex flex-col gap-3">
        <h3 className="font-headline-sm text-lg font-bold text-on-surface">Portfolio Overview</h3>
        <div className="grid grid-cols-2 gap-3">
          <div className="bg-surface-container/60 backdrop-blur-md border border-white/5 rounded-xl p-4 flex flex-col justify-between aspect-square">
            <div className="w-8 h-8 rounded-full bg-surface-variant flex items-center justify-center text-on-surface-variant">
              <span className="material-symbols-outlined text-[18px]">home_work</span>
            </div>
            <div>
              <p className="font-headline-md text-2xl font-bold text-on-surface">14</p>
              <p className="font-label-sm text-[11px] text-on-surface-variant">Properties Tracked</p>
            </div>
          </div>
          <div className="bg-surface-container/60 backdrop-blur-md border border-white/5 rounded-xl p-4 flex flex-col justify-between aspect-square">
            <div className="w-8 h-8 rounded-full bg-surface-variant flex items-center justify-center text-on-surface-variant">
              <span className="material-symbols-outlined text-[18px]">bookmark</span>
            </div>
            <div>
              <p className="font-headline-md text-2xl font-bold text-on-surface">8</p>
              <p className="font-label-sm text-[11px] text-on-surface-variant">Saved Valuations</p>
            </div>
          </div>
        </div>
      </section>

      {/* Market Signals */}
      <section className="flex flex-col gap-3">
        <div className="flex justify-between items-end">
          <h3 className="font-headline-sm text-lg font-bold text-on-surface">Market Signals</h3>
          <button className="font-label-sm text-xs text-secondary font-semibold">View All</button>
        </div>
        <div className="flex flex-col gap-2">
          <div className="bg-surface-container-low/40 border border-white/5 rounded-lg p-3 flex justify-between items-center">
            <div className="flex items-center gap-3">
              <div className="w-2 h-2 rounded-full bg-tertiary shadow-[0_0_8px_#1be0b2]"></div>
              <span className="font-body-md text-sm text-on-surface font-semibold">Zayed Demand</span>
            </div>
            <div className="flex items-center gap-1 text-tertiary bg-tertiary/10 px-2 py-1 rounded">
              <span className="material-symbols-outlined text-[14px]">arrow_upward</span>
              <span className="font-label-sm text-xs font-semibold">High</span>
            </div>
          </div>
        </div>
      </section>
      
      {/* Spacer */}
      <div className="h-8 shrink-0"></div>
    </main>
  );
}
