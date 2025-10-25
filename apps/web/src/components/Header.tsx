import { Bell, Menu } from 'lucide-react';
import { Button } from './ui/button';
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from './ui/sheet';
import { NotificationPanel } from './NotificationPanel';
import { MenuPanel } from './MenuPanel';
import { useState } from 'react';

interface HeaderProps {
  title?: string;
  subtitle?: string;
}

export const Header = ({ title = 'HealthFlow', subtitle }: HeaderProps) => {
  const [notificationsOpen, setNotificationsOpen] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <header className="bg-card border-border sticky top-0 z-40 border-b">
      <div className="mx-auto max-w-md px-4 py-4">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-foreground text-xl font-bold">{title}</h1>
            {subtitle && (
              <p className="text-muted-foreground text-sm">{subtitle}</p>
            )}
          </div>
          <div className="flex items-center gap-2">
            <Sheet open={notificationsOpen} onOpenChange={setNotificationsOpen}>
              <SheetTrigger asChild>
                <Button
                  variant="ghost"
                  size="icon"
                  className="relative rounded-full"
                >
                  <Bell className="h-5 w-5" />
                  <span className="bg-destructive absolute right-1 top-1 h-2 w-2 rounded-full" />
                </Button>
              </SheetTrigger>
              <SheetContent>
                <SheetHeader>
                  <SheetTitle>Notifications</SheetTitle>
                  <p className="text-center italic">Mark all as read</p>
                </SheetHeader>
                <NotificationPanel />
              </SheetContent>
            </Sheet>

            <Sheet open={menuOpen} onOpenChange={setMenuOpen}>
              <SheetTrigger asChild>
                <Button variant="ghost" size="icon" className="rounded-full">
                  <Menu className="h-5 w-5" />
                </Button>
              </SheetTrigger>
              <SheetContent>
                <SheetHeader>
                  <SheetTitle>Menu</SheetTitle>
                </SheetHeader>
                <MenuPanel />
              </SheetContent>
            </Sheet>
          </div>
        </div>
      </div>
    </header>
  );
};
