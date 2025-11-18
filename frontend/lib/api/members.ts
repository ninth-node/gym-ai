import { apiClient } from './client';

export interface DashboardStats {
  total_members: number;
  active_members: number;
  today_check_ins: number;
  active_check_ins: number;
}

export const membersApi = {
  async getDashboardStats(): Promise<DashboardStats> {
    return apiClient.get<DashboardStats>('/members/dashboard/stats');
  },
};
