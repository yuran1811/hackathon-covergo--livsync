import { ActivityCard } from '@/components/ActivityCard';
import { HealthMetricCard } from '@/components/HealthMetricCard';
import { Footprints, Heart, Moon, Zap } from 'lucide-react';

const Dashboard = () => {
  return (
    <>
      {/* AI Insights */}
      <section className="from-primary/10 to-secondary/10 border-primary/20 rounded-3xl border bg-gradient-to-r p-5">
        <h3 className="text-foreground mb-2 font-semibold">
          AI Health Insight
        </h3>
        <p className="text-muted-foreground text-sm">
          Your activity level is great today! Consider adding a short evening
          walk to reach your 10,000 steps goal and improve your sleep quality.
        </p>
      </section>

      {/* Health Summary */}
      <section>
        <h2 className="text-foreground mb-4 text-lg font-semibold">
          Today's Health Summary
        </h2>
        <div className="grid grid-cols-2 gap-3">
          <HealthMetricCard
            icon={Heart}
            label="Heart Rate"
            value="72"
            unit="bpm"
            trend="stable"
            variant="wellness"
          />
          <HealthMetricCard
            icon={Footprints}
            label="Steps"
            value="6,234"
            trend="up"
            variant="activity"
          />
          <HealthMetricCard
            icon={Moon}
            label="Sleep"
            value="7.5"
            unit="hrs"
            trend="up"
            variant="wellness"
          />
          <HealthMetricCard
            icon={Zap}
            label="Energy"
            value="85"
            unit="%"
            trend="stable"
            variant="energy"
          />
        </div>
      </section>

      {/* Today's Events */}
      <section>
        <h2 className="text-foreground mb-4 text-lg font-semibold">
          Today's Schedule
        </h2>
        <div className="space-y-3">
          <ActivityCard
            title="Morning Workout"
            time="7:00 AM - 8:00 AM"
            location="Home Gym"
            type="workout"
          />
          <ActivityCard
            title="Team Meeting"
            time="10:00 AM - 11:00 AM"
            location="Conference Room A"
            attendees={5}
            type="meeting"
          />
          <ActivityCard
            title="Lunch Break"
            time="12:30 PM - 1:30 PM"
            type="vacation"
          />
        </div>
      </section>
    </>
  );
};

export default Dashboard;
