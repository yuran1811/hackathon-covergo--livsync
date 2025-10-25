import { Activity, Heart, Moon, TrendingUp } from 'lucide-react';
import { ScrollArea } from './ui/scroll-area';

interface Notification {
  id: string;
  type: 'health' | 'activity' | 'sleep' | 'achievement';
  title: string;
  message: string;
  time: string;
  read: boolean;
}

const notifications: Notification[] = [
  {
    id: '1',
    type: 'health',
    title: 'Heart Rate Alert',
    message: 'Your resting heart rate is lower than usual today. Great job!',
    time: '2 hours ago',
    read: false,
  },
  {
    id: '2',
    type: 'activity',
    title: 'Step Goal Achieved',
    message: "You've reached 10,000 steps today! Keep it up!",
    time: '5 hours ago',
    read: false,
  },
  {
    id: '3',
    type: 'sleep',
    title: 'Sleep Quality',
    message: 'Your sleep quality was excellent last night - 8.5 hours of rest.',
    time: '1 day ago',
    read: true,
  },
  {
    id: '4',
    type: 'achievement',
    title: 'Weekly Streak',
    message: "7 days in a row! You're on fire!",
    time: '2 days ago',
    read: true,
  },
];

const iconMap = {
  health: Heart,
  activity: Activity,
  sleep: Moon,
  achievement: TrendingUp,
};

const colorMap = {
  health: 'text-wellness',
  activity: 'text-activity',
  sleep: 'text-energy',
  achievement: 'text-primary',
};

export const NotificationPanel = () => {
  return (
    <ScrollArea className="mt-6 h-[calc(100vh-8rem)]">
      <div className="space-y-3">
        {notifications.map((notification) => {
          const Icon = iconMap[notification.type];
          const iconColor = colorMap[notification.type];

          return (
            <div
              key={notification.id}
              className={`rounded-xl border p-4 transition-colors ${
                notification.read
                  ? 'bg-card border-border'
                  : 'bg-muted/50 border-primary/20'
              }`}
            >
              <div className="flex gap-3">
                <div
                  className={`bg-muted flex h-10 w-10 items-center justify-center rounded-full ${iconColor}`}
                >
                  <Icon className="h-5 w-5" />
                </div>
                <div className="flex-1">
                  <h4 className="text-foreground text-sm font-semibold">
                    {notification.title}
                  </h4>
                  <p className="text-muted-foreground mt-1 text-sm">
                    {notification.message}
                  </p>
                  <p className="text-muted-foreground mt-2 text-xs">
                    {notification.time}
                  </p>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </ScrollArea>
  );
};
