#!/usr/bin/env python3
"""
Calibration tool for improving person detection accuracy
"""

import cv2
import numpy as np
from config import *

def calibrate_detection():
    """Interactive calibration tool for detection parameters"""
    print("Person Detection Calibration Tool")
    print("=" * 40)
    
    # Initialize camera
    cap = cv2.VideoCapture(CAMERA_INDEX)
    if not cap.isOpened():
        print("Error: Could not open camera")
        return
    
    # Initialize cascades
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # Current parameters
    scale_factor = FACE_DETECTION_SCALE_FACTOR
    min_neighbors = FACE_DETECTION_MIN_NEIGHBORS
    min_size = FACE_DETECTION_MIN_SIZE[0]
    
    print("Controls:")
    print("Q - Quit")
    print("S - Save current settings")
    print("R - Reset to defaults")
    print("Arrow keys - Adjust parameters")
    print("Space - Toggle detection overlay")
    
    show_overlay = True
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Apply detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=scale_factor,
            minNeighbors=min_neighbors,
            minSize=(min_size, min_size),
            maxSize=FACE_DETECTION_MAX_SIZE,
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        
        # Draw overlay if enabled
        if show_overlay:
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, 'Face', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        
        # Add parameter display
        cv2.putText(frame, f'Scale Factor: {scale_factor:.2f}', (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, f'Min Neighbors: {min_neighbors}', (10, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, f'Min Size: {min_size}', (10, 90), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, f'Faces Detected: {len(faces)}', (10, 120), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f'Overlay: {"ON" if show_overlay else "OFF"}', (10, 150), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        
        cv2.imshow('Detection Calibration', frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            break
        elif key == ord('s'):
            print(f"Saving settings: scale={scale_factor:.2f}, neighbors={min_neighbors}, min_size={min_size}")
            save_settings(scale_factor, min_neighbors, min_size)
        elif key == ord('r'):
            scale_factor = 1.05
            min_neighbors = 5
            min_size = 30
            print("Reset to default settings")
        elif key == ord(' '):
            show_overlay = not show_overlay
        elif key == 83:  # Right arrow
            scale_factor += 0.01
        elif key == 81:  # Left arrow
            scale_factor = max(1.01, scale_factor - 0.01)
        elif key == 84:  # Up arrow
            min_neighbors += 1
        elif key == 82:  # Down arrow
            min_neighbors = max(1, min_neighbors - 1)
        elif key == ord('+'):
            min_size += 5
        elif key == ord('-'):
            min_size = max(10, min_size - 5)
    
    cap.release()
    cv2.destroyAllWindows()

def save_settings(scale_factor, min_neighbors, min_size):
    """Save calibrated settings to config file"""
    config_content = f"""# Configuration file for IoT Room Monitoring System

# ThingSpeak Configuration
# Replace these with your actual ThingSpeak channel details
THINGSPEAK_CHANNEL_ID = "YOUR_CHANNEL_ID"  # Your ThingSpeak channel ID
THINGSPEAK_API_KEY = "YOUR_API_KEY"        # Your ThingSpeak API key

# Camera Configuration
CAMERA_INDEX = 0  # Change this if you have multiple cameras (0, 1, 2, etc.)

# Detection Configuration (Calibrated)
FACE_DETECTION_SCALE_FACTOR = {scale_factor:.2f}  # Calibrated scale factor
FACE_DETECTION_MIN_NEIGHBORS = {min_neighbors}    # Calibrated min neighbors
FACE_DETECTION_MIN_SIZE = ({min_size}, {min_size})  # Calibrated min size
FACE_DETECTION_MAX_SIZE = (300, 300) # Maximum face size to detect

# Body detection (if available)
BODY_DETECTION_ENABLED = True
BODY_DETECTION_SCALE_FACTOR = 1.1
BODY_DETECTION_MIN_NEIGHBORS = 3
BODY_DETECTION_MIN_SIZE = (50, 100)

# Update Intervals (in seconds)
THINGSPEAK_UPDATE_INTERVAL = 5     # How often to fetch IoT data
PEOPLE_COUNT_UPDATE_INTERVAL = 1   # How often to update people count
CAMERA_DETECTION_DELAY = 0.1       # Delay between camera frame processing

# Flask Configuration
FLASK_HOST = '0.0.0.0'
FLASK_PORT = 2000
FLASK_DEBUG = True
"""
    
    with open('config.py', 'w') as f:
        f.write(config_content)
    
    print("Settings saved to config.py")

if __name__ == "__main__":
    calibrate_detection()
