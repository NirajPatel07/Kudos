const API_BASE_URL = 'http://localhost:8000/api';

// Login function
export const login = async (username, password) => {
  const response = await fetch(`${API_BASE_URL}/auth/login/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include',
    body: JSON.stringify({ username, password }),
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.error || 'Login failed');
  }
  
  return response.json();
};

// Logout function
export const logout = async () => {
  const response = await fetch(`${API_BASE_URL}/auth/logout/`, {
    method: 'POST',
    credentials: 'include',
  });
  
  if (!response.ok) {
    throw new Error('Logout failed');
  }
  
  return response.json();
};

// Get current user
export const getCurrentUser = async () => {
  const response = await fetch(`${API_BASE_URL}/auth/me/`, {
    credentials: 'include',
  });
  
  if (!response.ok) {
    throw new Error('Failed to get current user');
  }
  
  return response.json();
};

// Get organization users
export const getOrganizationUsers = async () => {
  const response = await fetch(`${API_BASE_URL}/users/`, {
    credentials: 'include',
  });
  
  if (!response.ok) {
    throw new Error('Failed to get organization users');
  }
  
  return response.json();
};

// Give kudos (renamed to match component usage)
export const giveKudos = async (receiverId, message) => {
  const response = await fetch(`${API_BASE_URL}/kudos/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include',
    body: JSON.stringify({
      receiver_id: receiverId,
      message: message,
    }),
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to give kudo');
  }
  
  return response.json();
};

// Get received kudos
export const getReceivedKudos = async () => {
  const response = await fetch(`${API_BASE_URL}/kudos/received/`, {
    credentials: 'include',
  });
  
  if (!response.ok) {
    throw new Error('Failed to get received kudos');
  }
  
  return response.json();
};

// Get given kudos
export const getGivenKudos = async () => {
  const response = await fetch(`${API_BASE_URL}/kudos/given/`, {
    credentials: 'include',
  });
  
  if (!response.ok) {
    throw new Error('Failed to get given kudos');
  }
  
  return response.json();
};
