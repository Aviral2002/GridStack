import React from 'react';
import FreshnessChecker from './components/FreshnessChecker';
import OCRScanner from './components/OCRScanner';
import BrandRecognition from './components/BrandRecognition';
import DataDisplay from './components/DataDisplay';
import './App.css';

function App() {
  return (
    <div className="App">
      <h1>GridStack</h1>
      <div className="component-container">
        <FreshnessChecker />
        <OCRScanner />
        <BrandRecognition />
      </div>
      <DataDisplay />
    </div>
  );
}

export default App;

