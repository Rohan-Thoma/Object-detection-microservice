import cv2
import random
import numpy as np
from ultralytics import YOLO
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import io
import os
import time
import json

# --- 1. Initialization ---
app = FastAPI()

# --- Create directories for data persistence ---
SAVE_DIR_BASE = "saved_data"
INPUT_DIR = os.path.join(SAVE_DIR_BASE, "inputs")
OUTPUT_DIR = os.path.join(SAVE_DIR_BASE, "outputs")
JSON_DIR = os.path.join(SAVE_DIR_BASE, "json")

os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(JSON_DIR, exist_ok=True)

# Mount directories for static files (for frontend display) and templates
os.makedirs("static/outputs", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Load the YOLOv8 Model
model = YOLO('yolo11n.pt')

# Define the same vibrant color palette
COLOR_PALETTE = [
    ((102, 229, 255), (48, 48, 48)), ((255, 204, 102), (48, 48, 48)),
    ((178, 255, 102), (48, 48, 48)), ((80, 127, 255), (48, 48, 48)),
    ((221, 160, 221), (48, 48, 48)), ((208, 224, 64), (48, 48, 48)),
]

# --- 2. Reusable Object Detection Logic ---
def detect_and_draw(input_image: np.ndarray):
    """
    This function is adapted from your Gradio app. It performs detection,
    draws dynamically scaled annotations, and returns the annotated image
    and the structured JSON data.
    """
    img_height, img_width, _ = input_image.shape
    results = model(input_image)
    output_data = []
    annotated_image = input_image.copy()

    # Dynamic Scaling for Annotations
    font_scale = min(3.0, max(0.5, img_width / 1200))
    thickness = max(1, int(img_width / 600))
    bbox_thickness = max(2, int(img_width / 300))
    padding = max(3, int(img_width / 200))
    line_spacing = max(3, int(img_width / 250))

    for i, box in enumerate(results[0].boxes):
        class_id = int(box.cls)
        class_name = model.names[class_id]
        confidence = float(box.conf)
        bbox_abs = box.xyxy[0].cpu().numpy()
        x1, y1, x2, y2 = bbox_abs.astype(int)
        
        bg_color, text_color = random.choice(COLOR_PALETTE)
        cv2.rectangle(annotated_image, (x1, y1), (x2, y2), bg_color, bbox_thickness)
        
        lines = [f"ID: {i}", f"{class_name}", f"Score: {confidence:.2f}"]
        line_heights = []
        max_line_width = 0
        for line in lines:
            (w, h), _ = cv2.getTextSize(line, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)
            line_heights.append(h)
            max_line_width = max(max_line_width, w)
        
        total_text_height = sum(line_heights) + line_spacing * (len(lines) - 1)
        
        label_y_start = max(y1 - total_text_height - (padding * 2) - (thickness * 4), 0)
        label_x_start = x1
        bg_top_left = (label_x_start, label_y_start)
        bg_bottom_right = (label_x_start + max_line_width + (padding * 2), label_y_start + total_text_height + (padding * 2))
        
        cv2.rectangle(annotated_image, bg_top_left, bg_bottom_right, bg_color, -1)
        
        current_y = label_y_start + padding
        for line, h in zip(lines, line_heights):
            text_y = current_y + h
            cv2.putText(annotated_image, line, (label_x_start + padding, text_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_color, thickness)
            current_y = text_y + line_spacing

        relative_bbox = [
            round(x1 / img_width, 4), round(y1 / img_height, 4),
            round(x2 / img_width, 4), round(y2 / img_height, 4)
        ]
        output_data.append({
            "object_id": i, "class_name": class_name,
            "confidence_score": f"{confidence:.2f}",
            "relative_bbox_coordinates": relative_bbox
        })
    
    return annotated_image, output_data

# --- 3. FastAPI Endpoints ---
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serves the main HTML page."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/detect")
async def process_detection(file: UploadFile = File(...)):
    """
    Processes the uploaded image, saves all artifacts, and returns detection results.
    """
    # Read image from upload
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Perform detection
    annotated_image, json_data = detect_and_draw(img)

    # --- Save artifacts with chronological naming ---
    # 1. Determine the next chronological ID
    next_id = len(os.listdir(INPUT_DIR)) + 1
    
    # 2. Define base filename
    file_extension = os.path.splitext(file.filename)[1]
    if not file_extension: file_extension = ".jpg" # Default extension
    base_filename = f"image{next_id}"

    # 3. Save the input image
    input_path = os.path.join(INPUT_DIR, f"{base_filename}{file_extension}")
    with open(input_path, "wb") as f:
        f.write(contents)

    # 4. Save the annotated output image
    output_path = os.path.join(OUTPUT_DIR, f"{base_filename}_output.jpg")
    cv2.imwrite(output_path, annotated_image)

    # 5. Save the JSON data
    json_path = os.path.join(JSON_DIR, f"{base_filename}_data.json")
    with open(json_path, "w") as f:
        json.dump(json_data, f, indent=4)
    
    # --- Save a temporary output image for frontend display ---
    timestamp = int(time.time())
    display_filename = f"output_{timestamp}.jpg"
    display_path = os.path.join("static/outputs", display_filename)
    cv2.imwrite(display_path, annotated_image)
    
    # URL for the saved image to be displayed on the webpage
    image_url = f"/static/outputs/{display_filename}"

    return JSONResponse(content={
        "json_output": json_data,
        "image_url": image_url
    })

