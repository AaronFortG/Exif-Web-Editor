# Step 1: Start from an official Python base image
# Using 'slim' for a smaller image size
FROM python:3.11-slim

# Step 1: Install system dependencies (exiftool)
RUN apt-get update && \
    apt-get install -y exiftool && \
    rm -rf /var/lib/apt/lists/*

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Install dependencies
# Copy only the requirements.txt first to leverage Docker's layer caching.
# This way, dependencies are only re-installed if requirements.txt changes.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Step 4: Copy the application code into the container
# Copy the main app file and the templates directory
COPY app.py .
COPY templates/ ./templates/

# Step 5: Create the 'uploads' directory
# The app.py will likely try to write here.
# This directory should be mounted as a volume at runtime for persistence.
RUN mkdir uploads

# Step 6: Expose the port
# We assume the app will run on port 8000 (a common port for gunicorn).
# If your app.py or DEPLOYMENT.md specifies a different port, change this.
EXPOSE 8000

# Step 7: Define the command to run the application
# This assumes 'gunicorn' is listed in your requirements.txt,
# which is standard for deploying a Flask app.
# It runs the 'app' instance from the 'app.py' file.
# -w 4: Starts 4 worker processes (adjust as needed)
# -b 0.0.0.0:8000: Binds to all network interfaces on port 8000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]