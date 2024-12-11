#!/bin/bash

# Update package list
apt-get update

# Install Tesseract and its dependencies
apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    libleptonica-dev

# Verify Tesseract installation
if ! command -v tesseract &> /dev/null
then
    echo "Tesseract could not be found"
    exit 1
fi

# Install Python dependencies
pip install --no-cache-dir -r requirements.txt