# Use an official Python runtime
FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    libpq-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*


# Set working directory in container
WORKDIR /app

# Copy only the requirement file first to take advantage of Docker caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project (excluding data/ via .dockerignore)
COPY . .

# Run your app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]