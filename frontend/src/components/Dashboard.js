import React from 'react';
import Header from './Header';
import GiveKudos from './GiveKudos';
import KudosList from './KudosList';

const Dashboard = ({ user, onLogout, onUserUpdate }) => {
  return (
    <div className="dashboard">
      <Header user={user} onLogout={onLogout} />
      
      <main className="dashboard-content">
        <div className="dashboard-grid">
          <div className="main-section">
            <GiveKudos 
              currentUser={user} 
              onKudosGiven={onUserUpdate} 
            />
          </div>
          
          <div className="sidebar-section">
            <KudosList />
          </div>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
