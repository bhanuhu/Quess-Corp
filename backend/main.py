from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from datetime import date
from typing import List
import schemas
import mongodb
from mongodb import DatabaseOperations, Employee, Attendance, init_db

app = FastAPI(title="HRMS Lite API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", 
        "http://127.0.0.1:5173",
        "https://eloquent-strudel-2748df.netlify.app"
    ],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    await init_db()

# Employee endpoints
@app.get("/employees", response_model=List[schemas.Employee])
async def get_employees():
    """Get all employees"""
    employees = await DatabaseOperations.get_all_employees()
    return [schemas.Employee(
        id=emp.id,
        employeeId=emp.employeeId,
        fullName=emp.fullName,
        email=emp.email,
        department=emp.department
    ) for emp in employees]

@app.get("/employees/{employee_id}", response_model=schemas.Employee)
async def get_employee(employee_id: str):
    """Get a specific employee by ID"""
    employee = await DatabaseOperations.get_employee_by_id(employee_id)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    return schemas.Employee(
        id=employee.id,
        employeeId=employee.employeeId,
        fullName=employee.fullName,
        email=employee.email,
        department=employee.department
    )

@app.post("/employees", response_model=schemas.Employee, status_code=status.HTTP_201_CREATED)
async def create_employee(employee: schemas.EmployeeCreate):
    """Create a new employee"""
    # Check if employee ID already exists
    existing_employee = await DatabaseOperations.get_employee_by_employee_id(employee.employeeId)
    if existing_employee:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee ID already exists"
        )
    
    # Check if email already exists
    employees = await DatabaseOperations.get_all_employees()
    for emp in employees:
        if emp.email == employee.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )
    
    new_employee = Employee(
        employeeId=employee.employeeId,
        fullName=employee.fullName,
        email=employee.email,
        department=employee.department
    )
    
    created_employee = await DatabaseOperations.create_employee(new_employee)
    return schemas.Employee(
        id=created_employee.id,
        employeeId=created_employee.employeeId,
        fullName=created_employee.fullName,
        email=created_employee.email,
        department=created_employee.department
    )

@app.delete("/employees/{employee_id}")
async def delete_employee(employee_id: str):
    """Delete an employee"""
    employee = await DatabaseOperations.get_employee_by_id(employee_id)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    
    success = await DatabaseOperations.delete_employee(employee_id)
    if success:
        return {"message": "Employee deleted successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete employee"
        )

# Attendance endpoints
@app.post("/attendance", response_model=schemas.Attendance, status_code=status.HTTP_201_CREATED)
async def mark_attendance(attendance: schemas.AttendanceCreate):
    """Mark attendance for an employee"""
    # Check if employee exists
    employee = await DatabaseOperations.get_employee_by_id(attendance.employeeId)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    
    # Check if attendance already marked for this date and employee
    exists = await DatabaseOperations.check_attendance_exists(attendance.employeeId, attendance.date.isoformat())
    if exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Attendance already marked for this date"
        )
    
    new_attendance = Attendance(
        employeeId=attendance.employeeId,
        date=attendance.date.isoformat(),
        status=attendance.status
    )
    
    created_attendance = await DatabaseOperations.create_attendance(new_attendance)
    return schemas.Attendance(
        id=created_attendance.id,
        employeeId=created_attendance.employeeId,
        date=date.fromisoformat(created_attendance.date),
        status=created_attendance.status
    )

@app.get("/attendance/employee/{employee_id}", response_model=List[schemas.Attendance])
async def get_employee_attendance(employee_id: str):
    """Get attendance records for a specific employee"""
    # Check if employee exists
    employee = await DatabaseOperations.get_employee_by_id(employee_id)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    
    attendance_records = await DatabaseOperations.get_attendance_by_employee(employee_id)
    return [schemas.Attendance(
        id=att.id,
        employeeId=att.employeeId,
        date=date.fromisoformat(att.date),
        status=att.status
    ) for att in attendance_records]

@app.get("/attendance", response_model=List[schemas.AttendanceResponse])
async def get_all_attendance():
    """Get all attendance records"""
    attendance_records = await DatabaseOperations.get_all_attendance()
    return [schemas.AttendanceResponse(**record) for record in attendance_records]

@app.get("/")
def read_root():
    return {"message": "HRMS Lite API", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
