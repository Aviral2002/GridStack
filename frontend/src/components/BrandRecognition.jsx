import React, { useState, useRef, useEffect } from "react";
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

const BrandRecognition = () => {
  const [brand, setBrand] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
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

  const handleBrandRecognition = async () => {
    setLoading(true);
    setError(null);
    setBrand("");

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

      const response = await fetch("http://192.168.29.157:5000/api/brand/brand-recognition", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      console.log("Brand recognition response:", data);

      if (!response.ok) {
        throw new Error(data.error || `HTTP error! status: ${response.status}`);
      }

      if (data.error) {
        throw new Error(data.error);
      }

      setBrand(data.brand || "Unknown");
    } catch (error) {
      console.error("Error recognizing brand:", error);
      setError(`Failed to recognize brand: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card className="w-full max-w-md mx-auto">
      <CardHeader>
        <CardTitle>Brand Recognition</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
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
              onClick={handleBrandRecognition}
              disabled={loading}
              className="flex-1"
            >
              {loading ? "Recognizing..." : "Recognize Brand"}
            </Button>
          </div>
          {error && <p className="text-destructive">{error}</p>}
          {brand && (
            <div className="mt-4">
              <p className="font-semibold">Recognized Brand: <span className="text-primary">{brand}</span></p>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
};

export default BrandRecognition;

