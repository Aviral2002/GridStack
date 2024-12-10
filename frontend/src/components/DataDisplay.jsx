import React, { useState, useEffect, useCallback } from 'react';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Checkbox } from "@/components/ui/checkbox"
import { Button } from "@/components/ui/button"
import { ScrollArea } from "@/components/ui/scroll-area"

const DataDisplay = () => {
  const [data, setData] = useState({ packaged_products: [], fresh_produce: [] });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedRows, setSelectedRows] = useState({ packaged_products: [], fresh_produce: [] });

  const fetchData = useCallback(async () => {
    try {
      const response = await fetch('http://192.168.29.157:5000/api/data/get-all-data');
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

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  useEffect(() => {
    const intervalId = setInterval(fetchData, 10000);
    return () => clearInterval(intervalId);
  }, [fetchData]);

  const handleRowSelection = (type, id) => {
    setSelectedRows(prev => ({
      ...prev,
      [type]: prev[type].includes(id)
        ? prev[type].filter(rowId => rowId !== id)
        : [...prev[type], id]
    }));
  };

  const handleDeleteSelected = async (type) => {
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/data/delete-rows`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ type, ids: selectedRows[type] }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      fetchData();
      setSelectedRows(prev => ({ ...prev, [type]: [] }));
    } catch (error) {
      console.error("Error deleting rows:", error);
      setError(`Failed to delete rows: ${error.message}`);
    }
  };

  if (loading) return <div className="text-center p-4">Loading...</div>;
  if (error) return <div className="text-center p-4 text-red-500">Error: {error}</div>;

  return (
    <div className="p-4">
      <h2 className="text-2xl font-bold mb-4">Stored Data</h2>
      <div className="mb-8">
        <h3 className="text-xl font-semibold mb-2">Packaged Products</h3>
        <Button 
          onClick={() => handleDeleteSelected('packaged_products')}
          disabled={selectedRows.packaged_products.length === 0}
          className="mb-2"
        >
          Delete Selected
        </Button>
        <ScrollArea className="h-[400px]">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead className="w-[50px]">Select</TableHead>
                <TableHead>Timestamp</TableHead>
                <TableHead>Brand</TableHead>
                <TableHead>Expiry Date</TableHead>
                <TableHead>Count</TableHead>
                <TableHead>Expired</TableHead>
                <TableHead>Expected Life Span</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {data.packaged_products.map((product) => (
                <TableRow key={product.id}>
                  <TableCell>
                    <Checkbox
                      checked={selectedRows.packaged_products.includes(product.id)}
                      onCheckedChange={() => handleRowSelection('packaged_products', product.id)}
                    />
                  </TableCell>
                  <TableCell>{product.timestamp}</TableCell>
                  <TableCell>{product.brand}</TableCell>
                  <TableCell>{product.expiry_date}</TableCell>
                  <TableCell>{product.count}</TableCell>
                  <TableCell>{product.expired}</TableCell>
                  <TableCell>{product.expected_life_span} days</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </ScrollArea>
      </div>
      <div>
        <h3 className="text-xl font-semibold mb-2">Fresh Produce</h3>
        <Button 
          onClick={() => handleDeleteSelected('fresh_produce')}
          disabled={selectedRows.fresh_produce.length === 0}
          className="mb-2"
        >
          Delete Selected
        </Button>
        <ScrollArea className="h-[400px]">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead className="w-[50px]">Select</TableHead>
                <TableHead>Timestamp</TableHead>
                <TableHead>Produce</TableHead>
                <TableHead>Classification</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {data.fresh_produce.map((produce) => (
                <TableRow key={produce.id}>
                  <TableCell>
                    <Checkbox
                      checked={selectedRows.fresh_produce.includes(produce.id)}
                      onCheckedChange={() => handleRowSelection('fresh_produce', produce.id)}
                    />
                  </TableCell>
                  <TableCell>{produce.timestamp}</TableCell>
                  <TableCell>{produce.produce}</TableCell>
                  <TableCell>{produce.result}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </ScrollArea>
      </div>
    </div>
  );
};

export default DataDisplay;

