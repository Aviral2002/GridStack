import React from "react";
import FreshnessChecker from "./components/FreshnessChecker";
import OCRScanner from "./components/OCRScanner";
import BrandRecognition from "./components/BrandRecognition";

import './App.css';  // Importing the custom styles

const App = () => {
  return (
    <div className="app-container">
      <header className="header">
        <h1>AI Image Processing</h1>
        <p>Check freshness, recognize brands, or scan text using your camera or file upload.</p>
      </header>

      <main className="main-content">
        <section className="features-section">
          <div className="feature">
            <FreshnessChecker />
          </div>

          <div className="feature">
            <OCRScanner />
          </div>

          <div className="feature">
            <BrandRecognition />
          </div>
        </section>
      </main>

      <footer className="footer">
        <p>&copy; 2024 Flipkart Grid App</p>
      </footer>
    </div>
  );
};

export default App;
