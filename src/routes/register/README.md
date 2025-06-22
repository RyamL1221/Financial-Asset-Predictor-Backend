# Register Endpoint

This module provides user registration functionality with MySQL database integration and bcrypt password encryption.

## Setup

1. Install required dependencies:
   ```bash
   pip install bcrypt pymysql python-dotenv
   ```

2. Create a `.env` file in the root directory with the following variables:
   ```
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=your_password_here
   DB_NAME=financial_predictor
   DB_PORT=3306
   ```

3. Create the MySQL database:
   ```sql
   CREATE DATABASE financial_predictor;
   ```

## API Endpoints

### POST /api/register/
Register a new user.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response (201 Created):**
```json
{
  "message": "User registered successfully",
  "user_id": 1,
  "email": "user@example.com"
}
```

**Error Responses:**
- `400 Bad Request`: Missing or invalid data
- `409 Conflict`: User already exists
- `500 Internal Server Error`: Database connection issues

### GET /api/register/health
Health check endpoint.

**Response (200 OK):**
```json
{
  "status": "healthy",
  "service": "register"
}
```

## Database Schema

The `users` table is automatically created with the following structure:

```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

## Security Features

- Passwords are encrypted using bcrypt with salt
- Email validation (basic format check)
- Password minimum length requirement (6 characters)
- Unique email constraint
- SQL injection prevention using parameterized queries 