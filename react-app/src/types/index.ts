// src/types/index.ts
export interface User {
    user_id: number;
    email: string;
    first_name?: string | null;
    last_name?: string | null;
  }

  export interface AuthContextType {
    user: User | null;
    isAuthenticated: boolean;
    isLoading: boolean;
    login: (token: string, user: User) => void;
    logout: () => Promise<void>;
    checkAuth: () => Promise<void>;
  }
  