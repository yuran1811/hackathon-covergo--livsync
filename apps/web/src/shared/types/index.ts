export type UserProfile = {
  id: number;
  full_name: string;
  email: string;
  custom_goals: string;
  activity_level: string;
  step_goal: number;
  dob: Date;
  gender: string;
  weight: number;
  height: number;
};

export interface PushNotification {
  id: string;
  type: 'health' | 'activity' | 'sleep' | 'achievement';
  title: string;
  message: string;
  time: string;
  read: boolean;
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
}
