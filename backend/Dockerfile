FROM python:3.9-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    libleptonica-dev && \
    rm -rf /var/lib/apt/lists/*

# Set up the application
WORKDIR /app
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Define the build command
CMD ["bash", "./build.sh"]
