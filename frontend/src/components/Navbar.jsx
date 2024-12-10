import React from "react";
import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav className="bg-primary text-primary-foreground">
      <div className="container mx-auto px-4 py-4">
        <div className="flex flex-col sm:flex-row justify-between items-center">
          <Link to="/" className="text-2xl font-bold mb-4 sm:mb-0">
            GridStack
          </Link>
          <div className="flex space-x-4">
            <Link to="/freshness" className="hover:underline">Freshness</Link>
            <Link to="/ocr" className="hover:underline">OCR</Link>
            <Link to="/brand" className="hover:underline">Brand</Link>
            <Link to="/data" className="hover:underline">Data</Link>
          </div>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;

