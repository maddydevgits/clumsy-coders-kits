#!/usr/bin/env python3
"""
Test script to verify browser camera functionality
"""

import requests
import cv2
import numpy as np
from config import *

def test_browser_camera_config():
    """Test browser camera configuration"""
    print("🔍 Testing Browser Camera Configuration...")
    
    # Check if browser camera is enabled
    if CAMERA_TYPE == "browser":
        print("✅ Browser camera mode is enabled")
        print(f"   - Camera type: {CAMERA_TYPE}")
        print(f"   - Browser camera width: {BROWSER_CAMERA_WIDTH}")
        print(f"   - Browser camera height: {BROWSER_CAMERA_HEIGHT}")
        print(f"   - Browser camera FPS: {BROWSER_CAMERA_FPS}")
        return True
    else:
        print(f"❌ Browser camera mode is not enabled. Current type: {CAMERA_TYPE}")
        print("   To enable browser camera, set CAMERA_TYPE = 'browser' in config.py")
        return False

def test_api_endpoint():
    """Test the process_frame API endpoint"""
    print("\n🔍 Testing API Endpoint...")
    
    try:
        # Create a test image
        test_image = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.putText(test_image, "Test Frame", (200, 240), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
        
        # Encode as JPEG
        ret, buffer = cv2.imencode('.jpg', test_image)
        image_bytes = buffer.tobytes()
        
        # Test API endpoint
        url = "http://localhost:5000/api/process_frame"
        files = {'frame': ('test.jpg', image_bytes, 'image/jpeg')}
        
        response = requests.post(url, files=files)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API endpoint is working!")
            print(f"   - People count: {data.get('people_count', 'N/A')}")
            print(f"   - Confidence: {data.get('confidence', 'N/A')}")
            print(f"   - Detections: {len(data.get('detections', []))}")
            return True
        else:
            print(f"❌ API endpoint failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server")
        print("   Make sure the Flask app is running: python3 app.py")
        return False
    except Exception as e:
        print(f"❌ Error testing API: {e}")
        return False

def test_yolo_model():
    """Test YOLO model loading"""
    print("\n🔍 Testing YOLO Model...")
    
    try:
        from ultralytics import YOLO
        model = YOLO(YOLO_MODEL)
        print("✅ YOLO model loaded successfully!")
        print(f"   - Model: {YOLO_MODEL}")
        print(f"   - Confidence threshold: {YOLO_CONFIDENCE_THRESHOLD}")
        print(f"   - IOU threshold: {YOLO_IOU_THRESHOLD}")
        return True
    except Exception as e:
        print(f"❌ Error loading YOLO model: {e}")
        return False

def test_browser_compatibility():
    """Test browser compatibility features"""
    print("\n🔍 Testing Browser Compatibility...")
    
    # Check if we're in a browser environment
    try:
        import webbrowser
        print("✅ Browser module available")
        
        # Test HTML template
        with open('templates/index.html', 'r') as f:
            html_content = f.read()
            
        if 'getUserMedia' in html_content:
            print("✅ getUserMedia API found in HTML")
        else:
            print("❌ getUserMedia API not found in HTML")
            
        if 'startBrowserCamera' in html_content:
            print("✅ Browser camera functions found in HTML")
        else:
            print("❌ Browser camera functions not found in HTML")
            
        if 'api/process_frame' in html_content:
            print("✅ Process frame API endpoint found in HTML")
        else:
            print("❌ Process frame API endpoint not found in HTML")
            
        return True
        
    except Exception as e:
        print(f"❌ Error testing browser compatibility: {e}")
        return False

def main():
    """Run all tests"""
    print("📱 Browser Camera Functionality Test")
    print("=" * 50)
    
    tests = [
        ("Configuration", test_browser_camera_config),
        ("YOLO Model", test_yolo_model),
        ("Browser Compatibility", test_browser_compatibility),
        ("API Endpoint", test_api_endpoint)
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} test failed: {e}")
            results[test_name] = False
    
    print("\n📊 Test Results Summary:")
    print("=" * 30)
    for test_name, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    passed = sum(results.values())
    total = len(results)
    
    print(f"\n🎯 Overall Score: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Browser camera is ready for cloud deployment!")
        print("\n🚀 Next Steps:")
        print("1. Open http://localhost:5000 in your browser")
        print("2. Click '📷 Start Camera' button")
        print("3. Allow camera access when prompted")
        print("4. Test people detection")
        print("5. Deploy to cloud platform")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure Flask app is running: python3 app.py")
        print("2. Check config.py settings")
        print("3. Verify all dependencies are installed")
        print("4. Check browser console for errors")

if __name__ == "__main__":
    main()
