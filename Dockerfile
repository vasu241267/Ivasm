FROM python:3.11-slim

# Avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install Chrome + Chromedriver + other deps
RUN apt-get update && apt-get install -y \
    wget unzip curl gnupg2 ca-certificates \
    chromium chromium-driver \
    xvfb \
    && apt-get clean

# Environment variables for Selenium
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/lib/chromium/chromedriver

# Create app directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port (for Flask)
EXPOSE 8080

# Run your app
CMD ["python", "main.py"]
