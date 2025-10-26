import { Button } from '@/components/ui/button';
import { Link } from 'react-router';
import { Activity, Heart, Calendar, Sparkles, CloudCog } from 'lucide-react';
import { useEffect, useState } from 'react';

const Index = () => {
  return (
    <div className="from-background via-background to-primary/5 min-h-screen bg-gradient-to-b">
      {/* Header */}
      <header className="container mx-auto flex items-center justify-between px-4 py-6">
        <div className="flex items-center gap-2">
          <div className="from-primary to-accent flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br">
            <Sparkles className="h-6 w-6 text-white" />
          </div>
          <span className="from-primary to-accent bg-gradient-to-r bg-clip-text text-2xl font-bold text-transparent">
            LivSync
          </span>
        </div>
        <Link to="/auth">
          <Button variant="outline">Sign In</Button>
        </Link>
      </header>

      {/* Hero Section */}
      <main className="container mx-auto px-4 py-16 md:py-24">
        <div className="mx-auto max-w-4xl space-y-8 text-center">
          <div className="bg-primary/10 text-primary mb-4 inline-flex items-center gap-2 rounded-full px-4 py-2">
            <Sparkles className="h-4 w-4" />
            <span className="text-sm font-medium">
              AI-Powered Health Assistant
            </span>
          </div>

          <h1 className="text-4xl font-bold leading-tight md:text-6xl">
            Your Personal Health
            <span className="from-primary via-accent to-secondary bg-gradient-to-r bg-clip-text text-transparent">
              {' '}
              Assistant{' '}
            </span>
            for Better Living
          </h1>

          <p className="text-muted-foreground mx-auto max-w-2xl text-lg md:text-xl">
            Track your health metrics, plan your day smartly, and get AI-powered
            suggestions to optimize your wellness routine.
          </p>

          <div className="flex flex-col justify-center gap-4 pt-4 sm:flex-row">
            <Link to="/auth">
              <Button size="lg" className="w-full sm:w-auto">
                Get Started Free
              </Button>
            </Link>
            <Link to="/auth">
              <Button size="lg" variant="outline" className="w-full sm:w-auto">
                Learn More
              </Button>
            </Link>
          </div>
        </div>

        {/* Features Grid */}
        <div className="mx-auto mt-24 grid max-w-5xl gap-6 md:grid-cols-3">
          <div className="bg-card border-border hover:border-primary/50 rounded-2xl border p-6 transition-all">
            <div className="bg-primary/10 mb-4 flex h-12 w-12 items-center justify-center rounded-xl">
              <Heart className="text-primary h-6 w-6" />
            </div>
            <h3 className="mb-2 text-xl font-semibold">Health Tracking</h3>
            <p className="text-muted-foreground">
              Monitor heart rate, sleep quality, stress levels, and activity
              metrics in real-time.
            </p>
          </div>

          <div className="bg-card border-border hover:border-accent/50 rounded-2xl border p-6 transition-all">
            <div className="bg-accent/10 mb-4 flex h-12 w-12 items-center justify-center rounded-xl">
              <Calendar className="text-accent h-6 w-6" />
            </div>
            <h3 className="mb-2 text-xl font-semibold">Smart Planning</h3>
            <p className="text-muted-foreground">
              AI adapts your schedule based on your health data and suggests
              optimal activity times.
            </p>
          </div>

          <div className="bg-card border-border hover:border-secondary/50 rounded-2xl border p-6 transition-all">
            <div className="bg-secondary/10 mb-4 flex h-12 w-12 items-center justify-center rounded-xl">
              <Activity className="text-secondary h-6 w-6" />
            </div>
            <h3 className="mb-2 text-xl font-semibold">Activity Insights</h3>
            <p className="text-muted-foreground">
              Get personalized recommendations to improve your daily routine and
              overall wellness.
            </p>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-border container mx-auto mt-24 border-t px-4 py-8">
        <div className="text-muted-foreground text-center text-sm">
          © 2025 HealthFlow. Your journey to better health starts here.
        </div>
      </footer>
    </div>
  );
};

export default Index;
