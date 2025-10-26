import { UserProfile } from '@/shared/types';
import { useQuery } from '@tanstack/react-query';

export function useUserProfile() {
  return useQuery({
    queryKey: ['userProfile'],
    queryFn: async (): Promise<UserProfile> => {
      const response = await fetch(
        import.meta.env.VITE_API_URL +
          '/users/7e0d54d0-e609-4f0c-be79-d850812bf788',
      );
      return await response.json();
    },
  });
}
