import { apiClient } from './client';

export interface User {
  id: number;
  email: string;
  full_name: string;
  role: 'super_admin' | 'admin' | 'staff' | 'member';
  is_active: boolean;
  is_verified: boolean;
  phone_number?: string;
  avatar_url?: string;
  created_at: string;
  last_login?: string;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  user: User;
}

export interface LoginData {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
  full_name: string;
  phone_number?: string;
  role?: 'member' | 'staff' | 'admin';
}

export const authApi = {
  async login(data: LoginData): Promise<TokenResponse> {
    const response = await apiClient.post<TokenResponse>('/auth/login', data);
    apiClient.setToken(response.access_token);
    return response;
  },

  async register(data: RegisterData): Promise<User> {
    return apiClient.post<User>('/auth/register', data);
  },

  async getCurrentUser(): Promise<User> {
    return apiClient.get<User>('/auth/me');
  },

  async refreshToken(): Promise<TokenResponse> {
    return apiClient.post<TokenResponse>('/auth/refresh', {});
  },

  logout() {
    apiClient.setToken(null);
  },
};
