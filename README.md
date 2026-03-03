# HRMS Lite - Human Resource Management System

A lightweight, full-stack HR management application built with React and FastAPI.

## Project Overview

HRMS Lite is a simple yet professional HR management system that allows administrators to:
- Manage employee records (add, view, delete)
- Track daily attendance
- View attendance history per employee

## Tech Stack

### Frontend
- **React 19** - UI framework
- **React Router** - Client-side routing
- **Axios** - HTTP client for API calls
- **Vite** - Build tool and development server
- **CSS3** - Styling with modern design principles

### Backend
- **FastAPI** - Modern Python web framework
- **MongoDB** - NoSQL database for cloud deployment
- **Motor** - Async MongoDB driver
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

## Features

### Employee Management
- ✅ Add new employees with validation
- ✅ View all employees in a table format
- ✅ Delete employees (with cascade deletion of attendance records)
- ✅ Unique employee ID and email validation
- ✅ Professional form validation and error handling

### Attendance Management
- ✅ Mark attendance (Present/Absent) for employees
- ✅ View attendance records per employee
- ✅ Date-based attendance tracking
- ✅ Prevent duplicate attendance entries
- ✅ Clean attendance history display

### UI/UX Features
- ✅ Professional, modern interface
- ✅ Responsive design (mobile-friendly)
- ✅ Loading states
- ✅ Error states with meaningful messages
- ✅ Empty states
- ✅ Smooth navigation
- ✅ Form validation with user-friendly errors

## API Endpoints

### Employee Endpoints
- `GET /employees` - Get all employees
- `GET /employees/{id}` - Get specific employee
- `POST /employees` - Create new employee
- `DELETE /employees/{id}` - Delete employee

### Attendance Endpoints
- `POST /attendance` - Mark attendance
- `GET /attendance/employee/{employee_id}` - Get employee attendance
- `GET /attendance` - Get all attendance records

### System Endpoints
- `GET /` - API info
- `GET /health` - Health check

## Project Structure

```
Quess-Corp/
├── frontend/                 # React frontend
│   ├── src/
│   │   ├── components/      # Reusable components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API service layer
│   │   └── utils/          # Utility functions
│   ├── package.json
│   └── vite.config.js
├── backend/                  # FastAPI backend
│   ├── main.py             # Main application file
│   ├── database.py         # Database models and setup
│   ├── schemas.py          # Pydantic models
│   ├── requirements.txt    # Python dependencies
│   └── hrms.db            # SQLite database (auto-created)
└── README.md
```

## Installation & Setup

### Prerequisites
- Node.js (v16 or higher)
- Python (v3.8 or higher)
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Start the backend server:
```bash
python main.py
```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

## Usage

1. Start both the backend and frontend servers as described above
2. Open `http://localhost:5173` in your browser
3. Use the navigation menu to:
   - **Employees**: View and manage employee records
   - **Add Employee**: Create new employee entries
   - **Attendance**: Mark and view attendance records

## Database Schema

### Employees Collection
- `id` (MongoDB ObjectId)
- `employeeId` (Unique)
- `fullName`
- `email` (Unique)
- `department`

### Attendance Collection
- `id` (MongoDB ObjectId)
- `employeeId` (Reference to employee)
- `date`
- `status` ("present" or "absent")

## Validation & Error Handling

### Frontend Validation
- Email format validation
- Required field validation
- Duplicate prevention
- User-friendly error messages

### Backend Validation
- Pydantic model validation
- Database constraint checking
- HTTP status codes
- Detailed error responses

## Assumptions & Limitations

- Single admin user (no authentication system)
- No advanced HR features (payroll, leave management, etc.)
- MongoDB database (cloud-ready for deployment)
- No file upload capabilities
- Basic reporting only

## Deployment Notes

For production deployment:

### Backend
- Use MongoDB Atlas for cloud database
- Update MONGODB_URL environment variable
- Implement authentication/authorization
- Add CORS configuration for production domains
- Use production ASGI server

### Frontend
- Build for production: `npm run build`
- Deploy to static hosting (Vercel, Netlify)
- Update API base URL to production backend

## Future Enhancements

- User authentication and role-based access
- Advanced reporting and analytics
- Leave management system
- Payroll integration
- Employee profile management
- Bulk attendance marking
- Export functionality (PDF, Excel)
- Email notifications
- Mobile app

## Development

This project was developed as a full-stack coding assignment to demonstrate:
- End-to-end development skills
- Clean, modular code architecture
- Professional UI/UX design
- Proper error handling
- RESTful API design
- Database modeling
- Modern development practices

## License

This project is for educational/demonstration purposes.