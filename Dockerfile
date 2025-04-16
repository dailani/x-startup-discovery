# Use an official Python runtime
FROM python:3.11-slim

# Set working directory in container
WORKDIR /app

# Copy only the requirement file first to take advantage of Docker caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project (excluding data/ via .dockerignore)
COPY . .

# Run your app
CMD ["python", "main.py"]
