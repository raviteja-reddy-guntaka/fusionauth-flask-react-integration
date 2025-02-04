import React from 'react';
import { useAuth } from '../auth/AuthProvider';
import { Link } from 'react-router-dom';

const Dashboard = () => {
  const { user, logout } = useAuth();

  return (
    <div className="dashboard-container">
      <nav>
        <Link to="/">Home</Link>
        <button onClick={logout}>Logout</button>
      </nav>
      
      <h1>Welcome, {user?.email}</h1>
      
      <div className="user-profile">
        {user && (
          <>
            <p>User ID: {user.user_id}</p>
            {user.first_name && <p>First Name: {user.first_name}</p>}
            {user.last_name && <p>Last Name: {user.last_name}</p>}
          </>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
