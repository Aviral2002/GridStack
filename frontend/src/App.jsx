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
      <div className="min-h-screen bg-background font-sans">
        <Navbar />
        <main className="container mx-auto px-4 py-8">
          <h1 className="text-4xl font-bold text-primary mb-8 text-center">GridStack</h1>
          <Routes>
            <Route path="/" element={
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                <FreshnessChecker />
                <OCRScanner />
                <BrandRecognition />
              </div>
            } />
            <Route path="/freshness" element={<FreshnessChecker />} />
            <Route path="/ocr" element={<OCRScanner />} />
            <Route path="/brand" element={<BrandRecognition />} />
            <Route path="/data" element={<DataDisplay />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;

