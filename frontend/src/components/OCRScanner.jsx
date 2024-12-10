import React, { useState, useRef, useEffect } from "react";
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

const OCRScanner = () => {
  const [text, setText] = useState("");
  const [details, setDetails] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [brand, setBrand] = useState("");
  const [count, setCount] = useState(1);
  const [imageSource, setImageSource] = useState("file");
  const [cameraFacing, setCameraFacing] = useState("environment");
  const fileInputRef = useRef(null);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [stream, setStream] = useState(null);

  useEffect(() => {
    if (imageSource === "camera") {
      startCamera();
    } else {
      stopCamera();
    }
  }, [imageSource, cameraFacing]);

  const startCamera = async () => {
    try {
      const constraints = {
        video: { facingMode: cameraFacing }
      };
      const cameraStream = await navigator.mediaDevices.getUserMedia(constraints);
      setStream(cameraStream);
      if (videoRef.current) {
        videoRef.current.srcObject = cameraStream;
      }
    } catch (err) {
      console.error("Error accessing camera:", err);
      setError("Failed to access camera. Please ensure camera permissions are granted.");
    }
  };

  const stopCamera = () => {
    if (stream) {
      stream.getTracks().forEach(track => track.stop());
      setStream(null);
    }
  };

  const toggleCamera = () => {
    setImageSource(prev => prev === "camera" ? "file" : "camera");
  };

  const switchCamera = () => {
    setCameraFacing(prev => prev === "user" ? "environment" : "user");
  };

  const captureImage = () => {
    if (videoRef.current && canvasRef.current) {
      const video = videoRef.current;
      const canvas = canvasRef.current;
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      canvas.getContext("2d").drawImage(video, 0, 0);
      return new Promise((resolve) => {
        canvas.toBlob(resolve, "image/jpeg");
      });
    }
    return null;
  };

  const handleOCRScan = async () => {
    setLoading(true);
    setError(null);

    try {
      let imageBlob;
      if (imageSource === "camera") {
        imageBlob = await captureImage();
      } else {
        const file = fileInputRef.current.files[0];
        if (!file) {
          throw new Error("No file selected");
        }
        imageBlob = file;
      }

      if (!imageBlob) {
        throw new Error("Failed to get image");
      }

      const formData = new FormData();
      formData.append("image", imageBlob, "image.jpg");
      formData.append("brand", brand);
      formData.append("count", count);

      const response = await fetch("http://192.168.29.157:5000/api/expiry/ocr-scan", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log("OCR scan response:", data);
      setText(data.raw_text || "");
      setDetails({
        expiry_date: data.expiry_date,
      });
    } catch (error) {
      console.error("Error scanning text:", error);
      setError("Failed to scan text. Please try again.");
      setText("");
      setDetails(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card className="w-full max-w-md mx-auto">
      <CardHeader>
        <CardTitle>OCR Scanner</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <Input
            type="text"
            value={brand}
            onChange={(e) => setBrand(e.target.value)}
            placeholder="Enter brand name"
          />
          <Input
            type="number"
            value={count}
            onChange={(e) => setCount(parseInt(e.target.value))}
            placeholder="Enter count"
            min="1"
          />
          {imageSource === "file" ? (
            <Input
              type="file"
              ref={fileInputRef}
              accept="image/*"
              onChange={() => setError(null)}
            />
          ) : (
            <div className="aspect-video bg-muted">
              <video ref={videoRef} autoPlay playsInline muted className="w-full h-full object-cover" />
              <canvas ref={canvasRef} className="hidden" />
            </div>
          )}
          <div className="flex flex-col sm:flex-row gap-2">
            <Button onClick={toggleCamera} variant="secondary" className="flex-1">
              {imageSource === "camera" ? "Use File Upload" : "Use Camera"}
            </Button>
            {imageSource === "camera" && (
              <Button onClick={switchCamera} variant="secondary" className="flex-1">
                Switch Camera
              </Button>
            )}
            <Button
              onClick={handleOCRScan}
              disabled={loading || !brand}
              className="flex-1"
            >
              {loading ? "Scanning..." : "Scan for Text"}
            </Button>
          </div>
          {error && <p className="text-destructive">{error}</p>}
          {text && (
            <div className="mt-4 space-y-2">
              <h3 className="font-semibold">Raw Text:</h3>
              <p className="whitespace-pre-wrap">{text}</p>
            </div>
          )}
          {details && details.expiry_date && (
            <div className="mt-4 space-y-2">
              <h3 className="font-semibold">Extracted Details:</h3>
              <p><strong>EXPIRY DATE:</strong> {details.expiry_date}</p>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
};

export default OCRScanner;

