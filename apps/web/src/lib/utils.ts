import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export const pushNotification = ({
  title = 'New Notification',
  body = 'You have a new notification.',
}) => {
  if (Notification.permission === 'granted') {
    new Notification(title, { body });
  } else {
    console.log('Notification permission not granted.');
    Notification.requestPermission().then((permission) => {
      if (permission === 'granted') {
        new Notification(title, { body });
      }
    });
  }
};
