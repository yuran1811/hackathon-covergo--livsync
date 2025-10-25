import { Sparkles, Plus, X } from 'lucide-react';
import { Button } from './ui/button';
import { useState } from 'react';
import { cn } from '@/lib/utils';

interface Suggestion {
  id: string;
  activity: string;
  time: string;
  duration: string;
  reason: string;
}

const mockSuggestions: Suggestion[] = [
  {
    id: '1',
    activity: 'Morning Yoga',
    time: '7:00 AM',
    duration: '30 min',
    reason: 'Based on your stress level and sleep quality',
  },
  {
    id: '2',
    activity: 'Walking Break',
    time: '2:30 PM',
    duration: '15 min',
    reason: "You've been inactive for 3 hours",
  },
  {
    id: '3',
    activity: 'Evening Meditation',
    time: '8:00 PM',
    duration: '20 min',
    reason: 'Helps improve sleep quality',
  },
];

export const AISuggestionPanel = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [suggestions, setSuggestions] = useState<Suggestion[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const generateSuggestions = () => {
    setIsLoading(true);
    setTimeout(() => {
      setSuggestions(mockSuggestions);
      setIsLoading(false);
      setIsOpen(true);
    }, 1500);
  };

  const addToCalendar = (id: string) => {
    setSuggestions(suggestions.filter((s) => s.id !== id));
  };

  if (!isOpen && suggestions.length === 0) {
    return (
      <div className="fixed bottom-24 right-4 z-40">
        <Button
          onClick={generateSuggestions}
          disabled={isLoading}
          className="shadow-elevated from-primary to-primary/80 h-14 w-14 rounded-full bg-gradient-to-r transition-all hover:shadow-lg"
        >
          {isLoading ? (
            <div className="h-5 w-5 animate-spin rounded-full border-2 border-white/30 border-t-white" />
          ) : (
            <Sparkles className="h-6 w-6" />
          )}
        </Button>
      </div>
    );
  }

  if (!isOpen) return null;

  return (
    <div className="fixed inset-x-0 bottom-24 z-40 px-4">
      <div className="bg-card border-border shadow-elevated mx-auto max-w-md space-y-4 rounded-3xl border p-5">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Sparkles className="text-primary h-5 w-5" />
            <h3 className="text-foreground font-semibold">AI Suggestions</h3>
          </div>
          <Button
            variant="ghost"
            size="icon"
            className="rounded-full"
            onClick={() => setIsOpen(false)}
          >
            <X className="h-4 w-4" />
          </Button>
        </div>

        <div className="space-y-3">
          {suggestions.map((suggestion) => (
            <div
              key={suggestion.id}
              className="bg-wellness-light/50 border-wellness/20 space-y-2 rounded-2xl border p-4"
            >
              <div className="flex items-start justify-between">
                <div>
                  <h4 className="text-foreground font-semibold">
                    {suggestion.activity}
                  </h4>
                  <p className="text-muted-foreground text-sm">
                    {suggestion.time} • {suggestion.duration}
                  </p>
                </div>
                <Button
                  size="icon"
                  variant="ghost"
                  className="bg-primary/10 hover:bg-primary/20 text-primary h-8 w-8 rounded-full"
                  onClick={() => addToCalendar(suggestion.id)}
                >
                  <Plus className="h-4 w-4" />
                </Button>
              </div>
              <p className="text-muted-foreground text-xs">
                {suggestion.reason}
              </p>
            </div>
          ))}
        </div>

        <Button
          variant="ghost"
          className="w-full"
          onClick={() => setIsOpen(false)}
        >
          Close
        </Button>
      </div>
    </div>
  );
};
