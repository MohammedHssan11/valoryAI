export default function Copilot() {
  return (
    <main className="flex-1 flex flex-col h-full bg-background relative z-10 overflow-hidden w-full pb-20">
      <div className="ambient-glow"></div>
      
      {/* TopAppBar Copilot Context */}
      <header className="bg-background/80 backdrop-blur-xl border-b border-white/10 flex items-center px-4 h-16 shrink-0 z-20">
        <span className="font-headline-md text-lg font-bold text-secondary">ValorAI Copilot</span>
      </header>
      
      <div className="flex-1 overflow-y-auto px-4 py-6 flex flex-col gap-6 z-10 w-full">
        <div className="flex justify-center">
          <span className="px-4 py-1 rounded-full glass-panel font-label-sm text-[10px] text-on-surface-variant font-semibold">Today</span>
        </div>

        {/* User Msg */}
        <div className="flex flex-col items-end gap-1 max-w-[85%] self-end">
          <div className="px-4 py-3 rounded-2xl rounded-tr-sm bg-surface-container-highest border border-white/5 text-on-surface text-sm shadow-lg leading-relaxed">
            Analyze the current investment potential of premium properties focusing on projected yields.
          </div>
        </div>

        {/* AI Msg */}
        <div className="flex flex-col items-start gap-3 max-w-[95%]">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-primary-container border border-secondary/30 flex items-center justify-center shadow-[0_0_15px_rgba(20,216,255,0.2)]">
              <span className="material-symbols-outlined text-secondary text-[18px]">smart_toy</span>
            </div>
            <span className="font-label-md text-sm font-semibold text-secondary">Valor Advisor</span>
          </div>
          
          <div className="text-sm text-on-surface leading-relaxed pl-10">
            <p className="mb-3">Based on institutional models, here is a synthesized breakdown of the signals and references.</p>
            
            {/* Bento Evidence */}
            <div className="glass-card-ai rounded-xl p-4 flex flex-col gap-2 relative overflow-hidden mb-4">
              <div className="absolute top-0 left-0 w-full h-1 ai-shimmer-bg"></div>
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-1 text-secondary text-xs uppercase font-bold tracking-wider">
                  <span className="material-symbols-outlined text-[16px]">monitoring</span> Market Signals
                </div>
              </div>
              <div className="flex items-end gap-2">
                <div className="font-headline-lg text-3xl font-extrabold text-white">6.8%</div>
                <div className="text-sm font-bold text-tertiary flex items-center pb-1">
                  <span className="material-symbols-outlined text-[16px]">arrow_upward</span> 1.2%
                </div>
              </div>
              <div className="text-[11px] text-on-surface-variant">Projected 3-Year Avg Yield</div>
            </div>
            
            {/* Action Chips */}
            <div className="flex flex-wrap gap-2">
               <button className="px-3 py-1 rounded-full border border-secondary/30 text-secondary text-[11px] font-semibold flex items-center gap-1 bg-secondary/10">
                 <span className="material-symbols-outlined text-[14px]">add_circle</span> Save to Portfolio
               </button>
            </div>
          </div>
        </div>
      </div>
      
      {/* Input Area */}
      <div className="w-full px-4 pt-2 pb-6 shrink-0 z-20">
        <div className="flex gap-2 overflow-x-auto hide-scrollbar mb-2">
          <button className="shrink-0 px-3 py-1.5 rounded-full glass-panel text-on-surface-variant text-[11px] font-medium whitespace-nowrap">Generate forecast</button>
          <button className="shrink-0 px-3 py-1.5 rounded-full glass-panel text-on-surface-variant text-[11px] font-medium whitespace-nowrap">Compare options</button>
        </div>
        <div className="relative w-full glass-input rounded-2xl flex items-end p-2 shadow-2xl">
          <button className="p-2 text-on-surface-variant">
            <span className="material-symbols-outlined">attach_file</span>
          </button>
          <textarea 
            className="flex-1 bg-transparent border-none text-on-surface text-sm focus:ring-0 resize-none py-2 px-2"
            placeholder="Ask AI Advisor..."
            rows={1}
          />
          <button className="p-2 m-1 rounded-xl bg-secondary text-on-secondary flex items-center shadow-[0_0_15px_rgba(175,236,255,0.4)]">
            <span className="material-symbols-outlined" style={{ fontVariationSettings: "'FILL' 1" }}>send</span>
          </button>
        </div>
      </div>
    </main>
  );
}
