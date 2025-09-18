# IP Camera Setup Guide for Nexora

This guide will help you set up an IP camera using your Android phone to stream video to the Nexora room monitoring system.

## Step 1: Install IP Camera App

### Recommended Apps:
1. **IP Webcam** (Free) - Most popular and reliable
2. **DroidCam** (Free/Paid) - Good quality
3. **EpocCam** (Paid) - Professional features
4. **AtHome Camera** (Free) - Easy setup

### Installation:
1. Go to Google Play Store
2. Search for "IP Webcam" or your preferred app
3. Install the app on your Android phone

## Step 2: Configure IP Camera App

### For IP Webcam:
1. Open the IP Webcam app
2. Scroll down to "Start server"
3. Tap "Start server"
4. Note the IP address shown (e.g., `192.168.1.100:8080`)
5. The camera will start streaming

### For DroidCam:
1. Open DroidCam app
2. Select "WiFi IP" mode
3. Note the IP address and port
4. Start the camera

## Step 3: Find Your Phone's IP Address

### Method 1: From the App
- Most IP camera apps display the IP address when started
- Look for something like: `http://192.168.1.100:8080`

### Method 2: From Phone Settings
1. Go to Settings > WiFi
2. Tap on your connected network
3. Note the IP address (e.g., `192.168.1.100`)

### Method 3: From Router
1. Access your router's admin panel
2. Look for connected devices
3. Find your phone's IP address

## Step 4: Configure Nexora

1. Open `config.py` in your Nexora project
2. Update the IP camera settings:

```python
# IP Camera Configuration
USE_IP_CAMERA = True  # Set to True to use IP camera
IP_CAMERA_URL = "http://192.168.1.100:8080/video"  # Replace with your phone's IP
IP_CAMERA_USERNAME = ""  # Leave empty if no authentication
IP_CAMERA_PASSWORD = ""  # Leave empty if no authentication
```

### Common URL Formats:
- **IP Webcam**: `http://192.168.1.100:8080/video`
- **DroidCam**: `http://192.168.1.100:4747/video`
- **AtHome**: `http://192.168.1.100:11111/video`

## Step 5: Test Connection

1. Start the Nexora application:
   ```bash
   python app.py
   ```

2. Check the console output for:
   ```
   Initializing IP camera: http://192.168.1.100:8080/video
   Camera test successful! Frame size: 640x480
   ```

3. Open the web interface: http://localhost:2000
4. Check if the camera feed is working

## Step 6: Optimize Settings

### For IP Webcam:
1. In the app, go to "Video preferences"
2. Set resolution to 640x480 or 1280x720
3. Set FPS to 15-30
4. Enable "Front camera" if needed
5. Disable "Night vision" for better detection

### For Better Detection:
1. Position phone at room entrance
2. Ensure good lighting
3. Mount phone securely
4. Keep phone charged or plugged in

## Troubleshooting

### "Could not open camera" Error
- **Check IP address**: Make sure the IP address is correct
- **Check network**: Ensure phone and computer are on same WiFi
- **Check app**: Make sure IP camera app is running
- **Check firewall**: Allow connection through firewall

### "No frames received" Error
- **Check URL format**: Ensure URL ends with `/video`
- **Check port**: Verify the port number is correct
- **Restart app**: Close and reopen the IP camera app
- **Check phone**: Ensure phone screen doesn't turn off

### Poor Video Quality
- **Increase resolution**: Set higher resolution in app
- **Check WiFi**: Ensure strong WiFi signal
- **Reduce interference**: Move phone closer to router
- **Close other apps**: Free up phone resources

### Connection Drops
- **Keep phone charging**: Prevent battery saving mode
- **Disable sleep**: Keep phone screen on or disable sleep
- **Check WiFi**: Ensure stable WiFi connection
- **Restart app**: Restart IP camera app periodically

## Security Considerations

### Network Security:
- Use a secure WiFi network
- Consider using VPN for remote access
- Change default passwords if app supports it

### Privacy:
- Position camera appropriately
- Inform people about monitoring
- Follow local privacy laws
- Secure the phone physically

## Advanced Configuration

### Authentication (if supported):
```python
IP_CAMERA_USERNAME = "admin"
IP_CAMERA_PASSWORD = "password"
```

### Custom URLs:
```python
# For different apps
IP_CAMERA_URL = "http://192.168.1.100:8080/video"  # IP Webcam
IP_CAMERA_URL = "http://192.168.1.100:4747/video"  # DroidCam
IP_CAMERA_URL = "http://192.168.1.100:11111/video" # AtHome
```

### Multiple Cameras:
- Use different ports for multiple phones
- Update config for each camera
- Run multiple instances if needed

## Performance Tips

1. **Phone Placement**: Mount phone at optimal height and angle
2. **Lighting**: Ensure consistent lighting conditions
3. **Network**: Use 5GHz WiFi if available
4. **Phone Specs**: Use a phone with good camera and WiFi
5. **Battery**: Keep phone plugged in for continuous operation

## Example Setup

### Complete config.py for IP Camera:
```python
# IP Camera Configuration
USE_IP_CAMERA = True
IP_CAMERA_URL = "http://192.168.1.100:8080/video"
IP_CAMERA_USERNAME = ""
IP_CAMERA_PASSWORD = ""

# YOLO Detection Configuration
YOLO_MODEL = "yolov8n.pt"
YOLO_CONFIDENCE_THRESHOLD = 0.5
YOLO_IOU_THRESHOLD = 0.45
YOLO_CLASSES = [0]  # Person class only

# Alert Thresholds
PEOPLE_COUNT_THRESHOLD = 5
ALERT_ONLY_THRESHOLD_CROSS = True
```

## Support

If you encounter issues:
1. Check the console output for error messages
2. Verify IP camera app is working in browser
3. Test with different IP camera apps
4. Check network connectivity
5. Review this guide for common solutions
