/*
  # Enhance Student Profile System

  1. New Columns
    - cgpa DECIMAL(3,2) - Student CGPA (0.00 to 10.00)
    - category VARCHAR(50) - Student category (e.g., General, OBC, SC/ST, etc.)
    - phone VARCHAR(15) - Contact phone number
    - email_verified BOOLEAN - Email verification status

  2. Constraints
    - CHECK constraint for CGPA range (0.00 to 10.00)
    - email already has UNIQUE constraint
    - email already has NOT NULL constraint

  3. Notes
    - Backward compatible with existing records (all new columns are nullable)
    - email column already exists with proper constraints
    - Existing student records remain valid
*/

USE alumni_connect;

-- Add new columns to users table for enhanced student profiles
ALTER TABLE users
  ADD COLUMN IF NOT EXISTS cgpa DECIMAL(3,2) NULL
    CHECK (cgpa >= 0.00 AND cgpa <= 10.00),
  ADD COLUMN IF NOT EXISTS category VARCHAR(50) NULL,
  ADD COLUMN IF NOT EXISTS phone VARCHAR(15) NULL,
  ADD COLUMN IF NOT EXISTS email_verified BOOLEAN DEFAULT FALSE;

-- Update existing student records with sample data
UPDATE users SET cgpa = 8.5, category = 'General', phone = '555-0103' WHERE email = 'sarah@student.edu';
UPDATE users SET cgpa = 7.8, category = 'OBC', phone = '555-0104' WHERE email = 'mike@student.edu';

-- Add index on frequently queried columns for better performance
CREATE INDEX IF NOT EXISTS idx_users_cgpa ON users(cgpa);
CREATE INDEX IF NOT EXISTS idx_users_category ON users(category);
CREATE INDEX IF NOT EXISTS idx_users_name ON users(name);
