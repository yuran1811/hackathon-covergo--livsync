import { createAsyncStoragePersister } from '@tanstack/query-async-storage-persister';
import { QueryClient } from '@tanstack/react-query';
import { PersistQueryClientProvider } from '@tanstack/react-query-persist-client';
import { BrowserRouter, Route, Routes } from 'react-router';

import { Toaster as Sonner } from '@/components/ui/sonner';
import { Toaster } from '@/components/ui/toaster';
import { TooltipProvider } from '@/components/ui/tooltip';
import DefaultLayout from './layouts/default';
import Index from './pages';
import Auth from './pages/Auth';
import Calendar from './pages/Calendar';
import Dashboard from './pages/Dashboard';
import Health from './pages/Health';
import NotFound from './pages/NotFound';
import Profile from './pages/Profile';
import { useEffect } from 'react';
import { pushNotification } from './lib/utils';
import { supabase } from './integrations/supabase/client';
import { useNotifs } from './store';

const queryClient = new QueryClient({});

const persister = createAsyncStoragePersister({
  storage: window.localStorage,
});

const notifChannel = supabase.channel('event-changes');

const messageReceived = (payload: any) => {
  pushNotification({
    title: payload?.suggestion?.title || 'New Notification',
    body: `${payload?.suggestion?.description}\n(${payload?.suggestion?.rationale || 'No additional info'})`,
  });
};

const App = () => {
  const addNotification = useNotifs((state) => state.addNotification);

  useEffect(() => {
    const registerServiceWorker = async () => {
      const permission = await Notification.requestPermission();
    };

    registerServiceWorker().then(console.log);

    notifChannel
      .on('broadcast', { event: 'shout' }, ({ payload }) => {
        messageReceived(payload);

        addNotification({
          id: Date.now().toString(),
          type: 'activity',
          title: payload?.suggestion?.title || 'New Notification',
          message: payload?.suggestion?.description || '',
          time: 'Just now',
          read: false,
        });
      })
      .subscribe();
  }, []);

  return (
    <PersistQueryClientProvider
      client={queryClient}
      persistOptions={{ persister }}
    >
      <TooltipProvider>
        <Toaster />
        <Sonner />
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<Index />} />
            <Route path="/auth" element={<Auth />} />
            <Route element={<DefaultLayout />}>
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/calendar" element={<Calendar />} />
              <Route path="/health" element={<Health />} />
              <Route path="/profile" element={<Profile />} />
            </Route>
            <Route path="*" element={<NotFound />} />
          </Routes>
        </BrowserRouter>
      </TooltipProvider>
    </PersistQueryClientProvider>
  );
};

export default App;
