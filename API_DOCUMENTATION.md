# Alumni Connect API Documentation

## Authentication Endpoints

### POST /api/auth/register
Register a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123",
  "name": "John Doe",
  "role": "student"
}
```

**Response:** 201 Created
```json
{
  "message": "User registered successfully"
}
```

### POST /api/auth/login
Authenticate user and receive JWT token.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:** 200 OK
```json
{
  "access_token": "eyJ...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe",
    "role": "student"
  }
}
```

### GET /api/auth/me
Get current authenticated user details.

**Headers:** `Authorization: Bearer <token>`

**Response:** 200 OK
```json
{
  "id": 1,
  "email": "user@example.com",
  "name": "John Doe",
  "role": "student"
}
```

## User Endpoints

### GET /api/users
List all users.

**Response:** 200 OK
```json
[
  {
    "id": 1,
    "name": "John Doe",
    "role": "student",
    "graduation_year": 2024,
    "major": "Computer Science",
    "cgpa": 8.5,
    "category": "General"
  }
]
```

### GET /api/users/:id
Get detailed user profile by ID.

**Response:** 200 OK
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "role": "student",
  "graduation_year": 2024,
  "major": "Computer Science",
  "cgpa": 8.5,
  "category": "General",
  "phone": "555-0123",
  "bio": "Final year CS student",
  "skills": "Python, Java, Web Development",
  "scholarship_applications_count": 3,
  "job_applications_count": 5,
  "mentorship_requests_count": 2
}
```

### PUT /api/users/profile
Update current user's profile.

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "name": "John Doe",
  "graduation_year": 2024,
  "major": "Computer Science",
  "cgpa": 8.5,
  "category": "General",
  "phone": "555-0123",
  "bio": "Updated bio",
  "skills": "Python, Java, React"
}
```

**Response:** 200 OK

## Scholarship Endpoints

### GET /api/scholarships
List all active scholarships.

**Response:** 200 OK
```json
[
  {
    "id": 1,
    "title": "Tech Innovation Scholarship",
    "description": "For students pursuing technology...",
    "eligibility_criteria": "Must be enrolled in CS/IT...",
    "cgpa_requirement": 7.5,
    "category_requirement": null,
    "amount": 5000.00,
    "deadline": "2024-12-31",
    "status": "active"
  }
]
```

### GET /api/scholarships/eligible
Get scholarships eligible for current student.

**Headers:** `Authorization: Bearer <token>`
**Role Required:** Student

**Response:** 200 OK - Returns scholarships matching student's CGPA and category.

### GET /api/scholarships/:id
Get scholarship details.

**Response:** 200 OK

### POST /api/scholarships
Create a new scholarship.

**Headers:** `Authorization: Bearer <token>`
**Role Required:** Alumni or Admin

**Request Body:**
```json
{
  "title": "Tech Innovation Scholarship",
  "description": "For students pursuing technology...",
  "eligibility_criteria": "Must be enrolled in CS/IT...",
  "cgpa_requirement": 7.5,
  "category_requirement": "General",
  "amount": 5000.00,
  "deadline": "2024-12-31"
}
```

**Response:** 201 Created

### PUT /api/scholarships/:id
Update scholarship (own scholarships only, or admin).

**Headers:** `Authorization: Bearer <token>`
**Role Required:** Alumni or Admin

### DELETE /api/scholarships/:id
Deactivate scholarship (own scholarships only, or admin).

**Headers:** `Authorization: Bearer <token>`
**Role Required:** Alumni or Admin

### POST /api/scholarships/:id/apply
Apply for a scholarship.

**Headers:** `Authorization: Bearer <token>`
**Role Required:** Student

**Request Body:**
```json
{
  "cover_letter": "I am passionate about...",
  "additional_info": "Additional details..."
}
```

**Response:** 201 Created

### GET /api/scholarships/:id/applications
Get applications for a scholarship (scholarship creator only, or admin).

**Headers:** `Authorization: Bearer <token>`
**Role Required:** Alumni or Admin

### GET /api/scholarships/applications/my
Get current student's scholarship applications.

**Headers:** `Authorization: Bearer <token>`
**Role Required:** Student

### PUT /api/scholarships/applications/:id/status
Update application status.

**Headers:** `Authorization: Bearer <token>`
**Role Required:** Alumni or Admin

**Request Body:**
```json
{
  "status": "approved"
}
```

## Opportunity Endpoints

### GET /api/opportunities
List all active job/internship opportunities.

### GET /api/opportunities/:id
Get opportunity details.

### POST /api/opportunities
Create a new opportunity.

**Headers:** `Authorization: Bearer <token>`
**Role Required:** Alumni or Admin

### PUT /api/opportunities/:id
Update opportunity (own opportunities only, or admin).

**Headers:** `Authorization: Bearer <token>`
**Role Required:** Alumni or Admin

### DELETE /api/opportunities/:id
Deactivate opportunity (own opportunities only, or admin).

**Headers:** `Authorization: Bearer <token>`
**Role Required:** Alumni or Admin

## Search Endpoint

### GET /api/search?query=:term
Unified search across all entities.

**Query Parameters:**
- `query` (required): Search term (minimum 2 characters)

**Response:** 200 OK
```json
{
  "query": "engineering",
  "count": 15,
  "results": [
    {
      "type": "opportunity",
      "id": 1,
      "title": "Software Engineering Intern",
      "description": "Join our team...",
      "company": "Google"
    },
    {
      "type": "student",
      "id": 3,
      "title": "Sarah Wilson",
      "description": "Final year CS student...",
      "major": "Computer Science",
      "cgpa": 8.5
    },
    {
      "type": "scholarship",
      "id": 1,
      "title": "Tech Innovation Scholarship",
      "description": "For students pursuing...",
      "cgpa_requirement": 7.5
    }
  ]
}
```

## Admin Endpoints

### GET /api/admin/dashboard
Get platform statistics.

**Headers:** `Authorization: Bearer <token>`
**Role Required:** Admin

**Response:** 200 OK
```json
{
  "users": {
    "total_students": 150,
    "total_alumni": 75,
    "total_admins": 3,
    "total": 228
  },
  "opportunities": {
    "active": 45
  },
  "scholarships": {
    "active": 12,
    "total_applications": 230
  },
  "mentorships": {
    "pending": 18
  }
}
```

### GET /api/admin/users
List all users with full details.

**Headers:** `Authorization: Bearer <token>`
**Role Required:** Admin

### POST /api/admin/users
Create a new user.

**Headers:** `Authorization: Bearer <token>`
**Role Required:** Admin

### PUT /api/admin/users/:id
Update any user.

**Headers:** `Authorization: Bearer <token>`
**Role Required:** Admin

### DELETE /api/admin/users/:id
Delete a user.

**Headers:** `Authorization: Bearer <token>`
**Role Required:** Admin

### GET /api/admin/opportunities
List all opportunities (including inactive).

**Headers:** `Authorization: Bearer <token>`
**Role Required:** Admin

### DELETE /api/admin/opportunities/:id
Delete any opportunity.

**Headers:** `Authorization: Bearer <token>`
**Role Required:** Admin

### GET /api/admin/scholarships
List all scholarships with application counts.

**Headers:** `Authorization: Bearer <token>`
**Role Required:** Admin

### DELETE /api/admin/scholarships/:id
Delete any scholarship.

**Headers:** `Authorization: Bearer <token>`
**Role Required:** Admin

### GET /api/admin/applications
List all applications.

**Headers:** `Authorization: Bearer <token>`
**Role Required:** Admin

## Role-Based Access Control

### Roles:
- **student**: Can view opportunities, apply for jobs/scholarships, request mentorship
- **alumni**: Can create opportunities/scholarships, mentor students, view applications
- **admin**: Full access to all endpoints, can manage all entities

### Demo Accounts:
- **Admin:** admin@alumni.edu / password123
- **Alumni:** alice@alumni.edu / password123
- **Student:** sarah@student.edu / password123

## Error Responses

### 400 Bad Request
```json
{
  "error": "Invalid input or missing required fields"
}
```

### 401 Unauthorized
```json
{
  "error": "Invalid credentials or missing token"
}
```

### 403 Forbidden
```json
{
  "error": "Access denied",
  "message": "This endpoint requires admin role"
}
```

### 404 Not Found
```json
{
  "error": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "Database connection failed"
}
```
