/*
  # Add Admin Role to Users Table

  1. Changes
    - Modify users.role ENUM to include 'admin' option
    - Update existing demo data to maintain backward compatibility
    - Add an admin user for testing

  2. Security
    - Admin role will be used for full CRUD operations
    - Default role remains 'student' for new registrations

  3. Notes
    - This migration is safe for existing data
    - All existing users retain their current roles
*/

USE alumni_connect;

-- Modify the role column to include 'admin'
ALTER TABLE users
  MODIFY COLUMN role ENUM('alumni','student','admin') NOT NULL DEFAULT 'student';

-- Insert an admin user for testing
INSERT INTO users (email, password_hash, name, role, graduation_year, major, bio, skills) VALUES
  ('admin@alumni.edu', '$2b$12$CgkJxu49qllIpCNNTwaVQu6wCeojAewFfBBmCokbwhW3k/djaCT2e', 'System Admin', 'admin', NULL, 'Administration', 'Platform administrator with full system access.', 'Platform Management, User Administration, System Configuration')
ON DUPLICATE KEY UPDATE name=VALUES(name);
