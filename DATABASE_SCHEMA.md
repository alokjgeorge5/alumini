# Alumni Connect - Database Schema Documentation

## Entity-Relationship Diagram Description

### Entities and Relationships

```
┌──────────────────────────────────────────────────────────────────────┐
│                      ALUMNI CONNECT ER DIAGRAM                        │
└──────────────────────────────────────────────────────────────────────┘

USERS (1) ──────creates────── (M) OPPORTUNITIES
  │                                      │
  │                                      │
  │                            (M) APPLICATIONS (M)
  │                                      │
  │                                      │
USERS (1) ──────creates────── (M) SCHOLARSHIPS
  │                                      │
  │                                      │
  │                            (M) SCHOLARSHIP_APPLICATIONS (M)
  │                                      │
  │                                      │
USERS (Student) (M) ──requests── (M) MENTORSHIP_REQUESTS ──accepted_by── (1) USERS (Alumni)
  │
  │
USERS (1) ──────sends────── (M) MESSAGES ──────receives────── (1) USERS
  │
  │
USERS (1) ──────writes────── (M) STORIES
```

## Table Definitions

### 1. USERS
Primary table storing all user accounts (students, alumni, admins).

**Columns:**
- `id` INT PRIMARY KEY AUTO_INCREMENT
- `email` VARCHAR(255) UNIQUE NOT NULL
- `password_hash` VARCHAR(255) NOT NULL
- `name` VARCHAR(100) NOT NULL
- `role` ENUM('alumni','student','admin') NOT NULL DEFAULT 'student'
- `graduation_year` INT
- `major` VARCHAR(100)
- `company` VARCHAR(100) - For alumni
- `position` VARCHAR(100) - For alumni
- `bio` TEXT
- `skills` TEXT
- `cgpa` DECIMAL(3,2) CHECK (cgpa >= 0.00 AND cgpa <= 10.00) - For students
- `category` VARCHAR(50) - For scholarship eligibility (e.g., General, OBC, SC/ST)
- `phone` VARCHAR(15)
- `email_verified` BOOLEAN DEFAULT FALSE
- `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP

**Indexes:**
- PRIMARY KEY (id)
- UNIQUE INDEX (email)
- INDEX idx_users_name (name)
- INDEX idx_users_cgpa (cgpa)
- INDEX idx_users_category (category)

**Constraints:**
- UNIQUE(email)
- CHECK(cgpa BETWEEN 0.00 AND 10.00)

**Normalization:** 3NF
- No repeating groups
- All non-key attributes fully dependent on primary key
- No transitive dependencies

---

### 2. OPPORTUNITIES
Job and internship postings created by alumni.

**Columns:**
- `id` INT PRIMARY KEY AUTO_INCREMENT
- `title` VARCHAR(200) NOT NULL
- `company` VARCHAR(100) NOT NULL
- `description` TEXT
- `requirements` TEXT
- `location` VARCHAR(100)
- `salary_range` VARCHAR(50)
- `type` ENUM('full-time','part-time','internship','contract') NOT NULL
- `posted_by` INT - Foreign key to USERS(id)
- `is_active` BOOLEAN DEFAULT TRUE
- `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP

**Relationships:**
- N:1 with USERS (posted_by → users.id)
- 1:N with APPLICATIONS

**Constraints:**
- FOREIGN KEY (posted_by) REFERENCES users(id)

---

### 3. SCHOLARSHIPS
Scholarship opportunities with eligibility criteria.

**Columns:**
- `id` INT PRIMARY KEY AUTO_INCREMENT
- `title` VARCHAR(200) NOT NULL
- `description` TEXT
- `eligibility_criteria` TEXT - Detailed eligibility description
- `cgpa_requirement` DECIMAL(3,2) DEFAULT 0.00 - Minimum CGPA required
- `category_requirement` VARCHAR(50) - Required student category
- `amount` DECIMAL(10,2)
- `deadline` DATE
- `created_by` INT NOT NULL - Foreign key to USERS(id)
- `status` ENUM('active','inactive','closed') DEFAULT 'active'
- `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP

**Indexes:**
- PRIMARY KEY (id)
- INDEX idx_scholarship_cgpa (cgpa_requirement)
- INDEX idx_scholarship_category (category_requirement)
- INDEX idx_scholarship_status (status)

**Relationships:**
- N:1 with USERS (created_by → users.id)
- 1:N with SCHOLARSHIP_APPLICATIONS

**Constraints:**
- FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE CASCADE

**Eligibility Logic:**
```sql
WHERE (cgpa_requirement IS NULL OR student.cgpa >= scholarship.cgpa_requirement)
  AND (category_requirement IS NULL OR student.category = scholarship.category_requirement)
```

---

### 4. SCHOLARSHIP_APPLICATIONS
Bridge table tracking student applications to scholarships.

**Columns:**
- `id` INT PRIMARY KEY AUTO_INCREMENT
- `student_id` INT NOT NULL - Foreign key to USERS(id)
- `scholarship_id` INT NOT NULL - Foreign key to SCHOLARSHIPS(id)
- `application_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
- `status` ENUM('submitted','under_review','approved','rejected') DEFAULT 'submitted'
- `cover_letter` TEXT
- `additional_info` TEXT

**Indexes:**
- PRIMARY KEY (id)
- UNIQUE KEY unique_application (student_id, scholarship_id)
- INDEX idx_application_status (status)
- INDEX idx_application_date (application_date)

**Relationships:**
- N:1 with USERS (student_id → users.id)
- N:1 with SCHOLARSHIPS (scholarship_id → scholarships.id)

**Constraints:**
- FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE
- FOREIGN KEY (scholarship_id) REFERENCES scholarships(id) ON DELETE CASCADE
- UNIQUE(student_id, scholarship_id) - Prevents duplicate applications

**Cardinality:** M:N between USERS and SCHOLARSHIPS

---

### 5. MENTORSHIP_REQUESTS
Mentorship requests from students to alumni.

**Columns:**
- `id` INT PRIMARY KEY AUTO_INCREMENT
- `student_id` INT NOT NULL - Foreign key to USERS(id)
- `mentor_id` INT NOT NULL - Foreign key to USERS(id)
- `subject` VARCHAR(200) NOT NULL
- `message` TEXT
- `status` ENUM('pending','accepted','rejected','completed') DEFAULT 'pending'
- `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP

**Relationships:**
- N:1 with USERS (student_id → users.id where role='student')
- N:1 with USERS (mentor_id → users.id where role='alumni')

**Constraints:**
- FOREIGN KEY (student_id) REFERENCES users(id)
- FOREIGN KEY (mentor_id) REFERENCES users(id)

---

### 6. APPLICATIONS
Job/opportunity applications from students.

**Columns:**
- `id` INT PRIMARY KEY AUTO_INCREMENT
- `applicant_id` INT NOT NULL - Foreign key to USERS(id)
- `opportunity_id` INT - Foreign key to OPPORTUNITIES(id)
- `scholarship_id` INT - Foreign key to SCHOLARSHIPS(id)
- `type` ENUM('job','scholarship') NOT NULL
- `status` ENUM('submitted','under_review','accepted','rejected') DEFAULT 'submitted'
- `cover_letter` TEXT
- `resume_url` VARCHAR(500)
- `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP

**Relationships:**
- N:1 with USERS (applicant_id → users.id)
- N:1 with OPPORTUNITIES (opportunity_id → opportunities.id)

**Constraints:**
- FOREIGN KEY (applicant_id) REFERENCES users(id)
- FOREIGN KEY (opportunity_id) REFERENCES opportunities(id)
- FOREIGN KEY (scholarship_id) REFERENCES scholarships(id)

---

### 7. MESSAGES
Direct messages between users.

**Columns:**
- `id` INT PRIMARY KEY AUTO_INCREMENT
- `sender_id` INT NOT NULL - Foreign key to USERS(id)
- `receiver_id` INT NOT NULL - Foreign key to USERS(id)
- `subject` VARCHAR(200)
- `content` TEXT NOT NULL
- `is_read` BOOLEAN DEFAULT FALSE
- `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP

**Relationships:**
- N:1 with USERS (sender_id → users.id)
- N:1 with USERS (receiver_id → users.id)

**Constraints:**
- FOREIGN KEY (sender_id) REFERENCES users(id)
- FOREIGN KEY (receiver_id) REFERENCES users(id)

---

### 8. STORIES
Success stories and experiences shared by users.

**Columns:**
- `id` INT PRIMARY KEY AUTO_INCREMENT
- `author_id` INT NOT NULL - Foreign key to USERS(id)
- `title` VARCHAR(200) NOT NULL
- `content` TEXT NOT NULL
- `category` VARCHAR(100)
- `is_featured` BOOLEAN DEFAULT FALSE
- `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP

**Relationships:**
- N:1 with USERS (author_id → users.id)

**Constraints:**
- FOREIGN KEY (author_id) REFERENCES users(id)

---

## Normalization Analysis

### First Normal Form (1NF)
✅ All tables have:
- Atomic values in each column
- No repeating groups
- Primary key defined

### Second Normal Form (2NF)
✅ All tables have:
- Met 1NF requirements
- All non-key attributes fully functionally dependent on the entire primary key
- No partial dependencies

### Third Normal Form (3NF)
✅ All tables have:
- Met 2NF requirements
- No transitive dependencies
- All non-key attributes directly dependent on primary key only

**Example Analysis:**

**USERS Table:**
- Primary Key: id
- email → determined by id (not by other non-key attributes)
- name → determined by id
- cgpa → determined by id (not determined by any other non-key attribute)
- No transitive dependencies exist

**SCHOLARSHIPS Table:**
- Primary Key: id
- title, amount, deadline → all determined by id
- created_by is a foreign key (references USERS table)
- cgpa_requirement → determined by id (scholarship-specific criteria)
- No transitive dependencies

---

## Query Performance Optimizations

### Indexes Created for Optimal Performance:

1. **Users Table:**
   - `idx_users_name` - For name searches
   - `idx_users_cgpa` - For scholarship eligibility queries
   - `idx_users_category` - For category-based filtering

2. **Scholarships Table:**
   - `idx_scholarship_cgpa` - For eligibility filtering
   - `idx_scholarship_category` - For category matching
   - `idx_scholarship_status` - For active/inactive filtering

3. **Scholarship Applications Table:**
   - `unique_application (student_id, scholarship_id)` - Prevents duplicates
   - `idx_application_status` - For status filtering
   - `idx_application_date` - For chronological sorting

### Expected Query Performance:
- Simple SELECT by ID: < 5ms
- Filtered searches with indexes: < 50ms
- Complex JOINs (2-3 tables): < 100ms
- Full-text search across entities: < 150ms

---

## Sample Complex Queries

### 1. Complex JOIN - Students with Scholarship Applications
```sql
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

### 2. UNION - Global Search
```sql
SELECT 'student' as type, id, name as title, bio as description
FROM users WHERE role = 'student' AND name LIKE '%term%'

UNION

SELECT 'alumni' as type, id, name as title, bio as description
FROM users WHERE role = 'alumni' AND name LIKE '%term%'

UNION

SELECT 'opportunity' as type, id, title, description
FROM opportunities WHERE title LIKE '%term%'

UNION

SELECT 'scholarship' as type, id, title, description
FROM scholarships WHERE title LIKE '%term%';
```

### 3. Aggregation - Application Statistics
```sql
SELECT
    s.id, s.title, s.amount,
    COUNT(sa.id) as total_applications,
    SUM(CASE WHEN sa.status = 'approved' THEN 1 ELSE 0 END) as approved_count,
    SUM(CASE WHEN sa.status = 'rejected' THEN 1 ELSE 0 END) as rejected_count,
    AVG(u.cgpa) as avg_applicant_cgpa
FROM scholarships s
LEFT JOIN scholarship_applications sa ON s.id = sa.scholarship_id
LEFT JOIN users u ON sa.student_id = u.id
GROUP BY s.id, s.title, s.amount
HAVING COUNT(sa.id) > 0
ORDER BY total_applications DESC;
```

### 4. Subquery - Eligible Students for High-Value Scholarships
```sql
SELECT u.id, u.name, u.email, u.cgpa, u.category
FROM users u
WHERE u.role = 'student'
  AND u.id IN (
    SELECT DISTINCT student_id
    FROM scholarship_applications sa
    JOIN scholarships s ON sa.scholarship_id = s.id
    WHERE s.amount > 5000
      AND sa.status = 'approved'
  )
ORDER BY u.cgpa DESC;
```

### 5. Eligibility Check with Subquery
```sql
SELECT s.id, s.title, s.amount, s.cgpa_requirement, s.category_requirement
FROM scholarships s
WHERE s.status = 'active'
  AND s.id NOT IN (
    SELECT scholarship_id
    FROM scholarship_applications
    WHERE student_id = :student_id
  )
  AND (s.cgpa_requirement IS NULL OR s.cgpa_requirement <= (
    SELECT cgpa FROM users WHERE id = :student_id
  ))
  AND (s.category_requirement IS NULL OR s.category_requirement = (
    SELECT category FROM users WHERE id = :student_id
  ));
```

---

## Referential Integrity

All foreign key relationships enforce CASCADE on DELETE to maintain data integrity:

- When a USER is deleted, all related records are automatically removed
- When a SCHOLARSHIP is deleted, all applications are removed
- This prevents orphaned records and maintains database consistency

---

## Security Considerations

1. **Password Storage:** Uses bcrypt hashing (never stores plain text)
2. **Role-Based Access:** Enforced at application level via middleware
3. **Input Validation:** All inputs validated before database operations
4. **SQL Injection Prevention:** Uses parameterized queries via SQLAlchemy
5. **Foreign Key Constraints:** Ensures data integrity at database level
