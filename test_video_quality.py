#!/usr/bin/env python3
"""
Test script to verify video quality improvements
"""

import cv2
import numpy as np
from config import *

def test_video_quality():
    """Test video quality and text visibility"""
    print("Video Quality Test")
    print("=" * 30)
    
    # Initialize camera
    cap = cv2.VideoCapture(CAMERA_INDEX)
    if not cap.isOpened():
        print("Error: Could not open camera")
        return
    
    # Set camera properties
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, VIDEO_FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, VIDEO_FRAME_HEIGHT)
    cap.set(cv2.CAP_PROP_FPS, 30)
    cap.set(cv2.CAP_PROP_BRIGHTNESS, 0.5)
    cap.set(cv2.CAP_PROP_CONTRAST, 0.5)
    
    print(f"Camera resolution: {VIDEO_FRAME_WIDTH}x{VIDEO_FRAME_HEIGHT}")
    print(f"JPEG quality: {VIDEO_JPEG_QUALITY}%")
    print("\nPress 'q' to quit, 's' to save test frame")
    
    frame_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_count += 1
        
        # Add test text with borders
        cv2.putText(frame, f'Frame: {frame_count}', (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 4)  # Black border
        cv2.putText(frame, f'Frame: {frame_count}', (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)  # Green text
        
        cv2.putText(frame, f'Quality: {VIDEO_JPEG_QUALITY}%', (10, 70), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 3)  # Black border
        cv2.putText(frame, f'Quality: {VIDEO_JPEG_QUALITY}%', (10, 70), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)  # Yellow text
        
        cv2.putText(frame, f'Resolution: {VIDEO_FRAME_WIDTH}x{VIDEO_FRAME_HEIGHT}', (10, 110), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 3)  # Black border
        cv2.putText(frame, f'Resolution: {VIDEO_FRAME_WIDTH}x{VIDEO_FRAME_HEIGHT}', (10, 110), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)  # White text
        
        # Add timestamp
        import time
        timestamp = time.strftime("%H:%M:%S")
        cv2.putText(frame, timestamp, (frame.shape[1] - 120, frame.shape[0] - 25), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 3)  # Black border
        cv2.putText(frame, timestamp, (frame.shape[1] - 120, frame.shape[0] - 25), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)  # White text
        
        cv2.imshow('Video Quality Test', frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            # Save test frame with high quality
            cv2.imwrite('test_frame.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 100])
            print("Test frame saved as 'test_frame.jpg'")
    
    cap.release()
    cv2.destroyAllWindows()
    
    print(f"\nTest completed. Processed {frame_count} frames.")
    print("Check the saved test_frame.jpg to verify text clarity.")

if __name__ == "__main__":
    test_video_quality()
