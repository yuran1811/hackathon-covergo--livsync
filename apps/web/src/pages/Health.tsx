import { Header } from '@/components/Header';
import { BottomNav } from '@/components/BottomNav';
import { HealthMetricCard } from '@/components/HealthMetricCard';
import { Heart, Footprints, Moon, Zap, Brain, Dumbbell } from 'lucide-react';
import { Progress } from '@/components/ui/progress';

const Health = () => {
  return (
    <>
      <section>
        <h2 className="text-foreground mb-4 text-lg font-semibold">
          Today's Metrics
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
          <HealthMetricCard
            icon={Brain}
            label="Stress"
            value="Low"
            trend="down"
            variant="wellness"
          />
          <HealthMetricCard
            icon={Dumbbell}
            label="Workouts"
            value="3"
            unit="this week"
            trend="up"
            variant="activity"
          />
        </div>
      </section>

      {/* Daily Goals */}
      <section>
        <h2 className="text-foreground mb-4 text-lg font-semibold">
          Daily Goals
        </h2>
        <div className="bg-card border-border space-y-4 rounded-3xl border p-5">
          <div>
            <div className="mb-2 flex items-center justify-between">
              <span className="text-sm font-medium">Steps Goal</span>
              <span className="text-muted-foreground text-sm">
                6,234 / 10,000
              </span>
            </div>
            <Progress value={62} className="h-2" />
          </div>

          <div>
            <div className="mb-2 flex items-center justify-between">
              <span className="text-sm font-medium">Active Minutes</span>
              <span className="text-muted-foreground text-sm">45 / 60</span>
            </div>
            <Progress value={75} className="h-2" />
          </div>

          <div>
            <div className="mb-2 flex items-center justify-between">
              <span className="text-sm font-medium">Water Intake</span>
              <span className="text-muted-foreground text-sm">5 / 8 cups</span>
            </div>
            <Progress value={62.5} className="h-2" />
          </div>

          <div>
            <div className="mb-2 flex items-center justify-between">
              <span className="text-sm font-medium">Sleep Goal</span>
              <span className="text-muted-foreground text-sm">7.5 / 8 hrs</span>
            </div>
            <Progress value={93.75} className="h-2" />
          </div>
        </div>
      </section>

      {/* Weekly Summary */}
      <section className="from-wellness-light via-activity-light/50 to-energy-light border-wellness/20 rounded-3xl border bg-gradient-to-br p-5">
        <h3 className="text-foreground mb-3 font-semibold">Weekly Summary</h3>
        <div className="grid grid-cols-2 gap-4 text-sm">
          <div>
            <p className="text-muted-foreground">Avg Heart Rate</p>
            <p className="text-wellness text-lg font-bold">68 bpm</p>
          </div>
          <div>
            <p className="text-muted-foreground">Total Steps</p>
            <p className="text-activity text-lg font-bold">42,180</p>
          </div>
          <div>
            <p className="text-muted-foreground">Avg Sleep</p>
            <p className="text-wellness text-lg font-bold">7.3 hrs</p>
          </div>
          <div>
            <p className="text-muted-foreground">Workouts</p>
            <p className="text-energy text-lg font-bold">3 times</p>
          </div>
        </div>
      </section>
    </>
  );
};

export default Health;
