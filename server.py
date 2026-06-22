from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from datetime import datetime
from optimize import RouteOptimizer

load_dotenv()
# Store driver locations temporarily
driver_locations = {}
app = FastAPI()

# Allow Flutter apps to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dummy student data
students = [
    {"id": 1, "name": "Raj", "stop": "Main Road", "lat": 13.0827, "lng": 80.2707},
    {"id": 2, "name": "Priya", "stop": "Main Road", "lat": 13.0828, "lng": 80.2708},
    {"id": 3, "name": "John", "stop": "Park Lane", "lat": 13.0830, "lng": 80.2710},
]

# API endpoint - return all students
@app.get('/api/students')
def get_students():
    return {"status": "success", "students": students}

# API endpoint - return single student
@app.get('/api/students/{student_id}')
def get_student(student_id: int):
    for student in students:
        if student["id"] == student_id:
            return {"status": "success", "student": student}
    return {"status": "error", "message": "Student not found"}

# Test endpoint
@app.get('/api/test')
def test():
    return {"message": "Backend is working!", "status": "success"}

# Driver login endpoint
@app.post('/api/driver-login')
def driver_login(data: dict):
    username = data.get('username')
    password = data.get('password')
    
    # Test with dummy credentials
    if username == 'driver123' and password == 'password123':
        return {
            "status": "success",
            "message": "Driver login successful!",
            "driver_id": 1,
            "name": "John Driver"
        }
    else:
        return {
            "status": "error",
            "message": "Invalid username or password"
        }
# Parent login endpoint
@app.post('/api/parent-login')
def parent_login(data: dict):
    phone = data.get('phone')
    password = data.get('password')
    
    # Test with dummy credentials
    if phone == '9876543210' and password == 'password123':
        return {
            "status": "success",
            "message": "Parent login successful!",
            "parent_id": 1,
            "child_name": "Raj"
        }
    else:
        return {
            "status": "error",
            "message": "Invalid phone or password"
        }
# Admin login endpoint
@app.post('/api/admin-login')
def admin_login(data: dict):
    email = data.get('email')
    password = data.get('password')
    
    # Test with dummy credentials
    if email == 'admin@school.com' and password == 'password123':
        return {
            "status": "success",
            "message": "Admin login successful!",
            "admin_id": 1,
            "school_name": "Central School"
        }
    else:
        return {
            "status": "error",
            "message": "Invalid email or password"
        }
# Driver location endpoint - receive location from driver
@app.post('/api/driver-location')
def update_driver_location(data: dict):
    driver_id = data.get('driver_id')
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    
    # Store location
    driver_locations[driver_id] = {
        'latitude': latitude,
        'longitude': longitude,
        'timestamp': str(datetime.now())
    }
    
    return {
        "status": "success",
        "message": "Location updated"
    }

# Get driver location endpoint - send location to parent
@app.get('/api/driver-location/{driver_id}')
def get_driver_location(driver_id: str):
    location = driver_locations.get(driver_id)
    
    if location:
        return {
            "status": "success",
            "latitude": location['latitude'],
            "longitude": location['longitude'],
            "timestamp": location['timestamp']
        }
    else:
        return {
            "status": "error",
            "message": "Location not found"
        }
# Route optimization endpoint
@app.post('/api/optimize-route')
def optimize_route(data: dict):
    students = data.get('students', [])
    
    # Call optimization algorithm
    optimized_students = RouteOptimizer.optimize_route(students)
    
    # Calculate distance saved
    original_distance = RouteOptimizer.calculate_total_distance(students)
    optimized_distance = RouteOptimizer.calculate_total_distance(optimized_students)
    distance_saved = original_distance - optimized_distance
    
    return {
        "status": "success",
        "optimized_students": optimized_students,
        "original_distance": original_distance,
        "optimized_distance": optimized_distance,
        "distance_saved": distance_saved,
        "fuel_saved_liters": round(distance_saved * 0.05, 2)  # Assume 5L per 100km
    }
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=5000)