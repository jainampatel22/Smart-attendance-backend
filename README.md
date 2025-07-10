# Smart Attendance System with Face Recognition

This project is a smart attendance system using FastAPI, React, and MongoDB. It allows users to register with their name, roll number, and photo, and then mark attendance using face recognition via a webcam.

---

## Features
- User registration with name, roll number, and photo upload
- Attendance marking via live webcam photo and face recognition
- MongoDB database for storing user info and attendance status
- REST API backend (FastAPI)
- Ready for React frontend integration

---

## Requirements

### Python Packages (Backend)
- fastapi
- uvicorn
- pymongo
- face_recognition
- opencv-python
- numpy
- python-multipart
- (Optional for local dev) mongosh or MongoDB Compass (GUI)

### Node Packages (Frontend)
- react
- react-dom
- react-webcam
- axios

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd <project-directory>
```

### 2. Install Python Dependencies
It is recommended to use a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn pymongo face_recognition opencv-python numpy python-multipart
```

### 3. Install and Start MongoDB
- **Local:**
  - Install via Homebrew:
    ```bash
    brew tap mongodb/brew
    brew install mongodb-community
    brew services start mongodb-community
    ```
  - Or use [MongoDB Atlas](https://www.mongodb.com/atlas) for cloud hosting.
- **Check connection:**
  - Default connection string for local: `mongodb://localhost:27017/`
  - For Atlas, use your provided connection string and set it as an environment variable (see below).

### 4. Configure MongoDB URL (for deployment)
- For production, set your MongoDB URL as an environment variable:
  ```bash
  export MONGODB_URL="<your-mongodb-connection-string>"
  ```
- In your code, use:
  ```python
  import os
  mongodb_url = os.environ.get("MONGODB_URL", "mongodb://localhost:27017/")
  client = MongoClient(mongodb_url)
  ```

### 5. Run the Backend
```bash
uvicorn main:app --reload
```
- The API will be available at `http://127.0.0.1:8000`
- Interactive docs: `http://127.0.0.1:8000/docs`

### 6. Frontend (React)
- Create a React app (if you don't have one):
  ```bash
  npx create-react-app frontend
  cd frontend
  npm install react-webcam axios
  ```
- Implement registration and attendance pages using the provided API endpoints.
- Make sure to set the backend URL to `http://127.0.0.1:8000` (or your deployed backend).

---

## Usage

- **Register:**
  - Send a POST request to `/register` with `name`, `roll_no`, and `photo` (file).
- **Mark Attendance:**
  - Send a POST request to `/attendance` with `photo` (file, e.g., from webcam).
- **CORS:**
  - CORS is enabled for all origins for development. Restrict this in production as needed.

---

## Notes
- Make sure MongoDB is running before starting the backend.
- For face recognition to work, the uploaded/captured photo must clearly show the user's face.
- For deployment, update the MongoDB connection string and CORS settings for security.

---

## License
MIT 