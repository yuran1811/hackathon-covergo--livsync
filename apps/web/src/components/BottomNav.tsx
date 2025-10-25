import { Home, Calendar, Activity, User, MessageCircle } from 'lucide-react';
import { Link, useLocation } from 'react-router';
import { cn } from '@/lib/utils';
import { FloatingChatButton } from './FloatingChatButton';

const navItems = [
  { icon: Home, label: 'Home', path: '/dashboard' },
  { icon: Calendar, label: 'Calendar', path: '/calendar' },
  { icon: MessageCircle, label: 'Chat', path: '/chat' },
  { icon: Activity, label: 'Health', path: '/health' },
  { icon: User, label: 'Profile', path: '/profile' },
];

export const BottomNav = () => {
  const location = useLocation();

  return (
    <nav className="bg-card border-border fixed bottom-0 left-0 right-0 z-50 border-t">
      <div className="mx-auto max-w-md px-4 py-2">
        <div className="flex items-center justify-around">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path;

            if (item.label === 'Chat') {
              return <FloatingChatButton key={item.path} />;
            }

            return (
              <Link
                key={item.path}
                to={item.path}
                className={cn(
                  'flex flex-col items-center gap-1 rounded-xl px-4 py-2 transition-all',
                  isActive
                    ? 'text-primary'
                    : 'text-muted-foreground hover:text-foreground',
                )}
              >
                <Icon
                  className={cn('h-5 w-5', isActive && 'fill-primary/20')}
                />
                <span className="text-xs font-medium">{item.label}</span>
              </Link>
            );
          })}
        </div>
      </div>
    </nav>
  );
};
