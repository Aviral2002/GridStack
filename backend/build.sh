#!/bin/bash

# Update package list
sudo apt-get update

# Install Tesseract and its dependencies
sudo apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    libleptonica-dev

# Install Python dependencies
pip install --no-cache-dir -r requirements.txt