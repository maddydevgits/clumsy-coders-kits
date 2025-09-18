#!/usr/bin/env python3
"""
Test script to verify IP camera connection
"""

import cv2
import requests
from config import *

def test_ip_camera_connection():
    """Test IP camera connection and stream"""
    print("IP Camera Connection Test")
    print("=" * 40)
    
    if not USE_IP_CAMERA:
        print("IP Camera is disabled in config.py")
        print("Set USE_IP_CAMERA = True to enable IP camera")
        return False
    
    print(f"Testing IP camera: {IP_CAMERA_URL}")
    
    # Test 1: Check if URL is accessible
    try:
        print("1. Testing URL accessibility...")
        response = requests.get(IP_CAMERA_URL, timeout=5)
        if response.status_code == 200:
            print("✓ URL is accessible")
        else:
            print(f"✗ URL returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"✗ URL is not accessible: {e}")
        print("Please check:")
        print("- IP camera app is running on your phone")
        print("- Phone and computer are on the same network")
        print("- IP address is correct")
        return False
    
    # Test 2: Test OpenCV connection
    print("2. Testing OpenCV connection...")
    try:
        cap = cv2.VideoCapture(IP_CAMERA_URL)
        if not cap.isOpened():
            print("✗ OpenCV cannot open the stream")
            return False
        
        print("✓ OpenCV connection successful")
        
        # Test 3: Read frames
        print("3. Testing frame reading...")
        ret, frame = cap.read()
        if ret:
            print(f"✓ Frame read successful! Size: {frame.shape[1]}x{frame.shape[0]}")
            
            # Save test frame
            cv2.imwrite('ip_camera_test_frame.jpg', frame)
            print("✓ Test frame saved as 'ip_camera_test_frame.jpg'")
            
            # Test multiple frames
            frame_count = 0
            for i in range(10):
                ret, frame = cap.read()
                if ret:
                    frame_count += 1
            
            print(f"✓ Read {frame_count}/10 frames successfully")
            
        else:
            print("✗ Failed to read frame")
            return False
        
        cap.release()
        
    except Exception as e:
        print(f"✗ OpenCV test failed: {e}")
        return False
    
    print("\n✓ All IP camera tests passed!")
    print("Your IP camera is ready for use with Nexora!")
    return True

def test_network_connectivity():
    """Test basic network connectivity"""
    print("Network Connectivity Test")
    print("=" * 30)
    
    # Extract IP from URL
    try:
        ip = IP_CAMERA_URL.split('//')[1].split(':')[0]
        print(f"Testing connectivity to: {ip}")
        
        # Test ping (if available)
        import subprocess
        try:
            result = subprocess.run(['ping', '-c', '1', ip], 
                                   capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print("✓ Network connectivity OK")
                return True
            else:
                print("✗ Network connectivity failed")
                return False
        except:
            print("? Ping test not available (this is OK)")
            return True
            
    except Exception as e:
        print(f"✗ Network test failed: {e}")
        return False

def show_setup_instructions():
    """Show setup instructions"""
    print("\nIP Camera Setup Instructions")
    print("=" * 40)
    print("1. Install IP camera app on your Android phone:")
    print("   - IP Webcam (recommended)")
    print("   - DroidCam")
    print("   - AtHome Camera")
    print()
    print("2. Start the IP camera app and note the IP address")
    print("3. Update config.py with your IP camera URL:")
    print(f"   IP_CAMERA_URL = \"http://YOUR_PHONE_IP:PORT/video\"")
    print()
    print("4. Common URL formats:")
    print("   - IP Webcam: http://192.168.1.100:8080/video")
    print("   - DroidCam: http://192.168.1.100:4747/video")
    print("   - AtHome: http://192.168.1.100:11111/video")
    print()
    print("5. Make sure phone and computer are on the same WiFi network")

def main():
    """Run all IP camera tests"""
    print("Nexora IP Camera Test")
    print("=" * 50)
    
    if not USE_IP_CAMERA:
        show_setup_instructions()
        return
    
    # Test network connectivity
    network_ok = test_network_connectivity()
    
    print("\n" + "=" * 50)
    
    # Test IP camera connection
    if test_ip_camera_connection():
        print("\n✓ IP camera setup is complete!")
        print("You can now run the main Nexora application:")
        print("python app.py")
    else:
        print("\n✗ IP camera setup failed")
        print("Please check the error messages above and try again")
        show_setup_instructions()

if __name__ == "__main__":
    main()
