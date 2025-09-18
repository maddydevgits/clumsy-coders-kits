#!/usr/bin/env python3
"""
Test script to verify different camera options for cloud deployment
"""

import cv2
import sys
from config import *

def test_local_camera():
    """Test local camera (works on cloud servers)"""
    print("🔍 Testing Local Camera...")
    try:
        camera = cv2.VideoCapture(CAMERA_INDEX)
        if camera.isOpened():
            ret, frame = camera.read()
            if ret:
                print(f"✅ Local camera working! Frame size: {frame.shape[1]}x{frame.shape[0]}")
                camera.release()
                return True
            else:
                print("❌ Local camera: No frames received")
        else:
            print("❌ Local camera: Could not open")
        camera.release()
    except Exception as e:
        print(f"❌ Local camera error: {e}")
    return False

def test_ip_camera():
    """Test IP camera (won't work on cloud)"""
    print("🔍 Testing IP Camera...")
    try:
        camera = cv2.VideoCapture(IP_CAMERA_URL)
        if camera.isOpened():
            ret, frame = camera.read()
            if ret:
                print(f"✅ IP camera working! Frame size: {frame.shape[1]}x{frame.shape[0]}")
                camera.release()
                return True
            else:
                print("❌ IP camera: No frames received")
        else:
            print("❌ IP camera: Could not open")
        camera.release()
    except Exception as e:
        print(f"❌ IP camera error: {e}")
    return False

def test_rtsp_stream():
    """Test RTSP stream (works on cloud if accessible)"""
    print("🔍 Testing RTSP Stream...")
    try:
        camera = cv2.VideoCapture(RTSP_URL)
        if camera.isOpened():
            ret, frame = camera.read()
            if ret:
                print(f"✅ RTSP stream working! Frame size: {frame.shape[1]}x{frame.shape[0]}")
                camera.release()
                return True
            else:
                print("❌ RTSP stream: No frames received")
        else:
            print("❌ RTSP stream: Could not open")
        camera.release()
    except Exception as e:
        print(f"❌ RTSP stream error: {e}")
    return False

def test_web_camera():
    """Test web camera URL (works on cloud)"""
    print("🔍 Testing Web Camera...")
    try:
        camera = cv2.VideoCapture(WEB_CAMERA_URL)
        if camera.isOpened():
            ret, frame = camera.read()
            if ret:
                print(f"✅ Web camera working! Frame size: {frame.shape[1]}x{frame.shape[0]}")
                camera.release()
                return True
            else:
                print("❌ Web camera: No frames received")
        else:
            print("❌ Web camera: Could not open")
        camera.release()
    except Exception as e:
        print(f"❌ Web camera error: {e}")
    return False

def main():
    """Test all camera options"""
    print("🎥 Camera Options Test for Cloud Deployment")
    print("=" * 50)
    
    # Test current configuration
    print(f"Current camera type: {CAMERA_TYPE}")
    print(f"Current camera index: {CAMERA_INDEX}")
    print(f"IP camera URL: {IP_CAMERA_URL}")
    print(f"RTSP URL: {RTSP_URL}")
    print(f"Web camera URL: {WEB_CAMERA_URL}")
    print()
    
    # Test all options
    results = {
        "Local Camera": test_local_camera(),
        "IP Camera": test_ip_camera(),
        "RTSP Stream": test_rtsp_stream(),
        "Web Camera": test_web_camera()
    }
    
    print("\n📊 Test Results:")
    print("=" * 30)
    for camera_type, success in results.items():
        status = "✅ Working" if success else "❌ Failed"
        print(f"{camera_type}: {status}")
    
    print("\n🌐 Cloud Deployment Recommendations:")
    print("=" * 40)
    
    if results["Local Camera"]:
        print("✅ Local Camera: Perfect for cloud deployment!")
        print("   - Works on cloud servers")
        print("   - No network configuration needed")
        print("   - Set CAMERA_TYPE = 'local' in config.py")
    
    if results["RTSP Stream"]:
        print("✅ RTSP Stream: Good for professional setups!")
        print("   - Works over internet")
        print("   - Secure and reliable")
        print("   - Set CAMERA_TYPE = 'rtsp' in config.py")
    
    if results["Web Camera"]:
        print("✅ Web Camera: Great for cloud services!")
        print("   - Cloud-native solution")
        print("   - Scalable and secure")
        print("   - Set CAMERA_TYPE = 'web_url' in config.py")
    
    if not results["IP Camera"]:
        print("❌ IP Camera: Won't work on cloud!")
        print("   - Local network only")
        print("   - Not accessible from cloud servers")
        print("   - Use for local development only")
    
    print("\n🚀 Next Steps:")
    print("1. Choose a working camera option")
    print("2. Update CAMERA_TYPE in config.py")
    print("3. Deploy to your cloud platform")
    print("4. Test the deployment")

if __name__ == "__main__":
    main()
