import React, { useState, useEffect, useCallback } from 'react';
import { getOrganizationUsers, giveKudos } from '../services/api';

const GiveKudos = ({ currentUser, onKudosGiven }) => {
  const [users, setUsers] = useState([]);
  const [selectedUser, setSelectedUser] = useState('');
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const loadUsers = useCallback(async () => {
    try {
      const data = await getOrganizationUsers();
      // Filter out current user
      const otherUsers = data.filter(user => user.id !== currentUser.id);
      setUsers(otherUsers);
    } catch (err) {
      setError('Failed to load users');
    }
  }, [currentUser.id]);

  useEffect(() => {
    loadUsers();
  }, [loadUsers]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedUser || !message.trim()) {
      setError('Please select a user and enter a message');
      return;
    }

    setLoading(true);
    setError('');
    setSuccess('');

    try {
      await giveKudos(selectedUser, message.trim());
      setSuccess('Kudos sent successfully!');
      setSelectedUser('');
      setMessage('');
      onKudosGiven(); // Refresh user data
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to send kudos');
    } finally {
      setLoading(false);
    }
  };

  if (currentUser.kudos_available === 0) {
    return (
      <div className="give-kudos-section">
        <h3>Give Kudos</h3>
        <div className="no-kudos-message">
          <p>You've used all your kudos for this week!</p>
          <p>Kudos reset every Monday. Come back next week to spread more appreciation!</p>
        </div>
      </div>
    );
  }

  return (
    <div className="give-kudos-section">
      <h3>Give Kudos ({currentUser.kudos_available} remaining)</h3>
      
      <form onSubmit={handleSubmit} className="kudos-form">
        {error && <div className="error-message">{error}</div>}
        {success && <div className="success-message">{success}</div>}
        
        <div className="form-group">
          <label htmlFor="recipient">Send kudos to:</label>
          <select
            id="recipient"
            value={selectedUser}
            onChange={(e) => setSelectedUser(e.target.value)}
            required
            disabled={loading}
          >
            <option value="">Select a colleague...</option>
            {users.map(user => (
              <option key={user.id} value={user.id}>
                {user.first_name && user.last_name 
                  ? `${user.first_name} ${user.last_name}` 
                  : user.username}
              </option>
            ))}
          </select>
        </div>
        
        <div className="form-group">
          <label htmlFor="message">Your message:</label>
          <textarea
            id="message"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Write why this person deserves kudos..."
            required
            disabled={loading}
            rows={4}
          />
        </div>
        
        <button type="submit" disabled={loading || !selectedUser || !message.trim()}>
          {loading ? 'Sending...' : 'Send Kudos'}
        </button>
      </form>
    </div>
  );
};

export default GiveKudos;
