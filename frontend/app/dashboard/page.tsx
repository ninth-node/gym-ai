'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/lib/store/auth';
import { membersApi, DashboardStats } from '@/lib/api/members';
import { Navbar } from '@/components/dashboard/navbar';
import { StatCard } from '@/components/dashboard/stat-card';

export default function DashboardPage() {
  const router = useRouter();
  const { user, checkAuth } = useAuthStore();
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const initAuth = async () => {
      await checkAuth();
    };
    initAuth();
  }, [checkAuth]);

  useEffect(() => {
    if (user) {
      loadDashboardStats();
    } else if (!loading) {
      router.push('/auth/login');
    }
  }, [user, router]);

  const loadDashboardStats = async () => {
    try {
      const data = await membersApi.getDashboardStats();
      setStats(data);
      setError('');
    } catch (err: any) {
      setError(err.message || 'Failed to load dashboard stats');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  if (!user) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />

      <main className="max-w-7xl mx-auto px-6 py-8">
        <div className="mb-8">
          <h2 className="text-3xl font-bold mb-2">Dashboard</h2>
          <p className="text-muted-foreground">
            Welcome back, {user.full_name}! Here's what's happening today.
          </p>
        </div>

        {error && (
          <div className="bg-destructive/10 text-destructive p-4 rounded-lg mb-6">
            {error}
          </div>
        )}

        {stats && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <StatCard
              title="Total Members"
              value={stats.total_members}
              icon={
                <svg
                  className="w-6 h-6"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"
                  />
                </svg>
              }
              color="primary"
            />

            <StatCard
              title="Active Members"
              value={stats.active_members}
              icon={
                <svg
                  className="w-6 h-6"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              }
              color="secondary"
            />

            <StatCard
              title="Today's Check-ins"
              value={stats.today_check_ins}
              icon={
                <svg
                  className="w-6 h-6"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
                  />
                </svg>
              }
              color="accent"
            />

            <StatCard
              title="Currently in Gym"
              value={stats.active_check_ins}
              icon={
                <svg
                  className="w-6 h-6"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"
                  />
                </svg>
              }
              color="default"
            />
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold mb-4">Quick Actions</h3>
            <div className="space-y-3">
              <button className="w-full text-left px-4 py-3 rounded-md bg-primary/10 hover:bg-primary/20 transition">
                <p className="font-medium text-primary">Check in Member</p>
                <p className="text-sm text-muted-foreground">
                  Scan QR code or enter member ID
                </p>
              </button>
              <button className="w-full text-left px-4 py-3 rounded-md bg-secondary/10 hover:bg-secondary/20 transition">
                <p className="font-medium text-secondary">Add New Member</p>
                <p className="text-sm text-muted-foreground">
                  Register a new gym member
                </p>
              </button>
              <button className="w-full text-left px-4 py-3 rounded-md bg-accent/10 hover:bg-accent/20 transition">
                <p className="font-medium text-accent">View Reports</p>
                <p className="text-sm text-muted-foreground">
                  Access analytics and insights
                </p>
              </button>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold mb-4">AI Insights</h3>
            <div className="space-y-4">
              <div className="p-4 bg-blue-50 rounded-md border border-blue-100">
                <p className="text-sm font-medium text-blue-900 mb-1">
                  Member Retention
                </p>
                <p className="text-xs text-blue-700">
                  AI detected 3 members at risk of churning this week. Review
                  retention campaigns.
                </p>
              </div>
              <div className="p-4 bg-green-50 rounded-md border border-green-100">
                <p className="text-sm font-medium text-green-900 mb-1">
                  Peak Hours
                </p>
                <p className="text-xs text-green-700">
                  Expected high traffic between 5-7 PM today. Consider
                  additional staff.
                </p>
              </div>
              <div className="p-4 bg-purple-50 rounded-md border border-purple-100">
                <p className="text-sm font-medium text-purple-900 mb-1">
                  Equipment Maintenance
                </p>
                <p className="text-xs text-purple-700">
                  Treadmill #3 requires maintenance in 5 days based on usage
                  patterns.
                </p>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
