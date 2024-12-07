import React, { useState, useRef, useEffect } from "react";
import "./FreshnessChecker.css";

const FreshnessChecker = () => {
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [stream, setStream] = useState(null);
  const [imageSource, setImageSource] = useState("camera");
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const fileInputRef = useRef(null);

  useEffect(() => {
    const setupCamera = async () => {
      try {
        const cameraStream = await navigator.mediaDevices.getUserMedia({ video: true });
        setStream(cameraStream);
        if (videoRef.current) {
          videoRef.current.srcObject = cameraStream;
        }
      } catch (err) {
        console.error("Error accessing camera:", err);
        setError("Failed to access camera. Please ensure camera permissions are granted.");
      }
    };

    if (imageSource === "camera") {
      setupCamera();
    }

    return () => {
      if (stream) {
        stream.getTracks().forEach(track => track.stop());
      }
    };
  }, [imageSource]);

  const captureImage = () => {
    return new Promise((resolve, reject) => {
      if (videoRef.current && canvasRef.current) {
        const video = videoRef.current;
        const canvas = canvasRef.current;
        const context = canvas.getContext("2d");

        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        context.drawImage(video, 0, 0, canvas.width, canvas.height);

        canvas.toBlob(resolve, "image/jpeg");
      } else {
        reject(new Error("Video or canvas element not available"));
      }
    });
  };

  const handleCheckFreshness = async () => {
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

      const response = await fetch("http://localhost:5000/api/freshness/freshness-check", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log("Freshness check response:", data);
      setResult(data.result || "Unknown");
    } catch (error) {
      console.error("Error checking freshness:", error);
      setError(`Failed to check freshness: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleImageSourceChange = (source) => {
    setImageSource(source);
    setError(null);
    setResult("");
  };

  return (
    <div className="freshness-checker">
      <h2>Freshness Checker</h2>
      <div className="image-source-selector">
        <button
          onClick={() => handleImageSourceChange("camera")}
          className={imageSource === "camera" ? "active" : ""}
        >
          Use Camera
        </button>
        <button
          onClick={() => handleImageSourceChange("file")}
          className={imageSource === "file" ? "active" : ""}
        >
          Upload Image
        </button>
      </div>
      {imageSource === "camera" ? (
        <div className="video-container">
          <video
            ref={videoRef}
            autoPlay
            playsInline
            muted
          />
          <canvas ref={canvasRef} style={{ display: "none" }} />
        </div>
      ) : (
        <div className="file-input-container">
          <input
            type="file"
            ref={fileInputRef}
            accept="image/*"
            onChange={() => setError(null)}
          />
        </div>
      )}
      {error && <p className="error">{error}</p>}
      {result && <p className="result">Result: {result}</p>}
      <button
        onClick={handleCheckFreshness}
        disabled={loading || (imageSource === "camera" && !stream)}
      >
        {loading ? "Checking..." : "Check Freshness"}
      </button>
    </div>
  );
};

export default FreshnessChecker;

