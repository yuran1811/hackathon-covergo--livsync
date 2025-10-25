import { Clock, MapPin, Users } from 'lucide-react';
import { cn } from '@/lib/utils';

interface ActivityCardProps {
  title: string;
  time: string;
  location?: string;
  attendees?: number;
  type: 'vacation' | 'shift' | 'workout' | 'meeting';
  className?: string;
}

export const ActivityCard = ({
  title,
  time,
  location,
  attendees,
  type,
  className,
}: ActivityCardProps) => {
  const typeStyles = {
    vacation: 'bg-wellness-light border-wellness/30',
    shift: 'bg-activity-light border-activity/30',
    workout: 'bg-energy-light border-energy/30',
    meeting: 'bg-muted border-border',
  };

  return (
    <div
      className={cn(
        'rounded-2xl border-2 p-4 transition-all hover:shadow-md',
        typeStyles[type],
        className,
      )}
    >
      <h3 className="text-foreground mb-3 font-semibold">{title}</h3>
      <div className="space-y-2">
        <div className="text-muted-foreground flex items-center gap-2 text-sm">
          <Clock className="h-4 w-4" />
          <span>{time}</span>
        </div>
        {location && (
          <div className="text-muted-foreground flex items-center gap-2 text-sm">
            <MapPin className="h-4 w-4" />
            <span>{location}</span>
          </div>
        )}
        {attendees && (
          <div className="text-muted-foreground flex items-center gap-2 text-sm">
            <Users className="h-4 w-4" />
            <span>{attendees} people</span>
          </div>
        )}
      </div>
    </div>
  );
};
