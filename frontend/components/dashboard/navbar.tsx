'use client';

import { useAuthStore } from '@/lib/store/auth';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';

export function Navbar() {
  const { user, logout } = useAuthStore();
  const router = useRouter();

  const handleLogout = () => {
    logout();
    router.push('/auth/login');
  };

  return (
    <nav className="bg-white border-b border-gray-200 px-6 py-4">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold bg-gradient-to-r from-primary via-accent to-secondary bg-clip-text text-transparent">
            AI Gym Management
          </h1>
        </div>
        <div className="flex items-center gap-4">
          {user && (
            <>
              <div className="text-sm">
                <p className="font-medium">{user.full_name}</p>
                <p className="text-muted-foreground capitalize">
                  {user.role.replace('_', ' ')}
                </p>
              </div>
              <Button onClick={handleLogout} variant="outline" size="sm">
                Logout
              </Button>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}
