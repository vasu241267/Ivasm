FROM python:3.11-slim

# Avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install Chrome + dependencies
RUN apt-get update && apt-get install -y \
    wget unzip curl gnupg2 ca-certificates \
    chromium \
    xvfb \
    && apt-get clean \
    && which chromium || echo "Chromium not found" \
    && chromium --version

# Create app directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY main.py .

# Expose port for Flask
EXPOSE 8080

# Run the app
CMD ["python", "main.py"]
