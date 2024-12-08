import React, { useState, useEffect, useCallback } from 'react';
import './DataDisplay.css';

const DataDisplay = () => {
  const [data, setData] = useState({ packaged_products: [], fresh_produce: [] });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);


  // Fetch data function with useCallback to prevent unnecessary re-renders
  const fetchData = useCallback(async () => {
    try {
      const response = await fetch('http://localhost:5000/api/data/get-all-data');
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const result = await response.json();
      setData(result);
      setLoading(false);
    } catch (e) {
      console.error("Error fetching data:", e);
      setError(`Failed to fetch data: ${e.message}`);
      setLoading(false);
    }
  }, []);

  // Initial data fetch
  useEffect(() => {
    fetchData();
  }, [fetchData]);

  // Periodic refresh every 10 seconds
  useEffect(() => {
    const intervalId = setInterval(fetchData, 10000);
    return () => clearInterval(intervalId);
  }, [fetchData]);


  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="data-display">
      <h1>Stored Data</h1>
      <div className="data-section">
        <h3>Packaged Products</h3>
        <table>
          <thead>
            <tr>
              <th>Timestamp</th>
              <th>Brand</th>
              <th>Expiry Date</th>
              <th>Count</th>
              <th>Expired</th>
              <th>Expected Life Span</th>
            </tr>
          </thead>
          <tbody>
            {data.packaged_products.map((product, index) => (
              <tr key={index}>
                <td>{product.timestamp}</td>
                <td>{product.brand}</td>
                <td>{product.expiry_date}</td>
                <td>{product.count}</td>
                <td>{product.expired}</td>
                <td>{product.expected_life_span} days</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="data-section">
        <h3>Fresh Produce</h3>
        <table>
          <thead>
            <tr>
              <th>Timestamp</th>
              <th>Produce</th>
              <th>Classification</th>
            </tr>
          </thead>
          <tbody>
            {data.fresh_produce.map((produce, index) => (
              <tr key={index}>
                <td>{produce.timestamp}</td>
                <td>{produce.produce}</td>
                <td>{produce.result}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default DataDisplay;

