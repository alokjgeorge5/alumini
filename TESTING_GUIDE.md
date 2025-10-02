# Alumni Connect - Testing Guide

## Setup Instructions

### 1. Start the Application
```bash
docker compose up --build
```

Wait for all services to start:
- Database: Ready when you see "ready for connections"
- Backend: Running on http://localhost:5000
- Frontend: Running on http://localhost:5173

### 2. Verify Backend Health
```bash
curl http://localhost:5000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "database": "connected"
}
```

---

## Demo Accounts

| Role    | Email              | Password    | Purpose                          |
|---------|-------------------|-------------|----------------------------------|
| Admin   | admin@alumni.edu  | password123 | Full system access, manage all   |
| Alumni  | alice@alumni.edu  | password123 | Create opportunities/scholarships|
| Alumni  | bob@alumni.edu    | password123 | Create opportunities/scholarships|
| Student | sarah@student.edu | password123 | Apply for jobs/scholarships      |
| Student | mike@student.edu  | password123 | Apply for jobs/scholarships      |

---

## Feature Testing Checklist

### ✅ Feature 1: Role-Based Access Control

#### Test 1.1: Admin Role Access
```bash
# Login as admin
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@alumni.edu","password":"password123"}'

# Save the token from response
TOKEN="<your_token_here>"

# Access admin dashboard
curl http://localhost:5000/api/admin/dashboard \
  -H "Authorization: Bearer $TOKEN"
```

**Expected:** 200 OK with platform statistics

#### Test 1.2: Alumni Role Restrictions
```bash
# Login as alumni
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@alumni.edu","password":"password123"}'

TOKEN_ALUMNI="<alumni_token>"

# Try to access admin endpoint (should fail)
curl http://localhost:5000/api/admin/dashboard \
  -H "Authorization: Bearer $TOKEN_ALUMNI"
```

**Expected:** 403 Forbidden

#### Test 1.3: Student Role Restrictions
```bash
# Login as student
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"sarah@student.edu","password":"password123"}'

TOKEN_STUDENT="<student_token>"

# Try to create opportunity (should fail)
curl -X POST http://localhost:5000/api/opportunities \
  -H "Authorization: Bearer $TOKEN_STUDENT" \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Job","company":"Test Co","type":"full-time"}'
```

**Expected:** 403 Forbidden

---

### ✅ Feature 2: Enhanced Student Profiles

#### Test 2.1: View Student Profile with Enhanced Fields
```bash
# Get student profile (Sarah - ID: 4)
curl http://localhost:5000/api/users/4
```

**Expected Response:**
```json
{
  "id": 4,
  "name": "Sarah Wilson",
  "email": "sarah@student.edu",
  "role": "student",
  "cgpa": 8.5,
  "category": "General",
  "phone": "555-0103",
  "major": "Computer Science",
  "graduation_year": 2024,
  "scholarship_applications_count": 1,
  "job_applications_count": 1,
  "mentorship_requests_count": 1
}
```

#### Test 2.2: Update Student Profile
```bash
curl -X PUT http://localhost:5000/api/users/profile \
  -H "Authorization: Bearer $TOKEN_STUDENT" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Sarah Wilson",
    "cgpa": 8.7,
    "category": "General",
    "phone": "555-9999",
    "bio": "Updated bio"
  }'
```

**Expected:** 200 OK

---

### ✅ Feature 3: Complete Scholarship Management

#### Test 3.1: List All Active Scholarships
```bash
curl http://localhost:5000/api/scholarships
```

**Expected:** Array of scholarships with eligibility criteria

#### Test 3.2: Get Eligible Scholarships (Student)
```bash
# Login as Sarah (CGPA: 8.5, Category: General)
curl http://localhost:5000/api/scholarships/eligible \
  -H "Authorization: Bearer $TOKEN_STUDENT"
```

**Expected:** Scholarships where:
- cgpa_requirement <= 8.5
- category_requirement is NULL or "General"

#### Test 3.3: Create Scholarship (Alumni)
```bash
# Login as alumni
curl -X POST http://localhost:5000/api/scholarships \
  -H "Authorization: Bearer $TOKEN_ALUMNI" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Women in Tech Scholarship",
    "description": "Supporting women pursuing CS degrees",
    "eligibility_criteria": "Female students in CS/IT programs",
    "cgpa_requirement": 7.0,
    "category_requirement": null,
    "amount": 6000.00,
    "deadline": "2025-03-31"
  }'
```

**Expected:** 201 Created

#### Test 3.4: Apply for Scholarship (Student)
```bash
# Student applies for scholarship ID: 1
curl -X POST http://localhost:5000/api/scholarships/1/apply \
  -H "Authorization: Bearer $TOKEN_STUDENT" \
  -H "Content-Type: application/json" \
  -d '{
    "cover_letter": "I am deeply passionate about technology and innovation...",
    "additional_info": "GPA: 8.5, Multiple projects on GitHub"
  }'
```

**Expected:** 201 Created (or 400 if already applied)

#### Test 3.5: View Scholarship Applications (Alumni)
```bash
# Alumni views applications for their scholarship
curl http://localhost:5000/api/scholarships/1/applications \
  -H "Authorization: Bearer $TOKEN_ALUMNI"
```

**Expected:** Array of applications with student details (name, email, CGPA, category)

#### Test 3.6: Update Application Status (Alumni)
```bash
curl -X PUT http://localhost:5000/api/scholarships/applications/1/status \
  -H "Authorization: Bearer $TOKEN_ALUMNI" \
  -H "Content-Type: application/json" \
  -d '{"status": "approved"}'
```

**Expected:** 200 OK

#### Test 3.7: View My Applications (Student)
```bash
curl http://localhost:5000/api/scholarships/applications/my \
  -H "Authorization: Bearer $TOKEN_STUDENT"
```

**Expected:** Array of student's scholarship applications with statuses

---

### ✅ Feature 4: Unified Search

#### Test 4.1: Search for "engineering"
```bash
curl "http://localhost:5000/api/search?query=engineering"
```

**Expected Response:**
```json
{
  "query": "engineering",
  "count": 3,
  "results": [
    {
      "type": "opportunity",
      "id": 1,
      "title": "Software Engineering Intern",
      "description": "Join our team for a 12-week summer...",
      "company": "Google"
    },
    {
      "type": "student",
      "id": 4,
      "title": "Sarah Wilson",
      "description": "Final year CS student...",
      "major": "Computer Science",
      "cgpa": 8.5
    }
  ]
}
```

#### Test 4.2: Search for "scholarship"
```bash
curl "http://localhost:5000/api/search?query=scholarship"
```

**Expected:** Results including scholarships with matching titles/descriptions

#### Test 4.3: Invalid Search (too short)
```bash
curl "http://localhost:5000/api/search?query=a"
```

**Expected:** 400 Bad Request

---

### ✅ Feature 5: Admin Dashboard

#### Test 5.1: View Platform Statistics
```bash
curl http://localhost:5000/api/admin/dashboard \
  -H "Authorization: Bearer $TOKEN_ADMIN"
```

**Expected Response:**
```json
{
  "users": {
    "total_students": 2,
    "total_alumni": 2,
    "total_admins": 1,
    "total": 5
  },
  "opportunities": {
    "active": 3
  },
  "scholarships": {
    "active": 4,
    "total_applications": 2
  }
}
```

#### Test 5.2: Manage Users (Admin)
```bash
# List all users
curl http://localhost:5000/api/admin/users \
  -H "Authorization: Bearer $TOKEN_ADMIN"

# Create new user
curl -X POST http://localhost:5000/api/admin/users \
  -H "Authorization: Bearer $TOKEN_ADMIN" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newstudent@test.edu",
    "password": "password123",
    "name": "New Student",
    "role": "student",
    "cgpa": 8.0,
    "category": "General"
  }'

# Update user
curl -X PUT http://localhost:5000/api/admin/users/6 \
  -H "Authorization: Bearer $TOKEN_ADMIN" \
  -H "Content-Type: application/json" \
  -d '{"cgpa": 8.5}'

# Delete user
curl -X DELETE http://localhost:5000/api/admin/users/6 \
  -H "Authorization: Bearer $TOKEN_ADMIN"
```

#### Test 5.3: Manage All Scholarships (Admin)
```bash
# View all scholarships (including inactive)
curl http://localhost:5000/api/admin/scholarships \
  -H "Authorization: Bearer $TOKEN_ADMIN"

# Delete any scholarship
curl -X DELETE http://localhost:5000/api/admin/scholarships/2 \
  -H "Authorization: Bearer $TOKEN_ADMIN"
```

---

## Database Query Testing

### Complex JOIN Query
```sql
-- Run in MySQL client (docker exec -it <db_container> mysql -u alumni_user -p)
USE alumni_connect;

-- Get students with their scholarship applications
SELECT
    u.id, u.name, u.email, u.cgpa, u.category,
    s.title as scholarship_title, s.amount,
    sa.status, sa.application_date
FROM users u
JOIN scholarship_applications sa ON u.id = sa.student_id
JOIN scholarships s ON sa.scholarship_id = s.id
WHERE u.role = 'student'
ORDER BY sa.application_date DESC;
```

### Aggregation Query
```sql
-- Application statistics per scholarship
SELECT
    s.id, s.title, s.amount,
    COUNT(sa.id) as total_applications,
    SUM(CASE WHEN sa.status = 'approved' THEN 1 ELSE 0 END) as approved,
    AVG(u.cgpa) as avg_applicant_cgpa
FROM scholarships s
LEFT JOIN scholarship_applications sa ON s.id = sa.scholarship_id
LEFT JOIN users u ON sa.student_id = u.id
GROUP BY s.id, s.title, s.amount
ORDER BY total_applications DESC;
```

### Eligibility Subquery
```sql
-- Find scholarships student is eligible for
SELECT s.id, s.title, s.cgpa_requirement, s.category_requirement
FROM scholarships s
WHERE s.status = 'active'
  AND (s.cgpa_requirement IS NULL OR s.cgpa_requirement <= 8.5)
  AND (s.category_requirement IS NULL OR s.category_requirement = 'General');
```

---

## Performance Testing

### Query Response Times
Test the following and ensure < 100ms response:

1. **Simple SELECT by ID:**
   ```bash
   time curl http://localhost:5000/api/users/1
   ```
   **Target:** < 10ms

2. **Filtered Search with Index:**
   ```bash
   time curl http://localhost:5000/api/scholarships/eligible \
     -H "Authorization: Bearer $TOKEN_STUDENT"
   ```
   **Target:** < 50ms

3. **Complex JOIN:**
   ```bash
   time curl http://localhost:5000/api/scholarships/1/applications \
     -H "Authorization: Bearer $TOKEN_ALUMNI"
   ```
   **Target:** < 100ms

4. **Global Search:**
   ```bash
   time curl "http://localhost:5000/api/search?query=computer"
   ```
   **Target:** < 150ms

---

## Error Handling Testing

### Test Invalid Inputs
```bash
# Missing required fields
curl -X POST http://localhost:5000/api/scholarships \
  -H "Authorization: Bearer $TOKEN_ALUMNI" \
  -H "Content-Type: application/json" \
  -d '{"description":"Missing title"}'

# Expected: 400 Bad Request

# Invalid CGPA value
curl -X PUT http://localhost:5000/api/users/profile \
  -H "Authorization: Bearer $TOKEN_STUDENT" \
  -H "Content-Type: application/json" \
  -d '{"cgpa": 15.0}'

# Expected: 500 with constraint violation error

# Unauthorized access
curl http://localhost:5000/api/admin/dashboard

# Expected: 401 Unauthorized
```

---

## Integration Testing Workflow

### Complete User Journey - Student Applies for Scholarship

1. **Student registers account:**
   ```bash
   curl -X POST http://localhost:5000/api/auth/register \
     -H "Content-Type: application/json" \
     -d '{
       "email":"newstudent@test.edu",
       "password":"test123",
       "name":"Test Student",
       "role":"student"
     }'
   ```

2. **Student logs in:**
   ```bash
   curl -X POST http://localhost:5000/api/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email":"newstudent@test.edu","password":"test123"}'
   ```

3. **Student updates profile with CGPA:**
   ```bash
   curl -X PUT http://localhost:5000/api/users/profile \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"cgpa":8.0,"category":"General","phone":"555-1234"}'
   ```

4. **Student views eligible scholarships:**
   ```bash
   curl http://localhost:5000/api/scholarships/eligible \
     -H "Authorization: Bearer $TOKEN"
   ```

5. **Student applies for scholarship:**
   ```bash
   curl -X POST http://localhost:5000/api/scholarships/1/apply \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"cover_letter":"I am interested in this scholarship..."}'
   ```

6. **Student checks application status:**
   ```bash
   curl http://localhost:5000/api/scholarships/applications/my \
     -H "Authorization: Bearer $TOKEN"
   ```

---

## Success Criteria Verification

### ✅ All features work independently
- [ ] Role-based access control prevents unauthorized actions
- [ ] Enhanced student profiles display all new fields
- [ ] Scholarship eligibility filtering works correctly
- [ ] Search returns results across all entity types
- [ ] Admin dashboard shows accurate statistics

### ✅ Database queries execute efficiently
- [ ] Simple queries: < 10ms
- [ ] Indexed searches: < 50ms
- [ ] Complex JOINs: < 100ms
- [ ] Global search: < 150ms

### ✅ Data integrity maintained
- [ ] Foreign key constraints prevent orphaned records
- [ ] CGPA validation (0.00-10.00) enforced
- [ ] Duplicate scholarship applications prevented
- [ ] Role restrictions enforced at API level

### ✅ User interface provides clear feedback
- [ ] Error messages are descriptive
- [ ] Success messages confirm actions
- [ ] API returns appropriate HTTP status codes

---

## Troubleshooting

### Issue: "Database connection failed"
**Solution:** Wait for database to fully initialize (30-60 seconds after startup)

### Issue: "Invalid token" error
**Solution:** Token may have expired. Login again to get a new token.

### Issue: 403 Forbidden on valid endpoint
**Solution:** Check that you're using the correct role (admin/alumni/student) for the endpoint.

### Issue: Duplicate key error on application
**Solution:** Student has already applied for this scholarship. Check existing applications.

---

## Manual Frontend Testing

1. **Open http://localhost:5173**
2. **Login with demo accounts**
3. **Test role-specific features:**
   - Admin: Access admin panel, manage users
   - Alumni: Create scholarships/opportunities
   - Student: View and apply for scholarships

4. **Test search functionality:**
   - Search for "engineering"
   - Search for "scholarship"
   - Verify results display correctly

5. **Test profile management:**
   - Update student profile with CGPA
   - Verify changes persist after refresh
