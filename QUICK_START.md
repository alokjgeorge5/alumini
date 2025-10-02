# Quick Start Guide - Alumni Connect Enhanced System

## 🚀 Get Started in 2 Minutes

### Step 1: Start the Application
```bash
docker compose up --build
```

Wait for these messages:
- Database: `ready for connections`
- Backend: `Running on http://0.0.0.0:5000`
- Frontend: `Local: http://localhost:5173`

### Step 2: Verify Backend Health
```bash
curl http://localhost:5000/api/health
```

Expected response:
```json
{"status": "healthy", "database": "connected"}
```

### Step 3: Access the Platform
Open your browser to: **http://localhost:5173**

---

## 🎯 Try These Features Right Away

### 1. Login as Admin
```
Email: admin@alumni.edu
Password: password123
```

**What you can do:**
- View platform statistics dashboard
- Manage all users, opportunities, and scholarships
- View all applications across the platform

**Try this API call:**
```bash
# Login
TOKEN=$(curl -s -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@alumni.edu","password":"password123"}' \
  | jq -r '.access_token')

# View dashboard
curl -s http://localhost:5000/api/admin/dashboard \
  -H "Authorization: Bearer $TOKEN" | jq
```

---

### 2. Login as Student
```
Email: sarah@student.edu
Password: password123
```

**Student Profile:**
- Name: Sarah Wilson
- CGPA: 8.5
- Category: General
- Major: Computer Science

**What you can do:**
- View scholarships you're eligible for (based on your CGPA and category)
- Apply for scholarships
- Track your application status
- Search for opportunities and alumni

**Try this API call:**
```bash
# Login as student
TOKEN=$(curl -s -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"sarah@student.edu","password":"password123"}' \
  | jq -r '.access_token')

# View eligible scholarships
curl -s http://localhost:5000/api/scholarships/eligible \
  -H "Authorization: Bearer $TOKEN" | jq
```

**Expected eligible scholarships:**
- Tech Innovation Scholarship (requires CGPA 7.5+) ✅
- Business Leadership Award (requires CGPA 7.0+) ✅
- Merit-Based Academic Scholarship (requires CGPA 8.5+, General category) ✅
- NOT Diversity Excellence (requires OBC category) ❌

---

### 3. Login as Alumni
```
Email: alice@alumni.edu
Password: password123
```

**Alumni Profile:**
- Name: Alice Johnson
- Company: Google
- Position: Software Engineer

**What you can do:**
- Create new scholarships with eligibility criteria
- Post job opportunities
- View and manage applications for your scholarships
- Approve or reject scholarship applications

**Try this API call:**
```bash
# Login as alumni
TOKEN=$(curl -s -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@alumni.edu","password":"password123"}' \
  | jq -r '.access_token')

# Create a new scholarship
curl -s -X POST http://localhost:5000/api/scholarships \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "AI Research Scholarship",
    "description": "For students pursuing AI and ML research",
    "eligibility_criteria": "Strong background in CS and mathematics",
    "cgpa_requirement": 8.0,
    "category_requirement": null,
    "amount": 8000.00,
    "deadline": "2025-06-30"
  }' | jq
```

---

### 4. Use Unified Search
Search across students, alumni, opportunities, scholarships, and mentorships:

```bash
# Search for "engineering"
curl -s "http://localhost:5000/api/search?query=engineering" | jq
```

**What you'll find:**
- Opportunities: "Software Engineering Intern"
- Students: Those majoring in engineering fields
- Scholarships: Tech-related scholarships

---

## 🧪 Test Complete Workflow

### Workflow: Student Applies for Scholarship

#### 1. Student views eligible scholarships
```bash
TOKEN_STUDENT=$(curl -s -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"sarah@student.edu","password":"password123"}' \
  | jq -r '.access_token')

curl -s http://localhost:5000/api/scholarships/eligible \
  -H "Authorization: Bearer $TOKEN_STUDENT" | jq
```

#### 2. Student applies for Tech Innovation Scholarship (ID: 1)
```bash
curl -s -X POST http://localhost:5000/api/scholarships/1/apply \
  -H "Authorization: Bearer $TOKEN_STUDENT" \
  -H "Content-Type: application/json" \
  -d '{
    "cover_letter": "I am passionate about technology and innovation. With a CGPA of 8.5 and multiple projects...",
    "additional_info": "GitHub: github.com/sarahwilson, Portfolio: sarahwilson.dev"
  }' | jq
```

Expected: `201 Created` (or `400 Bad Request` if already applied)

#### 3. Student checks application status
```bash
curl -s http://localhost:5000/api/scholarships/applications/my \
  -H "Authorization: Bearer $TOKEN_STUDENT" | jq
```

#### 4. Alumni views applications for their scholarship
```bash
TOKEN_ALUMNI=$(curl -s -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@alumni.edu","password":"password123"}' \
  | jq -r '.access_token')

curl -s http://localhost:5000/api/scholarships/1/applications \
  -H "Authorization: Bearer $TOKEN_ALUMNI" | jq
```

**Expected response includes:**
- Student name, email, CGPA, category
- Application date and status
- Cover letter and additional info

#### 5. Alumni approves the application
```bash
# Get application ID from previous response, then:
curl -s -X PUT http://localhost:5000/api/scholarships/applications/1/status \
  -H "Authorization: Bearer $TOKEN_ALUMNI" \
  -H "Content-Type: application/json" \
  -d '{"status": "approved"}' | jq
```

#### 6. Student checks updated status
```bash
curl -s http://localhost:5000/api/scholarships/applications/my \
  -H "Authorization: Bearer $TOKEN_STUDENT" | jq
```

Status should now be: `approved`

---

## 🎨 View Student Profile with Statistics

```bash
# Get detailed profile for Sarah (ID: 4)
curl -s http://localhost:5000/api/users/4 | jq
```

**Expected response includes:**
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
  "mentorship_requests_count": 1,
  "created_at": "2024-..."
}
```

---

## 🔍 Explore the Database

### Connect to MySQL
```bash
docker exec -it $(docker ps -qf "name=db") mysql -u alumni_user -palumni_pass alumni_connect
```

### Run Sample Queries

#### 1. View all students with their CGPA
```sql
SELECT id, name, email, cgpa, category FROM users WHERE role = 'student';
```

#### 2. See scholarship eligibility matching
```sql
SELECT
    s.title,
    s.cgpa_requirement,
    s.category_requirement,
    COUNT(sa.id) as total_applications
FROM scholarships s
LEFT JOIN scholarship_applications sa ON s.id = sa.scholarship_id
WHERE s.status = 'active'
GROUP BY s.id, s.title, s.cgpa_requirement, s.category_requirement;
```

#### 3. Complex JOIN - Students with applications
```sql
SELECT
    u.name as student_name,
    u.cgpa,
    u.category,
    s.title as scholarship_title,
    s.amount,
    sa.status,
    sa.application_date
FROM users u
JOIN scholarship_applications sa ON u.id = sa.student_id
JOIN scholarships s ON sa.scholarship_id = s.id
ORDER BY sa.application_date DESC;
```

#### 4. Aggregation - Average CGPA by category
```sql
SELECT
    category,
    COUNT(*) as student_count,
    AVG(cgpa) as avg_cgpa,
    MIN(cgpa) as min_cgpa,
    MAX(cgpa) as max_cgpa
FROM users
WHERE role = 'student' AND cgpa IS NOT NULL
GROUP BY category;
```

---

## 📊 View Platform Statistics

```bash
TOKEN_ADMIN=$(curl -s -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@alumni.edu","password":"password123"}' \
  | jq -r '.access_token')

curl -s http://localhost:5000/api/admin/dashboard \
  -H "Authorization: Bearer $TOKEN_ADMIN" | jq
```

**Expected statistics:**
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
  },
  "mentorships": {
    "pending": 2
  },
  "applications": {
    "total": 2
  }
}
```

---

## 🚦 Verify Role-Based Access Control

### Test 1: Student tries to create scholarship (should fail)
```bash
TOKEN_STUDENT=$(curl -s -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"sarah@student.edu","password":"password123"}' \
  | jq -r '.access_token')

curl -s -X POST http://localhost:5000/api/scholarships \
  -H "Authorization: Bearer $TOKEN_STUDENT" \
  -H "Content-Type: application/json" \
  -d '{"title":"Test","amount":1000}' | jq
```

**Expected:** `403 Forbidden` - "Access denied"

### Test 2: Alumni tries to access admin dashboard (should fail)
```bash
TOKEN_ALUMNI=$(curl -s -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@alumni.edu","password":"password123"}' \
  | jq -r '.access_token')

curl -s http://localhost:5000/api/admin/dashboard \
  -H "Authorization: Bearer $TOKEN_ALUMNI" | jq
```

**Expected:** `403 Forbidden` - "Access denied"

---

## 📚 Next Steps

1. **Read the full documentation:**
   - [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - Complete API reference
   - [DATABASE_SCHEMA.md](DATABASE_SCHEMA.md) - Database design and queries
   - [TESTING_GUIDE.md](TESTING_GUIDE.md) - Comprehensive testing procedures
   - [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) - Technical details

2. **Explore the frontend:**
   - Open http://localhost:5173
   - Login with different roles
   - Test the user interface

3. **Customize the system:**
   - Add more demo users
   - Create additional scholarships
   - Test various eligibility scenarios

---

## 🛑 Stop the Application

```bash
docker compose down
```

To completely reset (including database):
```bash
docker compose down -v
docker compose up --build
```

---

## 🆘 Troubleshooting

### Database not ready
**Symptom:** Backend shows database connection errors

**Solution:** Wait 30-60 seconds for MySQL to fully initialize

### Port already in use
**Symptom:** Cannot start containers

**Solution:**
```bash
docker compose down
# Then start again
docker compose up --build
```

### Invalid token error
**Symptom:** API returns "Invalid token"

**Solution:** Token may have expired, login again to get a new token

---

## ✅ Success Checklist

After following this guide, you should have:
- [x] Started the application successfully
- [x] Logged in with different roles (admin, alumni, student)
- [x] Tested scholarship eligibility filtering
- [x] Applied for a scholarship as a student
- [x] Viewed applications as alumni
- [x] Used the unified search feature
- [x] Verified role-based access control
- [x] Viewed platform statistics
- [x] Ran sample database queries

**Congratulations!** You've successfully explored all major features of the enhanced Alumni Connect system.
