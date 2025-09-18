#!/usr/bin/env python3
"""
Test script to verify YOLO detection setup
"""

import cv2
import numpy as np
from ultralytics import YOLO
from config import *

def test_yolo_setup():
    """Test YOLO model loading and basic detection"""
    print("YOLO Detection Test")
    print("=" * 30)
    
    try:
        # Test YOLO model loading
        print(f"Loading YOLO model: {YOLO_MODEL}")
        model = YOLO(YOLO_MODEL)
        print("✓ YOLO model loaded successfully!")
        
        # Test camera
        cap = cv2.VideoCapture(CAMERA_INDEX)
        if not cap.isOpened():
            print("✗ Camera not available")
            return False
        
        print("✓ Camera is working")
        
        # Test detection on a few frames
        print("\nTesting detection on camera feed...")
        print("Press 'q' to quit, 's' to save test image")
        
        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_count += 1
            
            # Run YOLO detection
            results = model(frame, 
                           conf=YOLO_CONFIDENCE_THRESHOLD,
                           iou=YOLO_IOU_THRESHOLD,
                           classes=YOLO_CLASSES,
                           verbose=False)
            
            # Count person detections
            person_count = 0
            if len(results) > 0:
                for result in results:
                    boxes = result.boxes
                    if boxes is not None:
                        for box in boxes:
                            class_id = int(box.cls[0].cpu().numpy())
                            if class_id == 0:  # Person class
                                person_count += 1
                                # Draw bounding box
                                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                                confidence = box.conf[0].cpu().numpy()
                                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                                cv2.putText(frame, f'Person: {confidence:.2f}', (int(x1), int(y1)-10), 
                                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            # Add status text
            cv2.putText(frame, f'People Detected: {person_count}', (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f'Frame: {frame_count}', (10, 70), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(frame, f'Confidence Threshold: {YOLO_CONFIDENCE_THRESHOLD}', (10, 110), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            cv2.imshow('YOLO Detection Test', frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):
                cv2.imwrite('yolo_test_frame.jpg', frame)
                print("Test frame saved as 'yolo_test_frame.jpg'")
        
        cap.release()
        cv2.destroyAllWindows()
        
        print(f"\n✓ YOLO test completed successfully!")
        print(f"Processed {frame_count} frames")
        print("YOLO is ready for use in the main application!")
        return True
        
    except Exception as e:
        print(f"✗ YOLO test failed: {e}")
        return False

def test_dependencies():
    """Test if all required packages are installed"""
    print("Testing YOLO dependencies...")
    required_packages = ['ultralytics', 'torch', 'torchvision']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package} is installed")
        except ImportError:
            print(f"✗ {package} is missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\nTo install missing packages, run:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    return True

def main():
    """Run all YOLO tests"""
    print("Nexora YOLO Detection Test")
    print("=" * 40)
    
    # Test dependencies
    if not test_dependencies():
        print("\n✗ Dependency test failed. Please install missing packages.")
        return
    
    print("\n" + "=" * 40)
    
    # Test YOLO setup
    if test_yolo_setup():
        print("\n✓ All YOLO tests passed!")
        print("You can now run the main application with YOLO detection.")
    else:
        print("\n✗ YOLO tests failed. Please check the error messages above.")

if __name__ == "__main__":
    main()
