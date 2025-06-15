#**⚠️🚫 Backend Offline Notice:**  
**Unfortunately, the backend hosting has been terminated due to the end of my Google App Engine free plan.**  
**But don’t worry! The frontend is still live here:** [https://gridstack-1.onrender.com](https://gridstack-1.onrender.com) 🌐  
🎥 **You can also watch a short demo video on the website showing how the project worked during its prototyping stage!**



# GridStack

GridStack is a full-stack application designed to streamline inventory management by automating product information extraction and analysis. It leverages image recognition and OCR technology to determine product freshness, extract expiry dates, and identify brands.  This information is then stored in a database for easy access and analysis.

## Features

* **Freshness Checker:** Analyzes images of fresh produce to classify them as "fresh" or "rotten," aiding in quality control and minimizing waste.  Uses a pre-trained TensorFlow model.
* **OCR Scanner:** Extracts textual information, including expiry dates, from product images using Tesseract OCR. This helps track product shelf life and manage inventory effectively.
* **Brand Recognition:**  Identifies the brand of a product from its image using a Roboflow-trained model, simplifying data entry and brand-specific analysis.
* **Data Display:** Provides a user-friendly interface to view and manage the data collected by the Freshness Checker and OCR Scanner, including features to delete selected records.
* **Camera Integration:** Allows users to capture images directly from their webcam for both Freshness Checking, OCR Scanning, and Brand Recognition, in addition to uploading images.

## Technologies Used

* **Frontend:** React, Vite, Tailwind CSS, Radix UI, Lucide React Icons
* **Backend:** Flask, Python, gunicorn
* **Database:** SQLite
* **Machine Learning & Image Processing:** TensorFlow, Tesseract OCR, Roboflow, OpenCV, Pillow
* **Deployment:** Render (example provided)

## Getting Started

### Prerequisites

* **Node.js (v14 or later):** For running the frontend development server.
* **npm or yarn:** For managing frontend dependencies.
* **Python (v3.7 or later):** For running the backend Flask server.
* **pip:** For installing Python dependencies.

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/gridstack.git
   ```

2. **Backend Setup:**

   ```bash
   cd gridstack/backend
   python3 -m venv .venv  # Create a virtual environment (recommended)
   source .venv/bin/activate  # Activate the virtual environment
   pip install -r requirements.txt  # Install backend dependencies
   ```
3. **Frontend Setup:**

   ```bash
   cd gridstack/frontend
   npm install  # Or yarn install
   ```

4. **Environment Variables (Backend):**

   Create a `.env` file in the `backend` directory and add the following:

   ```
   ALLOWED_ORIGINS=http://localhost:3000,http://your-frontend-url  # Replace with your frontend URL for production
   VITE_ROBOFLOW_MODEL_ENDPOINT=your_roboflow_model_endpoint # Replace with your Roboflow model endpoint
   VITE_ROBOFLOW_API_KEY=your_roboflow_api_key # Replace with your Roboflow API key
   ```
5. **Environment Variables (Frontend):**
Create a `.env` file in the `frontend` directory and add the following, ensuring to use the same URLs as the `ALLOWED_ORIGINS` in the backend setup.

```
VITE_API_URL=http://127.0.0.1:5000 # Replace with your backend URL for development, and production URL for production
VITE_ROBOFLOW_API_KEY=your_roboflow_api_key # Replace with your Roboflow API key
VITE_ROBOFLOW_MODEL_ENDPOINT=your_roboflow_model_endpoint # Replace with your Roboflow model endpoint
```

### Running the Application

1. **Start the backend server:**

   ```bash
   cd gridstack/backend
   flask run  # For development
   # For production, use gunicorn (as specified in render.yaml):
   gunicorn wsgi:app
   ```

2. **Start the frontend development server:**

   ```bash
   cd gridstack/frontend
   npm run dev  # Or yarn dev
   ```

## Usage Examples

**Freshness Checker:**

1. Navigate to the Freshness Checker section in the web interface.
2. Either upload an image of the produce or use your camera to take a picture.
3. Enter the name of the produce (e.g., "Apple," "Banana").
4. Click "Check Freshness."  The result ("fresh" or "rotten") will be displayed.

**OCR Scanner:**

1. Navigate to the OCR Scanner section.
2. Upload an image of a product label or use your camera to take a picture.
3. Enter the brand name and the number of items.
4. Click "Scan for Text."  The extracted text and identified expiry date will be displayed.

**Brand Recognition:**

1. Navigate to the Brand Recognition section.
2. Upload an image of a product or use your camera to take a picture.
3. Click "Recognize Brand." The identified brand will be displayed.

**Data Display:**

1. Navigate to the Data tab.  This page displays stored packaged product and fresh produce data in tables.
2. Select rows using the checkboxes and click "Delete Selected" to remove specific records.


## Deployment

This repository includes a `render.yaml` file for easy deployment on Render. Adjust the `startCommand` and environment variables in `render.yaml` as needed to match your application's setup.  Ensure to follow Render's instructions to deploy your application.

## Further Development

* **Improve Model Accuracy:**  Retrain the freshness detection and brand recognition models with a larger, more diverse dataset to enhance accuracy.
* **Enhanced OCR:**  Explore more advanced OCR techniques to improve accuracy and handle different fonts and layouts.
* **User Authentication:** Implement user authentication to restrict access to data and features.
* **Data Visualization:**  Add data visualization capabilities to provide insights into product freshness, expiry trends, and brand distribution.
* **API Integration:** Integrate with external APIs for product information retrieval and pricing data.

This enhanced README provides more detailed instructions, usage examples, and development suggestions for the GridStack project. Remember to replace placeholder values with your actual API keys and endpoints.
```
