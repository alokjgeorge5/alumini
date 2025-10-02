/*
  # Complete Scholarship Management System

  1. Changes to scholarships table
    - Add eligibility_criteria TEXT
    - Add cgpa_requirement DECIMAL(3,2)
    - Add category_requirement VARCHAR(50)
    - Add status ENUM for scholarship lifecycle
    - Rename posted_by to created_by for consistency

  2. New scholarship_applications table
    - Tracks student applications to scholarships
    - Prevents duplicate applications with composite primary key
    - Links to both students and scholarships via foreign keys
    - Tracks application status and timeline

  3. Security
    - Foreign key constraints ensure referential integrity
    - Composite primary key prevents duplicate applications
    - Status field enables workflow management

  4. Notes
    - Eligibility filtering will use cgpa_requirement and category_requirement
    - Alumni can create scholarships (created_by references users)
    - Students can apply (student_id references users with role='student')
    - Admin can manage all scholarships and applications
*/

USE alumni_connect;

-- Drop the old scholarships table and recreate with enhanced structure
DROP TABLE IF EXISTS scholarship_applications;
DROP TABLE IF EXISTS scholarships;

-- Create enhanced scholarships table
CREATE TABLE scholarships (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(200) NOT NULL,
  description TEXT,
  eligibility_criteria TEXT,
  cgpa_requirement DECIMAL(3,2) DEFAULT 0.00,
  category_requirement VARCHAR(50) NULL,
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

-- Create scholarship_applications table
CREATE TABLE scholarship_applications (
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

-- Insert sample scholarships with eligibility requirements
INSERT INTO scholarships (title, description, eligibility_criteria, cgpa_requirement, category_requirement, amount, deadline, created_by, status) VALUES
  ('Tech Innovation Scholarship',
   'For students pursuing technology and innovation with excellent academic records.',
   'Must be enrolled in CS/IT program, demonstrate innovation through projects, and maintain strong academic standing.',
   7.5,
   NULL,
   5000.00,
   '2024-12-31',
   1,
   'active'),

  ('Business Leadership Award',
   'Supporting future business leaders with demonstrated leadership experience.',
   'Business major with proven leadership in extracurricular activities or organizations.',
   7.0,
   NULL,
   3000.00,
   '2024-11-30',
   2,
   'active'),

  ('Diversity Excellence Scholarship',
   'Promoting diversity in technology by supporting underrepresented students.',
   'Open to students from OBC/SC/ST categories pursuing STEM fields.',
   6.5,
   'OBC',
   7500.00,
   '2025-01-15',
   1,
   'active'),

  ('Merit-Based Academic Scholarship',
   'Recognizing outstanding academic achievement across all disciplines.',
   'Top 10% of class with exceptional CGPA and consistent academic performance.',
   8.5,
   'General',
   10000.00,
   '2024-12-15',
   2,
   'active');

-- Insert sample scholarship applications
INSERT INTO scholarship_applications (student_id, scholarship_id, status, cover_letter) VALUES
  (3, 1, 'submitted', 'I am passionate about technology and have developed several innovative projects during my studies. My CGPA of 8.5 reflects my dedication to academic excellence.'),
  (4, 2, 'under_review', 'As a business student with leadership experience in multiple clubs, I believe I embody the qualities this scholarship seeks to recognize.');
