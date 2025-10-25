import { Header } from '@/components/Header';
import { BottomNav } from '@/components/BottomNav';
import { useState } from 'react';
import { cn } from '@/lib/utils';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { ActivityCard } from '@/components/ActivityCard';

const Calendar = () => {
  const [currentDate, setCurrentDate] = useState(new Date());
  const [selectedDate, setSelectedDate] = useState(new Date().getDate());

  const daysOfWeek = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
  const monthYear = currentDate.toLocaleDateString('en-US', {
    month: 'long',
    year: 'numeric',
  });

  const getDaysInMonth = () => {
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();
    const firstDay = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();

    const days = [];
    for (let i = 0; i < firstDay; i++) {
      days.push(null);
    }
    for (let i = 1; i <= daysInMonth; i++) {
      days.push(i);
    }
    return days;
  };

  const days = getDaysInMonth();

  return (
    <>
      {/* Calendar Header */}
      <div className="mb-4 flex items-center justify-between">
        <Button
          variant="ghost"
          size="icon"
          className="rounded-full"
          onClick={() =>
            setCurrentDate(
              new Date(currentDate.getFullYear(), currentDate.getMonth() - 1),
            )
          }
        >
          <ChevronLeft className="h-5 w-5" />
        </Button>
        <h2 className="text-lg font-semibold">{monthYear}</h2>
        <Button
          variant="ghost"
          size="icon"
          className="rounded-full"
          onClick={() =>
            setCurrentDate(
              new Date(currentDate.getFullYear(), currentDate.getMonth() + 1),
            )
          }
        >
          <ChevronRight className="h-5 w-5" />
        </Button>
      </div>

      {/* Calendar Grid */}
      <div className="bg-card border-border rounded-3xl border p-4">
        <div className="mb-2 grid grid-cols-7 gap-2">
          {daysOfWeek.map((day) => (
            <div
              key={day}
              className="text-muted-foreground text-center text-xs font-medium"
            >
              {day}
            </div>
          ))}
        </div>
        <div className="grid grid-cols-7 gap-2">
          {days.map((day, index) => (
            <button
              key={index}
              onClick={() => day && setSelectedDate(day)}
              disabled={!day}
              className={cn(
                'flex aspect-square items-center justify-center rounded-xl text-sm font-medium transition-all',
                !day && 'invisible',
                day === selectedDate &&
                  'bg-primary text-primary-foreground shadow-md',
                day !== selectedDate &&
                  day === new Date().getDate() &&
                  'bg-wellness-light text-wellness border-wellness/30 border-2',
                day &&
                  day !== selectedDate &&
                  day !== new Date().getDate() &&
                  'hover:bg-muted text-foreground',
              )}
            >
              {day}
            </button>
          ))}
        </div>
      </div>

      {/* Events for Selected Date */}
      <section>
        <h3 className="text-foreground mb-4 text-lg font-semibold">
          Events on {selectedDate}
        </h3>
        <div className="space-y-3">
          <ActivityCard
            title="Morning Workout"
            time="7:00 AM - 8:00 AM"
            location="Home Gym"
            type="workout"
          />
          <ActivityCard
            title="Team Standup"
            time="9:30 AM - 10:00 AM"
            attendees={8}
            type="meeting"
          />
          <ActivityCard
            title="Afternoon Walk"
            time="3:00 PM - 3:30 PM"
            location="Park"
            type="vacation"
          />
        </div>
      </section>
    </>
  );
};

export default Calendar;
