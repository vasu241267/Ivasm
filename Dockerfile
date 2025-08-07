FROM python:3.11-slim

# Install Chromium and ChromeDriver
RUN apt-get update && apt-get install -y \
    chromium chromium-driver fonts-liberation curl unzip \
    && rm -rf /var/lib/apt/lists/*

ENV PATH="/usr/bin:$PATH"

# Set environment variables for Flask
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Add app files
COPY . /app
WORKDIR /app

# Start Flask app
CMD ["python", "main.py"]
