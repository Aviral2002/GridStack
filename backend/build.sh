#!/bin/bash

# Update package list
apt-get update

# Install Tesseract and its dependencies
apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    libleptonica-dev

# Install Python dependencies
pip install --no-cache-dir -r requirements.txt