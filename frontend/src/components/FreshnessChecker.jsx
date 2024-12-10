import React, { useState, useRef, useEffect } from "react";
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

const FreshnessChecker = () => {
  const [result, setResult] = useState("");
  const [freshness, setFreshness] = useState(null);
  const [expectedLifeSpan, setExpectedLifeSpan] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [produce, setProduce] = useState("");
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

  const handleCheckFreshness = async () => {
    setLoading(true);
    setError(null);
    setResult("");
    setFreshness(null);
    setExpectedLifeSpan(null);

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
      formData.append("produce", produce);

      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/freshness/freshness-check`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log("Freshness check response:", data);
      setResult(data.result);
      setFreshness(data.freshness);
      setExpectedLifeSpan(data.expected_life_span);
    } catch (error) {
      console.error("Error checking freshness:", error);
      setError(`Failed to check freshness: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card className="w-full max-w-md mx-auto">
      <CardHeader>
        <CardTitle>Freshness Checker</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <Input
            type="text"
            value={produce}
            onChange={(e) => setProduce(e.target.value)}
            placeholder="Enter produce name"
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
              onClick={handleCheckFreshness}
              disabled={loading || !produce}
              className="flex-1"
            >
              {loading ? "Checking..." : "Check Freshness"}
            </Button>
          </div>
          {error && <p className="text-destructive">{error}</p>}
          {result && (
            <div className="mt-4 space-y-2">
              <p><strong>Classification:</strong> {result}</p>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
};

export default FreshnessChecker;

