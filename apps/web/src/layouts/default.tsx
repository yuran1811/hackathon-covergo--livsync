import { Outlet } from 'react-router';

import { BottomNav } from '@/components/BottomNav';
import { Header } from '@/components/Header';

export default function Layout() {
  const today = new Date().toLocaleDateString('en-US', {
    weekday: 'long',
    month: 'long',
    day: 'numeric',
  });

  return (
    <>
      <div className="from-background to-wellness-light/20 min-h-screen bg-gradient-to-b pb-24">
        <Header title="LivSync" subtitle={today} />

        <main className="mx-auto max-w-md space-y-6 px-4 py-6">
          <Outlet />
        </main>

        <BottomNav />
      </div>
    </>
  );
}
