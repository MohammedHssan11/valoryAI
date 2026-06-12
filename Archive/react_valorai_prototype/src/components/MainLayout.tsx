import { useState } from 'react';
import Home from './Home';
import Valuations from './Valuations';
import Copilot from './Copilot';
import Profile from './Profile';

export default function MainLayout({ onLogout }: { onLogout: () => void }) {
  const [activeTab, setActiveTab] = useState<'home' | 'valuations' | 'copilot' | 'profile'>('home');

  const navItems = [
    { id: 'home', icon: 'dashboard', label: 'Home' },
    { id: 'valuations', icon: 'analytics', label: 'Valuations' },
    { id: 'copilot', icon: 'smart_toy', label: 'Copilot' },
    { id: 'profile', icon: 'person', label: 'Profile' }
  ] as const;

  return (
    <div className="flex-1 flex flex-col w-full h-full relative overflow-hidden bg-backgroundz-10">
      {/* Dynamic Content */}
      <div className="flex-1 overflow-x-hidden relative">
        {activeTab === 'home' && <Home onNavigate={setActiveTab} />}
        {activeTab === 'valuations' && <Valuations />}
        {activeTab === 'copilot' && <Copilot />}
        {activeTab === 'profile' && <Profile onLogout={onLogout} />}
      </div>

      {/* Bottom Nav Bar (Mobile-first Layout) */}
      <nav className="shrink-0 w-full rounded-t-xl border-t border-white/10 shadow-[0_-10px_30px_-10px_rgba(0,216,255,0.15)] bg-surface-container/60 backdrop-blur-2xl z-50 flex justify-around items-center pt-2 pb-6 px-4">
        {navItems.map((item) => {
          const isActive = activeTab === item.id;
          return (
            <button 
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`flex flex-col items-center justify-center transition-all active:scale-90 duration-150 gap-1 w-16 relative ${isActive ? 'text-secondary font-bold' : 'text-on-surface-variant hover:text-secondary-fixed'}`}
            >
              {isActive && (
                <div className="absolute -top-3 w-10 h-1 bg-secondary rounded-full shadow-[0_0_10px_rgba(175,236,255,0.8)]"></div>
              )}
              <span className="material-symbols-outlined text-[24px]" style={{ fontVariationSettings: isActive ? "'FILL' 1" : "'FILL' 0" }}>
                {item.icon}
              </span>
              <span className="font-label-sm text-[10px]">{item.label}</span>
            </button>
          );
        })}
      </nav>
    </div>
  );
}
