import { Button } from '@/components/ui/button';
import { useUserProfile } from '@/hooks/use-user';
import { UserProfile } from '@/shared/types';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import {
  Bell,
  HelpCircle,
  LogOut,
  MessageCircle,
  Settings,
  User,
} from 'lucide-react';

const Profile = () => {
  const menuItems = [
    { icon: User, label: 'Personal Information', onClick: () => {} },
    { icon: Settings, label: 'App Settings', onClick: () => {} },
    { icon: MessageCircle, label: 'Chat', onClick: () => {} },
    { icon: Bell, label: 'Notifications', onClick: () => {} },
    { icon: HelpCircle, label: 'Help & Support', onClick: () => {} },
  ];

  const queryClient = useQueryClient();
  const { status, data, error, isFetching } = useUserProfile();
  if (!isFetching) console.log('🚀 ~ Profile ~ data:', data);

  return (
    <>
      {/* User Profile */}
      <section className="from-wellness to-wellness/80 rounded-3xl bg-gradient-to-br p-6 text-white">
        <div className="flex items-center gap-4">
          <div className="flex h-20 w-20 items-center justify-center rounded-full bg-white/20">
            <User className="h-10 w-10" />
          </div>
          {isFetching ? (
            <div>Loading...</div>
          ) : error ? (
            <div>Error loading profile</div>
          ) : (
            <div>
              <h2 className="text-xl font-bold">
                {data?.full_name || 'John Doe'}
              </h2>
              <p className="text-sm text-white/80">
                {data?.email || 'johndoe@example.com'}
              </p>
            </div>
          )}
        </div>
      </section>

      {/* Menu Items */}
      <section className="bg-card border-border overflow-hidden rounded-3xl border">
        {menuItems.map((item, index) => {
          const Icon = item.icon;
          return (
            <button
              key={index}
              onClick={item.onClick}
              className="hover:bg-muted border-border flex w-full items-center gap-4 border-b p-4 transition-colors last:border-0"
            >
              <div className="bg-wellness-light flex h-10 w-10 items-center justify-center rounded-full">
                <Icon className="text-wellness h-5 w-5" />
              </div>
              <span className="flex-1 text-left font-medium">{item.label}</span>
              <span className="text-muted-foreground">›</span>
            </button>
          );
        })}
      </section>

      {/* Health Goals */}
      <section className="from-activity-light to-energy-light border-activity/20 rounded-3xl border bg-gradient-to-r p-5">
        <h3 className="text-foreground mb-2 font-semibold">
          Your Health Goals
        </h3>
        <ul className="text-muted-foreground space-y-2 text-sm">
          <li>• Walk 10,000 steps daily</li>
          <li>• Sleep 8 hours per night</li>
          <li>• Exercise 3 times per week</li>
          <li>• Maintain healthy heart rate</li>
        </ul>
      </section>

      {/* Logout Button */}
      <Button variant="destructive" className="h-12 w-full rounded-2xl">
        <LogOut className="mr-2 h-4 w-4" />
        Sign Out
      </Button>
    </>
  );
};

export default Profile;
