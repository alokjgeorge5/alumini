# Alumni Connect (Dockerized Vite + Flask + MySQL)

One-command local dev with Docker. Frontend: Vite + React 18. Backend: Flask. DB: MySQL 8.

## Quick start

Prereqs: Docker Desktop running.

```
docker compose up --build
```

Open:
- Frontend: http://localhost:5173
- Backend health: http://localhost:5000/api/health

## Services
- `new-frontend/` Vite React app hitting `/api/*`
- `new-backend/` Flask app with CORS enabled
- `db/init.sql` schema + seed
- `docker-compose.yml` wires services

## 🚀 Features

### For Students:
- Browse job opportunities and internships
- **NEW:** View scholarships eligible based on CGPA and category
- **NEW:** Apply for scholarships with cover letter and additional info
- **NEW:** Track scholarship application status (submitted, under review, approved, rejected)
- **NEW:** Enhanced profile with CGPA, category, and contact information
- **NEW:** View application statistics on profile
- Find mentors based on skills and interests
- Share success stories
- **NEW:** Use unified search to find opportunities, scholarships, and alumni

### For Alumni:
- Post job openings and internships
- **NEW:** Create scholarships with eligibility criteria (CGPA, category)
- **NEW:** View and manage applications for your scholarships
- **NEW:** Update application statuses (approve/reject)
- Offer mentorship services
- Connect with students
- **NEW:** Full CRUD operations on your opportunities and scholarships

### For Admins:
- **NEW:** View comprehensive platform statistics dashboard
- **NEW:** Manage all users (create, update, delete)
- **NEW:** Manage all opportunities and scholarships
- **NEW:** View all applications across the platform
- **NEW:** Full administrative control over all entities

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- MySQL 8.0+
- npm or yarn

## Stop
```
docker compose down
```

### Manual Setup (Alternative)

If you prefer to set up components individually:

#### 1. Prerequisites
- Node.js 16+
- Python 3.8+
- MySQL 8.0+ (running)
- npm or yarn

#### 2. Environment Configuration

Create your environment file:
```bash
cp backend/.env.example backend/.env
```

Edit `backend/.env` with your actual values:
```env
DATABASE_HOST=localhost
DATABASE_USER=root
DATABASE_PASSWORD=your_actual_mysql_password
DATABASE_NAME=alumni_connect
JWT_SECRET_KEY=your_jwt_secret_key_here
```

Env defaults:
- DB: alumni_connect
- User: alumni_user / alumni_pass
Override via compose env if needed.

#### 4. Database Setup
```bash
npm run db:reset
```

#### 5. Start Development Servers
```bash
npm run dev
```

## 🚀 Available Scripts

- `npm start` - **Single command setup and start** (recommended for new developers)
- `npm run setup-and-start` - Same as `npm start`
- `npm run dev` - Start both frontend and backend (assumes setup is done)
- `npm run setup` - Install all dependencies and set up database
- `npm run install-deps` - Install Node.js and Python dependencies only
- `npm run db:reset` - Reset and seed the database
- `npm run build` - Build frontend for production

## 🔧 Development Workflow

### For New Developers
1. Clone the repository
2. Copy `backend/.env.example` to `backend/.env`
3. Update `DATABASE_PASSWORD` in `backend/.env`
4. Run `npm start`
5. Access the application at `http://localhost:3000`

### For Existing Developers
```bash
# Just start the servers (if already set up)
npm run dev

# Reset database with fresh data
npm run db:reset

# Reinstall dependencies after pulling changes
npm run install-deps
```

## 🏥 Health Checks

The setup script includes automatic health checks:
- ✅ MySQL connection verification
- ✅ Database creation confirmation
- ✅ Table structure validation
- ✅ Dependency installation verification

## 🐛 Troubleshooting

### Database Issues
- **"MySQL connection failed"**: Ensure MySQL server is running
- **"Access denied"**: Check DATABASE_PASSWORD in backend/.env
- **"Database not found"**: The script will create it automatically

### Permission Issues
- Ensure your MySQL user has CREATE/DROP database privileges
- On Windows, you may need to run the terminal as Administrator

### Port Conflicts
- Frontend runs on `http://localhost:3000`
- Backend runs on `http://localhost:5000`
- Ensure these ports are available

## Project Structure
```
new-frontend/
new-backend/
db/init.sql
docker-compose.yml
```

## 🔗 API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user

### Users
- `GET /api/users` - List all users
- `GET /api/users/:id` - Get user profile with statistics
- `PUT /api/users/profile` - Update user profile
- `GET /api/users/alumni` - Get all alumni
- `GET /api/users/students` - Get all students

### Opportunities
- `GET /api/opportunities` - Get all opportunities
- `GET /api/opportunities/:id` - Get opportunity details
- `POST /api/opportunities` - Create new opportunity (Alumni/Admin)
- `PUT /api/opportunities/:id` - Update opportunity (Owner/Admin)
- `DELETE /api/opportunities/:id` - Delete opportunity (Owner/Admin)

### Scholarships
- `GET /api/scholarships` - Get all active scholarships
- `GET /api/scholarships/:id` - Get scholarship details
- `GET /api/scholarships/eligible` - Get eligible scholarships (Student)
- `POST /api/scholarships` - Create scholarship (Alumni/Admin)
- `PUT /api/scholarships/:id` - Update scholarship (Owner/Admin)
- `DELETE /api/scholarships/:id` - Delete scholarship (Owner/Admin)
- `POST /api/scholarships/:id/apply` - Apply for scholarship (Student)
- `GET /api/scholarships/:id/applications` - View applications (Owner/Admin)
- `GET /api/scholarships/applications/my` - View own applications (Student)
- `PUT /api/scholarships/applications/:id/status` - Update status (Owner/Admin)

### Search
- `GET /api/search?query=:term` - Unified search across all entities

### Admin
- `GET /api/admin/dashboard` - Platform statistics (Admin)
- `GET /api/admin/users` - List all users (Admin)
- `POST /api/admin/users` - Create user (Admin)
- `PUT /api/admin/users/:id` - Update user (Admin)
- `DELETE /api/admin/users/:id` - Delete user (Admin)
- `GET /api/admin/opportunities` - List all opportunities (Admin)
- `DELETE /api/admin/opportunities/:id` - Delete opportunity (Admin)
- `GET /api/admin/scholarships` - List all scholarships (Admin)
- `DELETE /api/admin/scholarships/:id` - Delete scholarship (Admin)
- `GET /api/admin/applications` - List all applications (Admin)

### Mentorship
- `GET /api/mentorship/requests` - Get mentorship requests
- `POST /api/mentorship/requests` - Request mentorship
- `PUT /api/mentorship/requests/:id` - Update session

### Applications
- `POST /api/applications` - Submit application
- `GET /api/applications` - Get applications
- `PUT /api/applications/:id/status` - Update application status

## 🎨 UI Components

The platform features a modern, responsive design with:
- **Dashboard**: Personalized based on user role
- **Opportunity Browser**: Advanced filtering and search
- **Mentorship Matching**: Smart mentor-student pairing
- **Profile Management**: Comprehensive user profiles
- **Communication Hub**: Direct messaging and notifications

## 🔒 Security Features

- JWT-based authentication
- **NEW:** Role-based access control (Student, Alumni, Admin)
- Password hashing with bcrypt
- Input validation and sanitization
- CORS protection
- SQL injection prevention (parameterized queries)
- **NEW:** Foreign key constraints for referential integrity
- **NEW:** CHECK constraints for data validation (e.g., CGPA 0.00-10.00)

## 📱 Responsive Design

Fully responsive design optimized for:
- Desktop computers
- Tablets
- Mobile devices
- Various screen sizes

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 🎯 Demo Accounts

Test the platform with these pre-configured accounts:

| Role    | Email              | Password    | Features Available                   |
|---------|-------------------|-------------|--------------------------------------|
| Admin   | admin@alumni.edu  | password123 | Full platform management             |
| Alumni  | alice@alumni.edu  | password123 | Create opportunities & scholarships  |
| Student | sarah@student.edu | password123 | Apply for jobs & scholarships        |

## 📚 Documentation

Comprehensive documentation is available:

- **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** - Complete API reference with examples
- **[DATABASE_SCHEMA.md](DATABASE_SCHEMA.md)** - ER diagram, table definitions, and query examples
- **[TESTING_GUIDE.md](TESTING_GUIDE.md)** - Testing procedures and verification steps
- **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - Overview of all enhancements

### Database Highlights:
- ✅ Third Normal Form (3NF) compliance verified
- ✅ Optimized indexes for query performance (< 100ms for complex queries)
- ✅ Advanced DBMS concepts: JOINs, UNIONs, aggregations, subqueries
- ✅ Referential integrity with foreign key constraints

### New Database Features:
- **Enhanced student profiles** with CGPA, category, and contact info
- **Sophisticated scholarship system** with automated eligibility matching
- **Scholarship applications table** with composite primary key
- **Unified search** using UNION across 5 entity types
- **Comprehensive indexes** on frequently queried columns

## 📄 License

This project is licensed under the MIT License.

## 📞 Support

For support and questions, please contact the development team or create an issue in the repository.