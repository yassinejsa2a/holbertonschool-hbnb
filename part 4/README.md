# HBnB - Holberton School Project (Part 4)

A full-stack web application for property rental listings, similar to Airbnb. This project includes a Flask REST API backend and a vanilla JavaScript frontend.

## Architecture

- **Backend**: Flask REST API with SQLAlchemy ORM
- **Frontend**: Vanilla HTML, CSS, and JavaScript
- **Database**: SQLite (development)
- **Authentication**: JWT tokens with Flask-JWT-Extended

## Project Structure

```
part 4/
├── Backend/
│   ├── app/
│   │   ├── api/v1/          # API endpoints
│   │   ├── models/          # Database models
│   │   ├── persistence/     # Data persistence layer
│   │   ├── repositories/    # Repository pattern
│   │   └── services/        # Business logic
│   ├── config.py           # Application configuration
│   ├── init_db.py          # Database initialization script
│   ├── run.py              # Backend server entry point
│   └── requirements.txt    # Python dependencies
├── Frontend/
│   ├── index.html          # Main page - places listing
│   ├── place.html          # Place details and reviews
│   ├── add_review.html     # Add review form
│   ├── login.html          # User authentication
│   ├── scripts.js          # Frontend JavaScript logic
│   ├── styles.css          # Styling
│   ├── run.py              # Frontend server (if needed)
│   └── images/             # Static assets
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.8+
- Modern web browser

### Installation & Setup

Follow these steps to run the application locally:

#### 1. Clone the Repository

```bash
git clone <repository-url>
cd holbertonschool-hbnb/part\ 4
```

#### 2. Install Backend Dependencies

```bash
cd Backend
pip install -r requirements.txt
```

#### 3. Open 3 Terminals

You'll need **3 separate terminal** for this setup:

---

### Terminal 1: Initialize Database

First, populate the database with sample data:

```bash
cd Backend
python3 init_db.py
```

**Expected output:**
```
Tables créées avec succès!
Utilisateur administrateur créé!
Utilisateur lambda Jane créé!
✓ Place 1: 'Annonce 1' créée (ID: ...)
✓ Place 2: 'Annonce 2' créée (ID: ...)
...
Données initiales insérées avec succès!
```

This script creates:
- Database tables
- Admin user: `admin@hbnb.com` / `admin1234`
- Regular user: `jane@example.com` / `password123`
- 5 sample places with amenities
- Sample amenities (WiFi, Parking, Pool, etc.)

---

### Terminal 2: Start Backend Server

```bash
cd Backend
python3 run.py
```

**Expected output:**
```
* Running on http://127.0.0.1:5000
* Debug mode: on
```

The backend API will be available at: `http://localhost:5000`

---

### Terminal 3: Start Frontend Server

```bash
cd Frontend
python3 -m http.server 5500
```

**Expected output:**
```
Serving HTTP on 0.0.0.0 port 5500 (http://0.0.0.0:5500/) ...
```

The frontend will be available at: `http://localhost:5500`

---

## Accessing the Application

1. Open your web browser
2. Navigate to: `http://localhost:5500`
3. You should see the main page with a list of available places

### Test Accounts

Use these pre-created accounts to test the application:

**Admin Account:**
- Email: `admin@hbnb.com`
- Password: `admin1234`

**Regular User:**
- Email: `jane@example.com`
- Password: `password123`

## API Endpoints

The backend provides the following API endpoints:

- `GET /api/v1/places` - List all places
- `GET /api/v1/places/{id}` - Get place details
- `POST /api/v1/reviews` - Create a review (requires authentication)
- `POST /api/v1/auth/login` - User authentication
- `GET /api/v1/users` - List users
- `GET /api/v1/amenities` - List amenities

## Features

- **Place Listings**: Browse available rental properties
- **Place Details**: View detailed information about each place
- **User Authentication**: Login/logout functionality
- **Reviews System**: Add and view reviews for places
- **Price Filtering**: Filter places by price range
- **Responsive Design**: Works on desktop and mobile devices

## Authentication

The application uses JWT (JSON Web Tokens) for authentication:
- Tokens are stored in browser cookies
- Protected routes require valid authentication
- Users must be logged in to submit reviews

## Troubleshooting

### Common Issues

1. **Port already in use:**
   - Backend: Change port in `run.py` or kill process using port 5000
   - Frontend: Use different port: `python3 -m http.server 5501`

2. **CORS errors:**
   - Ensure both servers are running
   - Check that frontend is accessing `localhost:5000` for API calls

3. **Database errors:**
   - Delete `instance/hbnb.db` and run `python3 init_db.py` again

4. **Login issues:**
   - Ensure backend is running and accessible
   - Check browser console for error messages

### Useful Commands

```bash
# Check if ports are in use
lsof -i :5000  # Backend port
lsof -i :5500  # Frontend port

# Kill process using specific port
kill -9 $(lsof -t -i:5000)
```

## Development Notes

- The application runs in development mode with debug enabled
- Database file is located at `Backend/instance/hbnb.db`
- CORS is configured to allow frontend-backend communication
- Static files (images) are served from the `Frontend/images/` directory

## Quick Start Summary

```bash
# Terminal 1 - Initialize database
cd Backend && python3 init_db.py

# Terminal 2 - Start backend
cd Backend && python3 run.py

# Terminal 3 - Start frontend  
cd Frontend && python3 -m http.server 5500

# Open browser to http://localhost:5500
```

## Authors :
Yassine, Nawfel