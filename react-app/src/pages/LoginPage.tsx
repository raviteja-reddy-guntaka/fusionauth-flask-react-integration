import React, { useEffect } from 'react';
import { useAuth } from '../auth/AuthProvider';
import { useNavigate } from 'react-router-dom';

const LoginPage: React.FC = () => {
  const { user, isLoading } = useAuth();
  const navigate = useNavigate();

  // If the user is already logged in, redirect to the dashboard
  useEffect(() => {
    if (!isLoading && user) {
      navigate('/dashboard');
    }
  }, [user, isLoading, navigate]);

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col justify-center">
      <div className="text-center">
        <a 
          href="http://localhost:5001/auth/login"
          className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700"
        >
          Sign in with FusionAuth
        </a>
        <div className="mt-4">
          <a 
            href="http://localhost:5001/auth/register"
            className="text-blue-600 hover:underline"
          >
            Create new account
          </a>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
