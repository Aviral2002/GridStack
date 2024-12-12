import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from './components/Navbar';
import FreshnessChecker from './components/FreshnessChecker';
import OCRScanner from './components/OCRScanner';
import BrandRecognition from './components/BrandRecognition';
import DataDisplay from './components/DataDisplay';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gradient-to-b from-white to-gray-100 font-sans flex flex-col">
        <Navbar />
        <main className="container mx-auto px-4 py-8 flex-grow">
          <Routes>
            <Route
              path="/"
              element={
                <div>
                  <div className="video-container mb-8">
                    <video
                      className="w-full h-auto rounded-lg shadow-lg"
                      controls
                    >
                      <source src="public/beg.mp4" type="video/mp4" />
                      Your browser does not support the video tag.
                    </video>
                  </div>
                  <div className="mt-15 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                    <FreshnessChecker />
                    <OCRScanner />
                    <BrandRecognition />
                  </div>
                </div>
              }
            />
            <Route path="/freshness" element={<FreshnessChecker />} />
            <Route path="/ocr" element={<OCRScanner />} />
            <Route path="/brand" element={<BrandRecognition />} />
            <Route path="/data" element={<DataDisplay />} />
          </Routes>
        </main>
        <footer className="bg-gray-800 text-white text-center py-4">
          Developed by{' '}
          <a
            href="https://github.com/Aviral2002"
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-400 hover:underline"
          >
            Aviral2002
          </a>
        </footer>
      </div>
    </Router>
  );
}

export default App;
