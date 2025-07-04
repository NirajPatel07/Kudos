import React, { useState, useEffect, useCallback } from 'react';
import { getReceivedKudos, getGivenKudos } from '../services/api';

const KudosList = () => {
  const [activeTab, setActiveTab] = useState('received');
  const [receivedKudos, setReceivedKudos] = useState([]);
  const [givenKudos, setGivenKudos] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const loadKudos = useCallback(async () => {
    setLoading(true);
    setError('');

    try {
      if (activeTab === 'received') {
        const data = await getReceivedKudos();
        setReceivedKudos(data);
      } else {
        const data = await getGivenKudos();
        setGivenKudos(data);
      }
    } catch (err) {
      setError('Failed to load kudos');
    } finally {
      setLoading(false);
    }
  }, [activeTab]);

  useEffect(() => {
    loadKudos();
  }, [loadKudos]);

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      weekday: 'short',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const renderKudosItem = (kudo) => {
    const isReceived = activeTab === 'received';
    const person = isReceived ? kudo.giver : kudo.receiver;
    const personName = person.first_name && person.last_name 
      ? `${person.first_name} ${person.last_name}` 
      : person.username;

    return (
      <div key={kudo.id} className="kudos-item">
        <div className="kudos-header">
          <span className="person-name">
            {isReceived ? `From ${personName}` : `To ${personName}`}
          </span>
          <span className="kudos-date">{formatDate(kudo.created_at)}</span>
        </div>
        <div className="kudos-message">{kudo.message}</div>
      </div>
    );
  };

  const currentKudos = activeTab === 'received' ? receivedKudos : givenKudos;

  return (
    <div className="kudos-list-section">
      <div className="kudos-tabs">
        <button 
          className={`tab ${activeTab === 'received' ? 'active' : ''}`}
          onClick={() => setActiveTab('received')}
        >
          Received ({receivedKudos.length})
        </button>
        <button 
          className={`tab ${activeTab === 'given' ? 'active' : ''}`}
          onClick={() => setActiveTab('given')}
        >
          Given ({givenKudos.length})
        </button>
      </div>

      <div className="kudos-content">
        {loading && <div className="loading">Loading...</div>}
        {error && <div className="error-message">{error}</div>}
        
        {!loading && !error && (
          <>
            {currentKudos.length === 0 ? (
              <div className="no-kudos">
                <p>
                  {activeTab === 'received' 
                    ? "You haven't received any kudos yet. Keep up the great work!"
                    : "You haven't given any kudos yet. Spread some appreciation!"}
                </p>
              </div>
            ) : (
              <div className="kudos-items">
                {currentKudos.map(renderKudosItem)}
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default KudosList;
