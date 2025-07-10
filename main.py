from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from pymongo import MongoClient
import face_recognition
import numpy as np
import shutil
import os
import pickle
import bson

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = MongoClient("mongodb://localhost:27017/")
db = client["attendance_db"]
students = db["students"]

def save_upload_file(upload_file: UploadFile, destination: str) -> str:
    with open(destination, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    return destination

@app.post("/register")
async def register(
    name: str = Form(...),
    roll_no: str = Form(...),
    photo: UploadFile = File(...)
):
    photo_path = f"photos/{roll_no}_{photo.filename}"
    os.makedirs("photos", exist_ok=True)
    save_upload_file(photo, photo_path)

    image = face_recognition.load_image_file(photo_path)
    encodings = face_recognition.face_encodings(image)
    if not encodings:
        os.remove(photo_path)
        raise HTTPException(status_code=400, detail="No face found in the uploaded photo.")
    face_encoding = encodings[0].tolist() 


    if students.find_one({"roll_no": roll_no}):
        os.remove(photo_path)
        raise HTTPException(status_code=400, detail="Roll number already exists.")

    students.insert_one({
        "name": name,
        "roll_no": roll_no,
        "photo_path": photo_path,
        "face_encoding": face_encoding,
        "attendance": "absent"
    })
    return JSONResponse(content={"message": "Registered successfully."})

@app.post("/attendance")
async def attendance(photo: UploadFile = File(...)):
    photo_path = f"temp/{photo.filename}"
    os.makedirs("temp", exist_ok=True)
    save_upload_file(photo, photo_path)

    image = face_recognition.load_image_file(photo_path)
    encodings = face_recognition.face_encodings(image)
    if not encodings:
        os.remove(photo_path)
        raise HTTPException(status_code=400, detail="No face found in the uploaded photo.")
    face_encoding = encodings[0]

    
    for student in students.find():
        known_encoding = np.array(student["face_encoding"])
        distance = np.linalg.norm(known_encoding - face_encoding)
        if distance < 0.5:
            students.update_one({"_id": student["_id"]}, {"$set": {"attendance": "present"}})
            os.remove(photo_path)
            return JSONResponse(content={"message": f"Attendance marked for {student['name']} ({student['roll_no']})"})
    os.remove(photo_path)
    return JSONResponse(content={"message": "Face not recognized. Attendance not marked."})
