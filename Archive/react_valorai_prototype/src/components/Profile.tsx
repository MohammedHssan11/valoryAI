import { useState } from 'react';

export default function Profile({ onLogout }: { onLogout: () => void }) {
  const [isLogoutModalOpen, setIsLogoutModalOpen] = useState(false);
  const [isEditProfileModalOpen, setIsEditProfileModalOpen] = useState(false);
  const [userName, setUserName] = useState('Mohammed');
  const [userBio, setUserBio] = useState('Managing premium properties and leveraging AI for precise market valuations.');

  return (
    <main className="flex-1 flex flex-col w-full h-full bg-background relative overflow-y-auto px-4 py-6 pb-24 z-10 hide-scrollbar">
      {/* Header Profile Card */}
      <section className="relative bg-surface-container/30 backdrop-blur-2xl border border-white/10 rounded-2xl p-6 flex flex-col items-center text-center gap-4 group">
        <div className="absolute -inset-1 bg-gradient-to-r from-secondary/10 to-tertiary/10 blur-xl opacity-50 rounded-3xl pointer-events-none"></div>
        <div className="relative w-24 h-24 shrink-0">
          <div className="absolute inset-0 rounded-full border-2 border-secondary/40 shadow-[0_0_30px_-5px_rgba(0,216,255,0.3)] animate-pulse-slow"></div>
          <img src="https://lh3.googleusercontent.com/aida-public/AB6AXuBT1Q_n_eiXVfvUk-TSSJgKK6amh37J3Gl0CexwoFIMnX1iqSTBW_97-_LFxYsbeE4eIgU-gt2KMkvNE-FB4CKcmIkGA9oLx66W0BcDRRg9DoeOXz5zAgYhCxYrhUvVCMN6SFcY1gTONFtn8sBbDqbu8IJJEQEeC5FisQt8IemMYgZA-XPij_4TjISIhm4MlJ6He1MtO2PQfrqm0mjJRL-74Hb_c7CND4WONDT4e_NErhuEnxRDz1CfszJdWv-6aYShgjEmSAMlbqwU" alt="Profile" className="w-full h-full object-cover rounded-full relative z-10" />
          
          <label className="absolute bottom-0 right-0 w-8 h-8 rounded-full bg-surface-container-high border border-white/20 text-secondary z-30 flex items-center justify-center cursor-pointer hover:bg-white/10 transition-colors shadow-lg active:scale-95">
             <input type="file" accept="image/*" capture="user" className="hidden" />
             <span className="material-symbols-outlined text-[16px]">edit</span>
          </label>
        </div>
        <div className="relative z-10 flex-1">
          <h2 className="font-headline-lg text-2xl font-bold text-on-surface mb-1">{userName}</h2>
          <div className="inline-flex items-center gap-1 px-3 py-1 rounded-full bg-secondary/10 border border-secondary/20 mb-2">
            <span className="material-symbols-outlined text-[14px] text-secondary">verified</span>
            <span className="font-label-sm text-[10px] font-bold text-secondary uppercase tracking-wider">Professional Plan</span>
          </div>
          <p className="font-body-md text-sm text-on-surface-variant max-w-sm mx-auto mb-4">{userBio}</p>
          <button onClick={() => setIsEditProfileModalOpen(true)} className="bg-secondary/10 text-secondary border border-secondary/20 font-label-sm text-xs font-bold px-4 py-2 rounded-full flex items-center justify-center gap-2 hover:bg-secondary/20 transition-colors mx-auto">
            <span className="material-symbols-outlined text-[14px]">edit</span>
            Edit Profile
          </button>
        </div>
      </section>

      {/* Stats Board */}
      <section className="grid grid-cols-2 gap-3 mt-6">
        <div className="bg-surface-container-low/60 border border-white/[0.08] rounded-xl p-4 flex flex-col relative overflow-hidden hover:scale-105 transition-transform duration-300">
          <span className="material-symbols-outlined absolute top-3 right-3 text-secondary opacity-20">home_work</span>
          <p className="font-label-sm text-[10px] font-bold text-on-surface-variant uppercase tracking-wide mb-2">Tracked</p>
          <div className="font-headline-lg text-2xl font-extrabold text-on-surface mt-auto">142</div>
        </div>
        <div className="bg-surface-container-low/60 border border-white/[0.08] rounded-xl p-4 flex flex-col relative overflow-hidden hover:scale-105 transition-transform duration-300">
          <span className="material-symbols-outlined absolute top-3 right-3 text-secondary opacity-20">smart_toy</span>
          <p className="font-label-sm text-[10px] font-bold text-on-surface-variant uppercase tracking-wide mb-2">Sessions</p>
          <div className="font-headline-lg text-2xl font-extrabold text-on-surface mt-auto">324</div>
        </div>
      </section>

      {/* Menu Options */}
      <section className="bg-surface-container-low/40 border border-white/[0.05] rounded-2xl overflow-hidden mt-6 divide-y divide-white/[0.05]">
        {[
          { text: 'Account Settings', icon: 'manage_accounts' },
          { text: 'Notifications', icon: 'notifications', badge: '2 new' },
          { text: 'Support & Help', icon: 'support_agent' },
          { text: 'About ValorAI', icon: 'info' }
        ].map(item => (
          <button key={item.text} className="w-full flex items-center justify-between p-4 hover:bg-white/5 transition-colors">
            <div className="flex items-center gap-4">
               <div className="w-10 h-10 rounded-full bg-surface-variant flex items-center justify-center text-on-surface-variant">
                 <span className="material-symbols-outlined text-sm">{item.icon}</span>
               </div>
               <span className="font-body-md text-sm font-semibold">{item.text}</span>
            </div>
            <div className="flex items-center gap-3">
              {item.badge && <span className="text-[10px] font-bold bg-white/10 px-2 py-1 rounded text-on-surface-variant">{item.badge}</span>}
              <span className="material-symbols-outlined text-on-surface-variant text-sm">chevron_right</span>
            </div>
          </button>
        ))}
        <button onClick={() => setIsLogoutModalOpen(true)} className="w-full flex items-center justify-between p-4 hover:bg-error/10 transition-colors">
          <div className="flex items-center gap-4">
             <div className="w-10 h-10 rounded-full bg-error/10 flex items-center justify-center text-error">
               <span className="material-symbols-outlined text-sm">logout</span>
             </div>
             <span className="font-body-md text-sm font-semibold text-error">Logout</span>
          </div>
          <div className="flex items-center gap-3">
            <span className="material-symbols-outlined text-error text-sm">chevron_right</span>
          </div>
        </button>
      </section>

      {/* Version Label */}
      <div className="mt-8 text-center flex flex-col items-center">
         <div className="flex items-center gap-2 bg-white/5 px-4 py-2 rounded-full border border-white/5">
           <span className="material-symbols-outlined text-secondary text-[16px]">call</span>
           <span className="text-xs font-semibold text-on-surface-variant">Support: <span className="text-secondary">01221080473</span></span>
         </div>
         <p className="text-[10px] uppercase tracking-widest text-on-surface-variant/40 mt-4">ValorAI Platform 2.4.1</p>
      </div>

      {/* Logout Confirmation Modal */}
      {isLogoutModalOpen && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-background/80 backdrop-blur-sm animate-[fadeIn_0.2s_ease-out]">
          <div className="bg-surface-container border border-white/10 rounded-2xl p-6 w-full max-w-sm flex flex-col gap-4 shadow-[0_20px_40px_rgba(0,0,0,0.5)] relative overflow-hidden">
            <div className="flex flex-col gap-2">
              <h3 className="font-headline-md text-xl font-bold text-on-surface">Confirm Logout</h3>
              <p className="font-body-md text-sm text-on-surface-variant">
                Are you sure you want to sign out of ValorAI? You will need to sign in again to access your valuations and portfolio.
              </p>
            </div>
            <div className="flex items-center justify-end gap-3 mt-2">
              <button onClick={() => setIsLogoutModalOpen(false)} className="px-5 py-2.5 rounded-full font-label-md text-sm font-bold text-on-surface-variant hover:bg-white/5 transition-colors">
                Cancel
              </button>
              <button onClick={onLogout} className="px-5 py-2.5 rounded-full font-label-md text-sm font-bold bg-error/20 text-error hover:bg-error/30 transition-colors flex items-center gap-2">
                <span className="material-symbols-outlined text-[18px]">logout</span>
                Logout
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Edit Profile Modal */}
      {isEditProfileModalOpen && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-background/80 backdrop-blur-sm animate-[fadeIn_0.2s_ease-out]">
          <div className="bg-surface-container border border-white/10 rounded-2xl p-6 w-full max-w-sm flex flex-col gap-4 shadow-[0_20px_40px_rgba(0,0,0,0.5)] relative overflow-hidden">
            <h3 className="font-headline-md text-xl font-bold text-on-surface">Edit Profile</h3>
            <div className="flex flex-col gap-4">
              <div className="relative group flex flex-col gap-1">
                <label className="font-label-sm text-on-surface-variant text-xs">Full Name</label>
                <div className="relative">
                  <span className="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-on-surface-variant/50 text-[18px]">person</span>
                  <input type="text" value={userName} onChange={e => setUserName(e.target.value)} className="w-full bg-surface-container-lowest text-on-surface text-sm pl-10 pr-4 py-2.5 rounded-lg border border-white/10 focus:border-secondary-container focus:outline-none transition-colors" />
                </div>
              </div>
              <div className="relative group flex flex-col gap-1">
                <label className="font-label-sm text-on-surface-variant text-xs">Bio</label>
                <textarea rows={3} value={userBio} onChange={e => setUserBio(e.target.value)} className="w-full bg-surface-container-lowest text-on-surface text-sm p-3 rounded-lg border border-white/10 focus:border-secondary-container focus:outline-none transition-colors resize-none" />
              </div>
            </div>
            <div className="flex items-center justify-end gap-3 mt-2">
              <button onClick={() => setIsEditProfileModalOpen(false)} className="px-5 py-2.5 rounded-full font-label-md text-sm font-bold text-on-surface-variant hover:bg-white/5 transition-colors">
                Cancel
              </button>
              <button onClick={() => setIsEditProfileModalOpen(false)} className="px-5 py-2.5 rounded-full font-label-md text-sm font-bold bg-secondary-container text-on-secondary-fixed hover:bg-secondary-fixed transition-colors">
                Save Changes
              </button>
            </div>
          </div>
        </div>
      )}
    </main>
  );
}
