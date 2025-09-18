# IoT Room Monitoring System

A Flask web application that displays real-time room entry count from ThingSpeak IoT platform and uses computer vision to detect people currently in the room.

## Features

- **IoT Integration**: Fetches entry count data from ThingSpeak channels
- **Advanced People Detection**: Uses multiple Haar cascades (face + body) with smoothing
- **Live Camera Feed**: Streams video with detection overlays and confidence indicators
- **Detection Accuracy**: Implements detection smoothing and confidence scoring
- **Calibration Tool**: Interactive tool to fine-tune detection parameters
- **Modern UI**: Built with Tailwind CSS for a clean, responsive interface
- **Auto-refresh**: Automatically updates data every few seconds

## Prerequisites

- Python 3.7+
- Webcam/Camera
- ThingSpeak account and channel (for IoT data)

## Installation

1. **Clone or download the project**
   ```bash
   cd clumsy-coders-kits
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure ThingSpeak**
   - Open `app.py`
   - Replace `YOUR_CHANNEL_ID` with your ThingSpeak channel ID
   - Replace `YOUR_API_KEY` with your ThingSpeak API key
   - Make sure your ThingSpeak channel has data in `field1`

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the web interface**
   - Open your browser and go to `http://localhost:5000`

## Configuration

### ThingSpeak Setup

1. Create a ThingSpeak account at [https://thingspeak.com](https://thingspeak.com)
2. Create a new channel
3. Note down your Channel ID and API Key
4. Update the configuration in `app.py`:
   ```python
   THINGSPEAK_CHANNEL_ID = "YOUR_CHANNEL_ID"
   THINGSPEAK_API_KEY = "YOUR_API_KEY"
   ```

### Camera Setup

- Ensure your webcam is connected and working
- The application will automatically detect and use the default camera
- If you have multiple cameras, you may need to change the camera index in `app.py`:
   ```python
   camera = cv2.VideoCapture(0)  # Change 0 to 1, 2, etc. for different cameras
   ```

## API Endpoints

- `GET /` - Main web interface
- `GET /api/entry_count` - Returns IoT entry count from ThingSpeak
- `GET /api/people_count` - Returns current people count from camera
- `GET /video_feed` - Live camera feed with face detection

## How It Works

1. **IoT Data**: The app fetches entry count data from your ThingSpeak channel every 5 seconds
2. **Advanced People Detection**: Uses multiple detection methods:
   - Face detection with Haar cascades
   - Body detection (if available)
   - Detection smoothing to reduce false positives/negatives
   - Confidence scoring based on detection consistency
3. **Real-time Updates**: The web interface automatically refreshes data and displays live statistics
4. **Video Streaming**: Provides a live camera feed with detection overlays and confidence indicators

## Improving Detection Accuracy

### Calibration Tool
Run the calibration tool to fine-tune detection parameters:
```bash
python calibration_tool.py
```

**Controls:**
- Arrow keys: Adjust detection parameters
- Space: Toggle detection overlay
- S: Save current settings
- R: Reset to defaults
- Q: Quit

### Detection Parameters
- **Scale Factor**: Lower values = more sensitive detection
- **Min Neighbors**: Higher values = fewer false positives
- **Min Size**: Minimum face size to detect
- **Confidence**: Based on detection consistency over time

## Troubleshooting

### Camera Issues
- Make sure your camera is not being used by another application
- Check if the camera permissions are granted
- Try changing the camera index in `app.py`

### ThingSpeak Issues
- Verify your Channel ID and API Key are correct
- Ensure your ThingSpeak channel has data
- Check your internet connection

### Performance Issues
- Close other applications using the camera
- Reduce the detection frequency by increasing the sleep time in `detect_people()`

## Customization

- **Detection Sensitivity**: Adjust the parameters in `face_cascade.detectMultiScale()`
- **Update Frequency**: Modify the intervals in the JavaScript auto-refresh functions
- **UI Styling**: Customize the Tailwind CSS classes in `templates/index.html`

## License

This project is open source and available under the MIT License.
