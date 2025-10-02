CREATE DATABASE IF NOT EXISTS alumni_connect;
USE alumni_connect;

-- Users table with authentication and enhanced fields
CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  name VARCHAR(100) NOT NULL,
  role ENUM('alumni','student','admin') NOT NULL DEFAULT 'student',
  graduation_year INT,
  major VARCHAR(100),
  company VARCHAR(100),
  position VARCHAR(100),
  bio TEXT,
  skills TEXT,
  cgpa DECIMAL(3,2) CHECK (cgpa >= 0.00 AND cgpa <= 10.00),
  category VARCHAR(50),
  phone VARCHAR(15),
  email_verified BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_users_name (name),
  INDEX idx_users_cgpa (cgpa),
  INDEX idx_users_category (category)
);

-- Job/Internship postings
CREATE TABLE IF NOT EXISTS opportunities (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(200) NOT NULL,
  company VARCHAR(100) NOT NULL,
  description TEXT,
  requirements TEXT,
  location VARCHAR(100),
  salary_range VARCHAR(50),
  type ENUM('full-time','part-time','internship','contract') NOT NULL,
  posted_by INT,
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (posted_by) REFERENCES users(id)
);

-- Scholarships with enhanced eligibility criteria
CREATE TABLE IF NOT EXISTS scholarships (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(200) NOT NULL,
  description TEXT,
  eligibility_criteria TEXT,
  cgpa_requirement DECIMAL(3,2) DEFAULT 0.00,
  category_requirement VARCHAR(50),
  amount DECIMAL(10,2),
  deadline DATE,
  created_by INT NOT NULL,
  status ENUM('active','inactive','closed') DEFAULT 'active',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE CASCADE,
  INDEX idx_scholarship_cgpa (cgpa_requirement),
  INDEX idx_scholarship_category (category_requirement),
  INDEX idx_scholarship_status (status)
);

-- Scholarship applications
CREATE TABLE IF NOT EXISTS scholarship_applications (
  id INT AUTO_INCREMENT PRIMARY KEY,
  student_id INT NOT NULL,
  scholarship_id INT NOT NULL,
  application_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  status ENUM('submitted','under_review','approved','rejected') DEFAULT 'submitted',
  cover_letter TEXT,
  additional_info TEXT,
  FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY (scholarship_id) REFERENCES scholarships(id) ON DELETE CASCADE,
  UNIQUE KEY unique_application (student_id, scholarship_id),
  INDEX idx_application_status (status),
  INDEX idx_application_date (application_date)
);

-- Mentorship requests
CREATE TABLE IF NOT EXISTS mentorship_requests (
  id INT AUTO_INCREMENT PRIMARY KEY,
  student_id INT NOT NULL,
  mentor_id INT NOT NULL,
  subject VARCHAR(200) NOT NULL,
  message TEXT,
  status ENUM('pending','accepted','rejected','completed') DEFAULT 'pending',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (student_id) REFERENCES users(id),
  FOREIGN KEY (mentor_id) REFERENCES users(id)
);

-- Applications for jobs/scholarships
CREATE TABLE IF NOT EXISTS applications (
  id INT AUTO_INCREMENT PRIMARY KEY,
  applicant_id INT NOT NULL,
  opportunity_id INT,
  scholarship_id INT,
  type ENUM('job','scholarship') NOT NULL,
  status ENUM('submitted','under_review','accepted','rejected') DEFAULT 'submitted',
  cover_letter TEXT,
  resume_url VARCHAR(500),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (applicant_id) REFERENCES users(id),
  FOREIGN KEY (opportunity_id) REFERENCES opportunities(id),
  FOREIGN KEY (scholarship_id) REFERENCES scholarships(id)
);

-- Messages between users
CREATE TABLE IF NOT EXISTS messages (
  id INT AUTO_INCREMENT PRIMARY KEY,
  sender_id INT NOT NULL,
  receiver_id INT NOT NULL,
  subject VARCHAR(200),
  content TEXT NOT NULL,
  is_read BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (sender_id) REFERENCES users(id),
  FOREIGN KEY (receiver_id) REFERENCES users(id)
);

-- Success stories
CREATE TABLE IF NOT EXISTS stories (
  id INT AUTO_INCREMENT PRIMARY KEY,
  author_id INT NOT NULL,
  title VARCHAR(200) NOT NULL,
  content TEXT NOT NULL,
  category VARCHAR(100),
  is_featured BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (author_id) REFERENCES users(id)
);

-- Insert demo data with enhanced fields
INSERT INTO users (email, password_hash, name, role, graduation_year, major, company, position, bio, skills, cgpa, category, phone) VALUES
  ('admin@alumni.edu', '$2b$12$CgkJxu49qllIpCNNTwaVQu6wCeojAewFfBBmCokbwhW3k/djaCT2e', 'System Admin', 'admin', NULL, 'Administration', NULL, NULL, 'Platform administrator with full system access.', 'Platform Management, User Administration, System Configuration', NULL, NULL, '555-0100'),
  ('alice@alumni.edu', '$2b$12$CgkJxu49qllIpCNNTwaVQu6wCeojAewFfBBmCokbwhW3k/djaCT2e', 'Alice Johnson', 'alumni', 2020, 'Computer Science', 'Google', 'Software Engineer', 'Passionate about helping students succeed in tech careers.', 'Python, JavaScript, React, Machine Learning', NULL, NULL, '555-0101'),
  ('bob@alumni.edu', '$2b$12$CgkJxu49qllIpCNNTwaVQu6wCeojAewFfBBmCokbwhW3k/djaCT2e', 'Bob Smith', 'alumni', 2019, 'Business Administration', 'Microsoft', 'Product Manager', 'Experienced in product strategy and team leadership.', 'Product Management, Strategy, Leadership', NULL, NULL, '555-0102'),
  ('sarah@student.edu', '$2b$12$CgkJxu49qllIpCNNTwaVQu6wCeojAewFfBBmCokbwhW3k/djaCT2e', 'Sarah Wilson', 'student', 2024, 'Computer Science', NULL, NULL, 'Final year CS student looking for internship opportunities.', 'Java, Python, Web Development', 8.5, 'General', '555-0103'),
  ('mike@student.edu', '$2b$12$CgkJxu49qllIpCNNTwaVQu6wCeojAewFfBBmCokbwhW3k/djaCT2e', 'Mike Davis', 'student', 2025, 'Business Administration', NULL, NULL, 'Sophomore business student interested in entrepreneurship.', 'Business Analysis, Marketing, Finance', 7.8, 'OBC', '555-0104')
ON DUPLICATE KEY UPDATE name=VALUES(name);

INSERT INTO opportunities (title, company, description, requirements, location, salary_range, type, posted_by) VALUES
  ('Software Engineering Intern', 'Google', 'Join our team for a 12-week summer internship working on cutting-edge projects.', 'Python, JavaScript, CS fundamentals', 'Mountain View, CA', '$8,000/month', 'internship', 2),
  ('Product Management Intern', 'Microsoft', 'Work with our product team to define and deliver user experiences.', 'Business acumen, communication skills', 'Seattle, WA', '$7,500/month', 'internship', 3),
  ('Full Stack Developer', 'StartupXYZ', 'Build web applications using modern technologies.', 'React, Node.js, SQL', 'Remote', '$80,000-120,000', 'full-time', 2)
ON DUPLICATE KEY UPDATE title=VALUES(title);

INSERT INTO scholarships (title, description, eligibility_criteria, cgpa_requirement, category_requirement, amount, deadline, created_by, status) VALUES
  ('Tech Innovation Scholarship', 'For students pursuing technology and innovation with excellent academic records.', 'Must be enrolled in CS/IT program, demonstrate innovation through projects, and maintain strong academic standing.', 7.5, NULL, 5000.00, '2024-12-31', 2, 'active'),
  ('Business Leadership Award', 'Supporting future business leaders with demonstrated leadership experience.', 'Business major with proven leadership in extracurricular activities or organizations.', 7.0, NULL, 3000.00, '2024-11-30', 3, 'active'),
  ('Diversity Excellence Scholarship', 'Promoting diversity in technology by supporting underrepresented students.', 'Open to students from OBC/SC/ST categories pursuing STEM fields.', 6.5, 'OBC', 7500.00, '2025-01-15', 2, 'active'),
  ('Merit-Based Academic Scholarship', 'Recognizing outstanding academic achievement across all disciplines.', 'Top 10% of class with exceptional CGPA and consistent academic performance.', 8.5, 'General', 10000.00, '2024-12-15', 3, 'active')
ON DUPLICATE KEY UPDATE title=VALUES(title);

INSERT INTO mentorship_requests (student_id, mentor_id, subject, message, status) VALUES
  (4, 2, 'Career Guidance in Tech', 'I would love to learn about your journey from student to Google engineer.', 'accepted'),
  (5, 3, 'Product Management Career', 'Interested in understanding product management roles.', 'pending')
ON DUPLICATE KEY UPDATE subject=VALUES(subject);

INSERT INTO applications (applicant_id, opportunity_id, type, status, cover_letter) VALUES
  (4, 1, 'job', 'submitted', 'I am excited to apply for the Software Engineering Intern position...'),
  (5, 2, 'job', 'under_review', 'My business background and passion for technology make me a great fit...')
ON DUPLICATE KEY UPDATE cover_letter=VALUES(cover_letter);

INSERT INTO scholarship_applications (student_id, scholarship_id, status, cover_letter) VALUES
  (4, 1, 'submitted', 'I am passionate about technology and have developed several innovative projects during my studies. My CGPA of 8.5 reflects my dedication to academic excellence.'),
  (5, 2, 'under_review', 'As a business student with leadership experience in multiple clubs, I believe I embody the qualities this scholarship seeks to recognize.')
ON DUPLICATE KEY UPDATE cover_letter=VALUES(cover_letter);

INSERT INTO stories (author_id, title, content, category, is_featured) VALUES
  (2, 'From Campus to Google: My Journey', 'Starting as a CS student, I never imagined I would end up at Google...', 'Career Success', TRUE),
  (3, 'Building Products That Matter', 'Product management taught me that technology is about solving real problems...', 'Career Advice', FALSE)
ON DUPLICATE KEY UPDATE title=VALUES(title);


