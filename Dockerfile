# Use an official Python 3.8 image based on Ubuntu 20.04 (Focal Fossa)
FROM python:3.10.18-slim-bullseye

# Set the working directory in the container
WORKDIR /app

# --- FIX: Install system dependencies required by OpenCV ---
# This command is made more robust to prevent network timeouts and reduce image size.
# --no-install-recommends prevents installing optional packages.
# rm -rf /var/lib/apt/lists/* cleans up the package cache to keep the image slim.
# RUN apt-get update && \
#     apt-get install -y --no-install-recommends libgl1-mesa-glx && \
#     rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install uvicorn -y && apt-get install -y --no-install-recommends libgl1-mesa-glx libglib2.0-0
# RUN apt install uvicorn

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Specify the port the app will run on
EXPOSE 8000

# Command to run the application using uvicorn
CMD ["uvicorn", "fast-api-service:app", "--host", "0.0.0.0", "--port", "8000"]