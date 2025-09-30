const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
require('dotenv').config({ path: path.join(__dirname, '..', 'backend', '.env') });

console.log('🔧 Setting up Alumni Connect Database...\n');

// Check if .env file exists
const envPath = path.join(__dirname, '..', 'backend', '.env');
if (!fs.existsSync(envPath)) {
  console.error('❌ Error: backend/.env file not found!');
  console.log('Please create backend/.env file with your database configuration.');
  console.log('See backend/.env.example for reference.');
  process.exit(1);
}

// Get database configuration from environment variables
const dbConfig = {
  host: process.env.DATABASE_HOST || 'localhost',
  user: process.env.DATABASE_USER || 'root',
  password: process.env.DATABASE_PASSWORD,
  database: process.env.DATABASE_NAME || 'alumni_connect'
};

// Validate required configuration
if (!dbConfig.password) {
  console.error('❌ Error: DATABASE_PASSWORD not found in backend/.env file!');
  console.log('Please set DATABASE_PASSWORD in your backend/.env file.');
  process.exit(1);
}

console.log(`📊 Database Configuration:`);
console.log(`   Host: ${dbConfig.host}`);
console.log(`   User: ${dbConfig.user}`);
console.log(`   Database: ${dbConfig.database}\n`);

try {
  // Check if MySQL is accessible
  console.log('🔍 Checking MySQL connection...');
  execSync(`mysql -h ${dbConfig.host} -u ${dbConfig.user} -p${dbConfig.password} -e "SELECT 1;" 2>/dev/null`, { stdio: 'pipe' });
  console.log('✅ MySQL connection successful!\n');

  // Import the database schema and seed data
  console.log('📥 Importing database schema and seed data...');
  const sqlFilePath = path.join(__dirname, '..', 'database', 'alumni_connect.sql');
  
  if (!fs.existsSync(sqlFilePath)) {
    console.error('❌ Error: database/alumni_connect.sql file not found!');
    process.exit(1);
  }

  execSync(`mysql -h ${dbConfig.host} -u ${dbConfig.user} -p${dbConfig.password} < "${sqlFilePath}"`, { stdio: 'inherit' });
  console.log('✅ Database setup completed successfully!\n');

  // Verify database was created
  console.log('🔍 Verifying database setup...');
  const result = execSync(`mysql -h ${dbConfig.host} -u ${dbConfig.user} -p${dbConfig.password} -e "USE ${dbConfig.database}; SHOW TABLES;" 2>/dev/null`, { encoding: 'utf8' });
  
  if (result.includes('users') && result.includes('opportunities')) {
    console.log('✅ Database verification successful!');
    console.log('🎉 Alumni Connect database is ready to use!\n');
  } else {
    console.log('⚠️  Warning: Database setup may be incomplete. Please check manually.');
  }

} catch (error) {
  console.error('❌ Database setup failed!');
  console.error('Error details:', error.message);
  console.log('\n🔧 Troubleshooting tips:');
  console.log('1. Make sure MySQL server is running');
  console.log('2. Verify your database credentials in backend/.env');
  console.log('3. Ensure your MySQL user has CREATE/DROP database privileges');
  console.log('4. Check if the database/alumni_connect.sql file exists');
  process.exit(1);
}