import React, { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { User, AuthContextType } from '../types';

const AuthContext = createContext<AuthContextType>({} as AuthContextType);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const checkAuth = async () => {
    try {
      const response = await fetch('http://localhost:5001/auth/api/me', {
        method: 'GET',
        credentials: 'include'
      });

      if (response.ok) {
        const userData: User = await response.json();
        setUser(userData);
      } else {
        setUser(null);
      }
    } catch (error) {
      console.error('Auth check failed:', error);
      setUser(null);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    checkAuth();
  }, []);

  const login = (token: string, user: User) => {
    setUser(user);
  };

  const logout = async () => {
    try {
      await fetch('http://localhost:5001/auth/logout', {
        method: 'POST',
        credentials: 'include'
      });
      // Manually delete FusionAuth cookies from the browser
      document.cookie = "fusionauth.session=; path=/; domain=localhost; expires=Thu, 01 Jan 1970 00:00:00 UTC;";
      document.cookie = "fusionauth.remember-device=; path=/; domain=localhost; expires=Thu, 01 Jan 1970 00:00:00 UTC;";
    } catch (error) {
      console.error('Logout failed:', error);
    } finally {
      // Clear local storage and state
      localStorage.clear();
      sessionStorage.clear();
      setUser(null);
      // Force full page reload to clear any cach ed state
      window.location.href = '/login';
    }
  };

  return (
    <AuthContext.Provider value={{
      user,
      isAuthenticated: !!user,
      isLoading,
      login,
      logout,
      checkAuth // Add this to allow re-checking auth status
    }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
