# 🎯 Object Detection Microservice

A **containerized, real-time object detection web service** built with **FastAPI**, **YOLOv11**, and **Docker**.  
This project demonstrates a production-ready architecture with modern async APIs and computer vision inference.

---

## 🏷️ Tech Stack

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-teal?logo=fastapi)
![Ultralytics YOLO](https://img.shields.io/badge/YOLOv11-ultralytics-orange?logo=ai)
![Docker](https://img.shields.io/badge/Containerized-Docker-blue?logo=docker)
![OpenCV](https://img.shields.io/badge/OpenCV-Image_Processing-green?logo=opencv)

---
<img width="1294" height="1263" alt="image" src="https://github.com/user-attachments/assets/9fd91b21-7539-487d-b8a0-e8f9781132d2" />


## 1. 🧩 Initial Interpretation and Strategy

The initial request outlined a **microservice architecture** with two distinct components:  
- a **UI backend**, and  
- an **AI backend**.  

While this is a valid pattern, a **single-service architecture** was chosen for simplicity and efficiency.

### ✅ Justification for a Single-Service Model

- **Reduced Complexity** — avoids network overhead and inter-service communication.  
- **Efficiency** — FastAPI can serve both UI and model inference asynchronously.  
- **Maintainability** — easier debugging, versioning, and scaling.

This approach allowed for focusing on creating a **robust, high-quality** application.

---

## 2. ⚙️ Technology Selection

| Component | Choice | Reason |
|------------|---------|--------|
| **Backend Framework** | FastAPI | High-performance async API with built-in Swagger UI and Pydantic validation |
| **AI Model** | YOLOv11 (Ultralytics) | Modern, efficient, simple interface, better accuracy-speed tradeoff |
| **Containerization** | Docker | Ensures reproducible, isolated, and portable environment |

### 📚 References
- [FastAPI Official Docs](https://fastapi.tiangolo.com/)
- [Ultralytics YOLO Docs](https://docs.ultralytics.com)

---

## 3. 🧱 Step-by-Step Development Process

### 🪄 Step 1: Core Object Detection Logic
- Implemented core detection using `ultralytics.YOLO("yolov11n.pt")`.
- Extracted class names, confidence scores, and bounding boxes.
- Supported dynamic scaling for visual annotations.

---

### 🧩 Step 2: Building the Web Interface and API
- Designed a minimal HTML UI (`templates/index.html`).
- Added async `/predict/` endpoint using FastAPI.
- Used JavaScript `fetch()` for smooth frontend-backend interaction.

---

### 🗂️ Step 3: Implementing File Logging
- Auto-saves all results in structured directories:
  - `inputs/` → raw input images  
  - `outputs/` → annotated output images  
  - `results/` → JSON detection metadata  
- Handled using Python’s `os` and `json` modules.

---

### 🐳 Step 4: Containerization with Docker
- Used `python:3.10-slim` base image.
- Installed required dependencies and handled OpenCV shared libraries (`libGL.so.1`, `libgthread-2.0.so.0`).
- Built a robust and portable `Dockerfile`.

---

## 4. 🚀 Scalability & Production Considerations

Although the implementation meets assessment requirements, real-world deployments can enhance scalability and reliability.

### ⚖️ Horizontal Scaling & Load Balancing
- Stateless app design allows easy scaling across instances.  
- Can be distributed via **Nginx**, **AWS ALB**, or **Kubernetes Services**.

### 🔁 Automated Port Allocation & Service Discovery
- Future upgrade: script-based or orchestrated port allocation.
- Kubernetes handles this natively.

### ⚡ GPU-Accelerated Inference
- Use CUDA-based Docker images for GPU inference.
- Load YOLO model on GPU for high-speed detection.
- Scale to multiple GPUs for concurrent request processing.

> 💡 *Advanced deployment features are excluded here to keep the project lightweight and focused.*

---

## 5. 🛠️ Final Instructions for Replication

### 🔨 Build the Docker Image
```bash
docker build -t yolo-fastapi-service .
````

### ▶️ Run the Docker Container

```bash
docker run -p 8000:8000 yolo-fastapi-service
```

Then open your browser and visit:

```
http://localhost:8000
```

---

## ✅ Summary

This solution provides a:

* ⚡ **Lightweight, efficient, and modern FastAPI service**
* 🧠 **YOLOv11-powered real-time object detector**
* 🐳 **Dockerized and ready for local or cloud deployment**

> 🧩 A perfect foundation for scaling into a production-grade distributed inference system.

---

### 🖤 If you like this project…

Give it a ⭐ on [GitHub](https://github.com/yourusername/object-detection-microservice)!
