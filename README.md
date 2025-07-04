# Kudos Application

A Django + React application where users can give "kudos" to other users in their organization.

## Features

- **User Authentication**: Simple login/logout system
- **Weekly Kudos Limit**: Each user gets 3 kudos per week (non-accumulating)
- **Give Kudos**: Send appreciation messages to colleagues
- **View History**: See kudos you've received and given
- **Organization Management**: Users are grouped by organizations
- **Demo Data**: Built-in command to generate sample data

## Project Structure

```
kudos/
├── backend/                 # Django backend
│   └── kudos_project/
│       ├── manage.py
│       ├── api/            # API endpoints
│       ├── users/          # Custom user model
│       ├── organizations/  # Organization model
│       ├── kudos/          # Kudos model
│       └── kudos_project/  # Settings
└── frontend/               # React frontend
    └── src/
        ├── components/     # React components
        └── services/       # API service
```

## Quick Start

### Backend (Django)

1. **Navigate to backend directory:**
   ```bash
   cd backend/kudos_project
   ```

2. **Activate virtual environment and install dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Generate demo data (optional):**
   ```bash
   python manage.py generate_demo_data
   ```

5. **Start Django server:**
   ```bash
   python manage.py runserver
   ```
   Backend will be available at: http://localhost:8000

### Frontend (React)

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start React development server:**
   ```bash
   npm start
   ```
   Frontend will be available at: http://localhost:3000

## Demo Users

If you generated demo data, you can login with these sample accounts:

**Tech Innovators Inc.:**
- **Username:** `alice_dev` **Password:** `password123`
- **Username:** `bob_pm` **Password:** `password123`
- **Username:** `charlie_design` **Password:** `password123`
- **Username:** `diana_qa` **Password:** `password123`
- **Username:** `eve_dev` **Password:** `password123`

**Creative Solutions Ltd.:**
- **Username:** `frank_creative` **Password:** `password123`
- **Username:** `grace_marketing` **Password:** `password123`
- **Username:** `henry_design` **Password:** `password123`
- **Username:** `iris_copy` **Password:** `password123`

**Global Consulting Group:**
- **Username:** `jack_consultant` **Password:** `password123`
- **Username:** `kate_analyst` **Password:** `password123`
- **Username:** `liam_strategy` **Password:** `password123`

## API Endpoints

### Authentication
- `POST /api/auth/login/` - Login
- `POST /api/auth/logout/` - Logout
- `GET /api/auth/me/` - Get current user

### Users
- `GET /api/users/` - Get organization users

### Kudos
- `POST /api/kudos/` - Give kudos
- `GET /api/kudos/received/` - Get received kudos
- `GET /api/kudos/given/` - Get given kudos

## Management Commands

### Generate Demo Data
```bash
python manage.py generate_demo_data
```
Creates sample organizations, users, and randomized kudos.

### Reset Kudos (Weekly)
```bash
python manage.py reset_kudos
```
Resets all users' kudos count to 3. This should be run weekly.

## Application Flow

1. **Login**: Users authenticate with username/password
2. **Dashboard**: Shows user info, remaining kudos, and main actions
3. **Give Kudos**: 
   - Select a colleague from the organization
   - Write an appreciation message
   - Send kudos (decreases your weekly count)
4. **View History**: 
   - See kudos you've received from others
   - See kudos you've given to others

## Key Features

### Weekly Kudos System
- Each user starts with 3 kudos per week
- Kudos don't accumulate (use them or lose them)
- Reset happens every Monday (via management command)

### Organization-based
- Users can only give kudos to people in their organization
- Organization info is displayed in the header

### Responsive Design
- Clean, modern UI that works on desktop and mobile
- Intuitive user experience with clear calls-to-action

## Technology Stack

**Backend:**
- Django 5.2.4
- Django REST Framework
- SQLite database (development)
- CORS headers for cross-origin requests

**Frontend:**
- React 18
- Modern CSS with flexbox/grid
- Fetch API for backend communication
- Responsive design

## Development Notes

- Backend runs on port 8000
- Frontend runs on port 3000
- CORS is configured to allow frontend-backend communication
- Session-based authentication with cookies
- Real-time updates when giving kudos

## Future Enhancements

- Email notifications for received kudos
- Kudos analytics and reporting
- Team-based kudos
- Kudos categories/tags
- Mobile app
- Slack/Teams integration
