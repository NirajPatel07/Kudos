import React from 'react';
import { logout } from '../services/api';

const Header = ({ user, onLogout }) => {
  const handleLogout = async () => {
    try {
      await logout();
      onLogout();
    } catch (err) {
      console.error('Logout error:', err);
      // Force logout on frontend even if backend fails
      onLogout();
    }
  };

  return (
    <header className="app-header">
      <div className="header-content">
        <h1>Kudos</h1>
        
        <div className="user-info">
          <div className="user-details">
            <span className="username">Hello, {user.first_name || user.username}!</span>
            <span className="organization">{user.organization.name}</span>
            <span className="kudos-count">
              {user.kudos_available} kudos remaining this week
            </span>
          </div>
          
          <button onClick={handleLogout} className="logout-button">
            Sign Out
          </button>
        </div>
      </div>
    </header>
  );
};

export default Header;
