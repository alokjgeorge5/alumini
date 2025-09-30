# Alumni Connect & Scholarship Support Platform

A comprehensive platform connecting alumni with current students for career guidance, job opportunities, scholarships, and mentorship. Built as a mini LinkedIn specifically for educational institutions.

## 🎯 Project Overview

This platform addresses the lack of centralized alumni-student interaction by providing:
- **Job & Internship Postings** by alumni
- **Scholarship Opportunities** with eligibility tracking
- **Mentorship Programs** for resume building, interview prep, and skill development
- **Alumni-hosted Webinars** and networking events
- **Success Stories** sharing and inspiration
- **Direct Alumni-Student Communication**

## 🛠 Tech Stack

- **Frontend**: React.js with modern hooks and responsive design
- **Backend**: Flask (Python) with RESTful APIs
- **Database**: MySQL with optimized schema design
- **Authentication**: JWT-based secure authentication
- **Styling**: Modern CSS with responsive design

## 🚀 Features

### For Students:
- Browse job opportunities and internships
- Search and apply for scholarships
- Find mentors based on skills and interests
- Join webinars and networking events
- Share success stories
- Track application status

### For Alumni:
- Post job openings and internships
- Share scholarship opportunities
- Offer mentorship services
- Host webinars and events
- Connect with students
- View engagement analytics

### For Mentors:
- Manage mentorship sessions
- Schedule meetings with students
- Track mentoring progress
- Share expertise and resources

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- MySQL 8.0+
- npm or yarn

## 🔧 Installation & Setup

### Quick Start (Single Command)

For new developers, you can get the entire application running with just one command:

```bash
git clone <repository-url>
cd alumni-connect-platform

# Create your environment file first
cp backend/.env.example backend/.env
# Edit backend/.env with your MySQL password

# Start everything with one command
npm start
```

This single command will:
- Install all dependencies (Node.js and Python)
- Set up and seed the MySQL database
- Start both frontend and backend servers

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

#### 3. Install Dependencies
```bash
npm run install-deps
```

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

## 📁 Project Structure

```
alumni-connect-platform/
├── client/                 # React frontend
│   ├── public/
│   ├── src/
│   │   ├── components/     # Reusable components
│   │   ├── pages/         # Page components
│   │   ├── context/       # React context for state management
│   │   ├── services/      # API service functions
│   │   ├── utils/         # Utility functions
│   │   └── styles/        # CSS styles
│   ├── package.json
│   └── .env
├── server/                # Flask backend
│   ├── app/
│   │   ├── models/        # Database models
│   │   ├── routes/        # API routes
│   │   ├── utils/         # Utility functions
│   │   └── __init__.py
│   ├── requirements.txt
│   ├── run.py
│   └── .env
├── database/              # Database schema and migrations
│   ├── schema.sql
│   └── seed_data.sql
├── README.md
└── package.json
```

## 🔗 API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout

### Users
- `GET /api/users/profile` - Get user profile
- `PUT /api/users/profile` - Update user profile
- `GET /api/users/alumni` - Get all alumni
- `GET /api/users/students` - Get all students

### Opportunities
- `GET /api/opportunities` - Get all opportunities
- `POST /api/opportunities` - Create new opportunity
- `PUT /api/opportunities/:id` - Update opportunity
- `DELETE /api/opportunities/:id` - Delete opportunity

### Scholarships
- `GET /api/scholarships` - Get all scholarships
- `POST /api/scholarships` - Create scholarship
- `GET /api/scholarships/eligible` - Get eligible scholarships

### Mentorship
- `GET /api/mentorship/sessions` - Get mentorship sessions
- `POST /api/mentorship/request` - Request mentorship
- `PUT /api/mentorship/sessions/:id` - Update session

### Applications
- `POST /api/applications` - Submit application
- `GET /api/applications/my` - Get user's applications
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
- Password hashing with bcrypt
- Input validation and sanitization
- CORS protection
- Rate limiting
- SQL injection prevention

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

## 📄 License

This project is licensed under the MIT License.

## 📞 Support

For support and questions, please contact the development team or create an issue in the repository.