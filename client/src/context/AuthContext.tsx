import React, { createContext, useContext, useState, useEffect } from 'react';
import type { User } from '../types';
import { authApi } from '../services/api';

interface AuthContextType {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  loginWithGoogle: (credential: string) => Promise<void>;
  loginDemo: () => Promise<void>;
  logout: () => void;
  refreshProfile: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(localStorage.getItem('reachinbox_token'));
  const [isLoading, setIsLoading] = useState<boolean>(true);

  useEffect(() => {
    async function loadUser() {
      if (token) {
        try {
          const profile = await authApi.getProfile();
          setUser(profile);
        } catch (err) {
          console.error('Failed to load profile:', err);
          logout();
        }
      }
      setIsLoading(false);
    }
    loadUser();
  }, [token]);

  const loginWithGoogle = async (credential: string) => {
    setIsLoading(true);
    try {
      const data = await authApi.loginWithGoogle(credential);
      localStorage.setItem('reachinbox_token', data.token);
      setToken(data.token);
      setUser(data.user);
    } finally {
      setIsLoading(false);
    }
  };

  const loginDemo = async () => {
    setIsLoading(true);
    try {
      const data = await authApi.demoLogin();
      localStorage.setItem('reachinbox_token', data.token);
      setToken(data.token);
      setUser(data.user);
    } finally {
      setIsLoading(false);
    }
  };

  const logout = () => {
    localStorage.removeItem('reachinbox_token');
    setToken(null);
    setUser(null);
  };

  const refreshProfile = async () => {
    try {
      const profile = await authApi.getProfile();
      setUser(profile);
    } catch (err) {
      console.error('Failed to refresh profile:', err);
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        isLoading,
        loginWithGoogle,
        loginDemo,
        logout,
        refreshProfile,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
