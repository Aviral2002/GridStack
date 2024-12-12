#!/bin/bash

# Add APT sources for Tesseract
echo "deb http://deb.debian.org/debian buster main contrib non-free" >> /etc/apt/sources.list

# Update package list
apt-get update


# Install Tesseract and its dependencies
apt-get install -y tesseract-ocr tesseract-ocr-eng libleptonica-dev

# Verify Tesseract installation
if ! command -v tesseract &> /dev/null
then
    echo "Tesseract could not be found"
    exit 1
fi

# Install Python dependencies
pip install --no-cache-dir -r requirements.txt

