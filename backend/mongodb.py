from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING
from bson import ObjectId
from datetime import datetime
from typing import Optional, List
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB connection
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "hrms_db")

client = AsyncIOMotorClient(MONGODB_URL)
database = client[DATABASE_NAME]

# Collections
employees_collection = database["employees"]
attendance_collection = database["attendance"]

# Create indexes for better performance
async def create_indexes():
    """Create indexes for collections"""
    await employees_collection.create_index("employeeId", unique=True)
    await employees_collection.create_index("email", unique=True)
    await attendance_collection.create_index([("employeeId", ASCENDING), ("date", ASCENDING)], unique=True)

# Database models
class Employee:
    def __init__(self, employeeId: str, fullName: str, email: str, department: str, id: Optional[int] = None):
        self.id = id
        self.employeeId = employeeId
        self.fullName = fullName
        self.email = email
        self.department = department

    def to_dict(self):
        return {
            "employeeId": self.employeeId,
            "fullName": self.fullName,
            "email": self.email,
            "department": self.department
        }

    @classmethod
    def from_dict(cls, data: dict, employee_id: Optional[int] = None):
        return cls(
            id=employee_id or str(data.get("_id")),
            employeeId=data["employeeId"],
            fullName=data["fullName"],
            email=data["email"],
            department=data["department"]
        )

class Attendance:
    def __init__(self, employeeId: int, date: str, status: str, id: Optional[int] = None):
        self.id = id
        self.employeeId = employeeId
        self.date = date
        self.status = status

    def to_dict(self):
        return {
            "employeeId": self.employeeId,
            "date": self.date,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data: dict, attendance_id: Optional[int] = None):
        return cls(
            id=attendance_id or str(data.get("_id")),
            employeeId=data["employeeId"],
            date=data["date"],
            status=data["status"]
        )

# Database operations
class DatabaseOperations:
    @staticmethod
    async def create_employee(employee: Employee) -> Employee:
        """Create a new employee"""
        result = await employees_collection.insert_one(employee.to_dict())
        employee.id = str(result.inserted_id)
        return employee

    @staticmethod
    async def get_all_employees() -> List[Employee]:
        """Get all employees"""
        cursor = employees_collection.find({})
        employees = []
        async for document in cursor:
            employees.append(Employee.from_dict(document))
        return employees

    @staticmethod
    async def get_employee_by_id(employee_id: str) -> Optional[Employee]:
        """Get employee by ID"""
        try:
            obj_id = ObjectId(employee_id)
            document = await employees_collection.find_one({"_id": obj_id})
            if document:
                return Employee.from_dict(document)
        except:
            pass
        return None

    @staticmethod
    async def get_employee_by_employee_id(employee_id: str) -> Optional[Employee]:
        """Get employee by employeeId"""
        document = await employees_collection.find_one({"employeeId": employee_id})
        if document:
            return Employee.from_dict(document)
        return None

    @staticmethod
    async def delete_employee(employee_id: str) -> bool:
        """Delete employee and associated attendance records"""
        try:
            obj_id = ObjectId(employee_id)
            # Delete employee
            employee_result = await employees_collection.delete_one({"_id": obj_id})
            # Delete associated attendance records
            await attendance_collection.delete_many({"employeeId": employee_id})
            return employee_result.deleted_count > 0
        except:
            return False

    @staticmethod
    async def create_attendance(attendance: Attendance) -> Attendance:
        """Create attendance record"""
        result = await attendance_collection.insert_one(attendance.to_dict())
        attendance.id = str(result.inserted_id)
        return attendance

    @staticmethod
    async def get_attendance_by_employee(employee_id: str) -> List[Attendance]:
        """Get attendance records for an employee"""
        cursor = attendance_collection.find({"employeeId": employee_id})
        attendances = []
        async for document in cursor:
            attendances.append(Attendance.from_dict(document))
        return attendances

    @staticmethod
    async def get_all_attendance() -> List[dict]:
        """Get all attendance records with employee info"""
        pipeline = [
            {
                "$lookup": {
                    "from": "employees",
                    "localField": "employeeId",
                    "foreignField": "_id",
                    "as": "employee"
                }
            },
            {"$unwind": "$employee"},
            {
                "$project": {
                    "id": {"$toString": "$_id"},
                    "employeeId": "$employeeId",
                    "date": "$date",
                    "status": "$status",
                    "employee": {
                        "id": {"$toString": "$employee._id"},
                        "employeeId": "$employee.employeeId",
                        "fullName": "$employee.fullName",
                        "email": "$employee.email",
                        "department": "$employee.department"
                    }
                }
            }
        ]
        
        cursor = attendance_collection.aggregate(pipeline)
        results = []
        async for document in cursor:
            results.append(document)
        return results

    @staticmethod
    async def check_attendance_exists(employee_id: str, date: str) -> bool:
        """Check if attendance already exists for employee and date"""
        document = await attendance_collection.find_one({
            "employeeId": employee_id,
            "date": date
        })
        return document is not None

# Initialize database
async def init_db():
    """Initialize database and create indexes"""
    await create_indexes()
