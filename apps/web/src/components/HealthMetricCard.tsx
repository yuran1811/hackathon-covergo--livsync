import { LucideIcon } from 'lucide-react';
import { cn } from '@/lib/utils';

interface HealthMetricCardProps {
  icon: LucideIcon;
  label: string;
  value: string;
  unit?: string;
  trend?: 'up' | 'down' | 'stable';
  variant?: 'wellness' | 'activity' | 'energy';
}

export const HealthMetricCard = ({
  icon: Icon,
  label,
  value,
  unit,
  trend,
  variant = 'wellness',
}: HealthMetricCardProps) => {
  const variantStyles = {
    wellness: 'bg-wellness-light text-wellness border-wellness/20',
    activity: 'bg-activity-light text-activity border-activity/20',
    energy: 'bg-energy-light text-energy border-energy/20',
  };

  return (
    <div
      className={cn(
        'rounded-2xl border-2 p-4 transition-all hover:shadow-md',
        variantStyles[variant],
      )}
    >
      <div className="mb-3 flex items-start justify-between">
        <div className="bg-card/80 rounded-xl p-2">
          <Icon className="h-5 w-5" />
        </div>
        {trend && (
          <div className="text-xs font-medium">
            {trend === 'up' ? '↑' : trend === 'down' ? '↓' : '→'}
          </div>
        )}
      </div>
      <div className="space-y-1">
        <p className="text-sm font-medium opacity-80">{label}</p>
        <div className="flex items-baseline gap-1">
          <span className="text-2xl font-bold">{value}</span>
          {unit && <span className="text-sm opacity-70">{unit}</span>}
        </div>
      </div>
    </div>
  );
};
