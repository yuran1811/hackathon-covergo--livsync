import { ChatMessage, PushNotification } from '@/shared/types';
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';

export const useNotifs = create<{
  notifications: PushNotification[];
  addNotification: (notification: PushNotification) => void;
  clearNotifications: () => void;

  chatMessages: ChatMessage[];
  addChatMessage: (message: ChatMessage) => void;
  clearChatMessages: () => void;
}>()(
  persist(
    (set) => ({
      notifications: [],
      addNotification: (notification) =>
        set((state) => ({
          notifications: [...state.notifications, notification],
        })),
      clearNotifications: () => set({ notifications: [] }),

      chatMessages: [],
      addChatMessage: (message) =>
        set((state) => ({
          chatMessages: [...state.chatMessages, message],
        })),
      clearChatMessages: () => set({ chatMessages: [] }),
    }),
    {
      name: 'healthAppNotifs',
      storage: createJSONStorage(() => sessionStorage),
    },
  ),
);
