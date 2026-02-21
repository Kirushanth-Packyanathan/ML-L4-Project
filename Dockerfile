FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for XGBoost and Matplotlib
RUN apt-get update && apt-get install -y \
    libgomp1 \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Copy both requirement files
COPY requirements.txt .
COPY backend/requirements.txt ./backend_requirements.txt

# Install all dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r backend_requirements.txt

# Copy the entire project
COPY . .

# Environment variables
ENV PYTHONUNBUFFERED=1

# Note: The command is overridden in docker-compose.yml for each service
CMD ["python"]
