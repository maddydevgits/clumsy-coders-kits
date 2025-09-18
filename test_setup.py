#!/usr/bin/env python3
"""
Test script to verify the IoT Room Monitoring System setup
"""

import cv2
import requests
import sys
from config import *

def test_camera():
    """Test if camera is accessible"""
    print("Testing camera...")
    try:
        cap = cv2.VideoCapture(CAMERA_INDEX)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                print("✓ Camera is working correctly")
                cap.release()
                return True
            else:
                print("✗ Camera opened but cannot read frames")
                cap.release()
                return False
        else:
            print("✗ Cannot open camera")
            return False
    except Exception as e:
        print(f"✗ Camera error: {e}")
        return False

def test_haar_cascade():
    """Test if Haar cascade classifier is available"""
    print("Testing Haar cascade classifier...")
    try:
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        cascade = cv2.CascadeClassifier(cascade_path)
        if not cascade.empty():
            print("✓ Haar cascade classifier loaded successfully")
            return True
        else:
            print("✗ Haar cascade classifier failed to load")
            return False
    except Exception as e:
        print(f"✗ Haar cascade error: {e}")
        return False

def test_thingspeak_config():
    """Test ThingSpeak configuration"""
    print("Testing ThingSpeak configuration...")
    if THINGSPEAK_CHANNEL_ID == "YOUR_CHANNEL_ID":
        print("✗ ThingSpeak Channel ID not configured")
        return False
    if THINGSPEAK_API_KEY == "YOUR_API_KEY":
        print("✗ ThingSpeak API Key not configured")
        return False
    
    print("✓ ThingSpeak configuration appears to be set")
    return True

def test_thingspeak_connection():
    """Test ThingSpeak API connection"""
    print("Testing ThingSpeak API connection...")
    try:
        url = f"https://api.thingspeak.com/channels/{THINGSPEAK_CHANNEL_ID}/feeds/last.json"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✓ ThingSpeak API connection successful")
            print(f"  Latest data: {data}")
            return True
        else:
            print(f"✗ ThingSpeak API error: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ ThingSpeak connection error: {e}")
        return False

def test_dependencies():
    """Test if all required packages are installed"""
    print("Testing dependencies...")
    required_packages = ['flask', 'requests', 'opencv-python', 'numpy']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
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
    """Run all tests"""
    print("IoT Room Monitoring System - Setup Test")
    print("=" * 50)
    
    tests = [
        ("Dependencies", test_dependencies),
        ("Camera", test_camera),
        ("Haar Cascade", test_haar_cascade),
        ("ThingSpeak Config", test_thingspeak_config),
        ("ThingSpeak Connection", test_thingspeak_connection),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name} failed with error: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("Test Summary:")
    all_passed = True
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name}: {status}")
        if not result:
            all_passed = False
    
    if all_passed:
        print("\n✓ All tests passed! Your system is ready to run.")
        print("Run 'python app.py' to start the application.")
    else:
        print("\n✗ Some tests failed. Please fix the issues before running the application.")
        sys.exit(1)

if __name__ == "__main__":
    main()
