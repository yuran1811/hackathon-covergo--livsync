import { Link } from 'react-router';
import {
  User,
  Settings,
  Heart,
  Calendar,
  BarChart3,
  HelpCircle,
  LogOut,
} from 'lucide-react';
import { ScrollArea } from './ui/scroll-area';
import { Separator } from './ui/separator';

interface MenuItem {
  icon: typeof User;
  label: string;
  to?: string;
  onClick?: () => void;
  variant?: 'default' | 'destructive';
}

const menuItems: MenuItem[] = [
  { icon: User, label: 'Profile', to: '/profile' },
  { icon: Heart, label: 'Health Metrics', to: '/health' },
  { icon: Calendar, label: 'Calendar', to: '/calendar' },
  { icon: BarChart3, label: 'Dashboard', to: '/' },
  { icon: Settings, label: 'Settings' },
  { icon: HelpCircle, label: 'Help & Support' },
];

export const MenuPanel = () => {
  const handleLogout = () => {
    console.log('Logout clicked');
    // Add logout logic here
  };

  return (
    <ScrollArea className="mt-6 h-[calc(100vh-8rem)]">
      <div className="space-y-1">
        {menuItems.map((item, index) => {
          const Icon = item.icon;

          if (item.to) {
            return (
              <Link
                key={index}
                to={item.to}
                className="hover:bg-muted flex items-center gap-3 rounded-lg px-4 py-3 transition-colors"
              >
                <div className="bg-wellness-light flex h-10 w-10 items-center justify-center rounded-full">
                  <Icon className="text-wellness h-5 w-5" />
                </div>
                <span className="text-foreground font-medium">
                  {item.label}
                </span>
              </Link>
            );
          }

          return (
            <button
              key={index}
              onClick={item.onClick}
              className="hover:bg-muted flex w-full items-center gap-3 rounded-lg px-4 py-3 transition-colors"
            >
              <div className="bg-wellness-light flex h-10 w-10 items-center justify-center rounded-full">
                <Icon className="text-wellness h-5 w-5" />
              </div>
              <span className="text-foreground font-medium">{item.label}</span>
            </button>
          );
        })}

        <Separator className="my-4" />

        <button
          onClick={handleLogout}
          className="hover:bg-destructive/10 flex w-full items-center gap-3 rounded-lg px-4 py-3 transition-colors"
        >
          <div className="bg-destructive/10 flex h-10 w-10 items-center justify-center rounded-full">
            <LogOut className="text-destructive h-5 w-5" />
          </div>
          <span className="text-destructive font-medium">Sign Out</span>
        </button>
      </div>
    </ScrollArea>
  );
};
