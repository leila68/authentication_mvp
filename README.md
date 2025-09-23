# authentication_mvp

A secure, role-based authentication service built with FastAPI for the Bright Health AI Integration Platform. This MVP provides JWT-based authentication with healthcare-specific user roles and HIPAA-compliant security practices.

## Features

- **JWT Authentication** - Secure, stateless token-based authentication
- **Role-Based Access Control** - Doctor, Patient, Admin, and Staff roles
- **Healthcare-Focused** - Built with medical workflow requirements in mind
- **Password Security** - Bcrypt hashing with secure password policies
- **RESTful API** - Clean, documented endpoints
- **Interactive Documentation** - Automatic Swagger/OpenAPI docs
- **Production Ready** - Scalable architecture with Docker support

## Prerequisites

- Python 3.9 or higher
- pip (Python package installer)
- Postman (for API testing)

## Installation & Setup

### 1. Clone and Setup Project

```bash
# Create project directory
mkdir bright_health_auth_mvp
cd bright_health_auth_mvp

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn python-jose[cryptography] passlib[bcrypt] python-multipart sqlalchemy psycopg2-binary python-dotenv
```

### 2. Configure Environment Variables

Create a `.env` file in the root directory:

```env
# Generate SECRET_KEY with: python -c "import secrets; print(secrets.token_urlsafe(32))"
SECRET_KEY=your_generated_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///./bright_health.db
```

### 3. Run the Application

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API Base URL:** http://localhost:8000
- **Interactive Docs:** http://localhost:8000/docs
- **OpenAPI Schema:** http://localhost:8000/openapi.json

## Testing with Postman

### Quick Setup

1. **Start the server** (see installation steps above)
2. **Open Postman**
3. **Import the collection** or follow the manual setup below

### Environment Setup

Create a new Postman environment with these variables:

| Variable | Value |
|----------|--------|
| `base_url` | `http://localhost:8000` |
| `access_token` | (leave empty - will be auto-populated) |

### Core Test Scenarios

#### 1. Health Check ✅
```http
GET {{base_url}}/health
```
**Expected Response:**
```json
{
    "status": "healthy",
    "service": "auth-mvp"
}
```

#### 2. User Registration 👤
```http
POST {{base_url}}/auth/register
Content-Type: application/json

{
    "email": "doctor@brighthealth.com",
    "username": "dr_smith",
    "full_name": "Dr. John Smith",
    "password": "securepassword123",
    "role": "doctor",
    "is_active": true
}
```

**Expected Response:** User object without password field

#### 3. User Login 🔐
```http
POST {{base_url}}/auth/token
Content-Type: application/x-www-form-urlencoded

username=dr_smith&password=securepassword123
```

**Expected Response:**
```json
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "token_type": "bearer"
}
```

**Pro Tip:** Add this test script to auto-save the token:
```javascript
if (pm.response.code === 200) {
    const response = pm.response.json();
    pm.environment.set("access_token", response.access_token);
}
```

#### 4. Get Current User Profile 
```http
GET {{base_url}}/auth/me
Authorization: Bearer {{access_token}}
```

#### 5. Get All Users (Admin Only) 
```http
GET {{base_url}}/users/?skip=0&limit=10
Authorization: Bearer {{access_token}}
```

#### 6. Update User Profile 
```http
PUT {{base_url}}/users/1
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
    "full_name": "Dr. John Smith Updated",
    "email": "doctor.updated@brighthealth.com"
}
```

### Error Testing Scenarios

#### Invalid Credentials
```http
POST {{base_url}}/auth/token
Content-Type: application/x-www-form-urlencoded

username=wronguser&password=wrongpass
```
**Expected:** `401 Unauthorized`

#### Missing Authorization
```http
GET {{base_url}}/auth/me
# No Authorization header
```
**Expected:** `401 Unauthorized`

#### Permission Denied
```http
# Login as patient, then try to access admin endpoint
GET {{base_url}}/users/
Authorization: Bearer {{patient_token}}
```
**Expected:** `403 Forbidden`

### Complete Test Workflow

**Run these tests in sequence for full validation:**

1. ✅ **Health Check** → Verify API is running
2. ✅ **Register Admin** → Create admin user
3. ✅ **Register Doctor** → Create doctor user
4. ✅ **Register Patient** → Create patient user
5. ✅ **Login as Admin** → Get admin token
6. ✅ **Get Current User** → Verify admin profile
7. ✅ **Get All Users** → Admin can see all users
8. ✅ **Login as Doctor** → Get doctor token
9. ✅ **Try Get All Users** → Should fail (403 Forbidden)
10. ✅ **Get Own Profile** → Doctor can see own profile

## API Endpoints Reference

### Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/auth/register` | Register new user | No |
| POST | `/auth/token` | Login and get JWT token | No |
| GET | `/auth/me` | Get current user profile | Yes |

### User Management Endpoints

| Method | Endpoint | Description | Auth Required | Role Required |
|--------|----------|-------------|---------------|---------------|
| GET | `/users/` | Get all users (paginated) | Yes | Admin |
| GET | `/users/{user_id}` | Get user by ID | Yes | Self or Admin |
| PUT | `/users/{user_id}` | Update user | Yes | Self or Admin |

### System Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/` | Root endpoint | No |
| GET | `/health` | Health check | No |
| GET | `/docs` | Interactive API documentation | No |

## User Roles & Permissions

| Role | Permissions |
|------|-------------|
| **Patient** | View/edit own profile |
| **Doctor** | View/edit own profile, access patient data (when implemented) |
| **Staff** | View/edit own profile, limited admin functions (when implemented) |
| **Admin** | Full access to all users and system functions |


**Built with ❤️ for Bright Health's AI Integration Platform**
