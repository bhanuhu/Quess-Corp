from pydantic import BaseModel, EmailStr, validator
from datetime import date
from typing import Optional

class EmployeeBase(BaseModel):
    employeeId: str
    fullName: str
    email: EmailStr
    department: str

class EmployeeCreate(EmployeeBase):
    pass

class Employee(EmployeeBase):
    id: str
    
    class Config:
        from_attributes = True

class AttendanceBase(BaseModel):
    date: date
    status: str  # "present" or "absent"
    
    @validator('status')
    def validate_status(cls, v):
        if v not in ['present', 'absent']:
            raise ValueError('Status must be either "present" or "absent"')
        return v

class AttendanceCreate(AttendanceBase):
    employeeId: str

class Attendance(BaseModel):
    id: str
    employeeId: str
    date: date
    status: str
    
    class Config:
        from_attributes = True

class AttendanceResponse(BaseModel):
    id: str
    date: date
    status: str
    employee: Employee
    
    class Config:
        from_attributes = True
