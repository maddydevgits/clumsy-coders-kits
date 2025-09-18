# Configuration file for IoT Room Monitoring System

# ThingSpeak Configuration
# Replace these with your actual ThingSpeak channel details
THINGSPEAK_CHANNEL_ID = "YOUR_CHANNEL_ID"  # Your ThingSpeak channel ID
THINGSPEAK_API_KEY = "YOUR_API_KEY"        # Your ThingSpeak API key

# Camera Configuration
CAMERA_INDEX = 0  # Change this if you have multiple cameras (0, 1, 2, etc.)

# Camera Configuration Options
CAMERA_TYPE = "browser"  # Options: "browser", "local", "ip_camera", "rtsp", "web_url"

# Browser Camera (Recommended for cloud deployment)
USE_BROWSER_CAMERA = True  # Use browser's camera via WebRTC
BROWSER_CAMERA_WIDTH = 640  # Browser camera width
BROWSER_CAMERA_HEIGHT = 480  # Browser camera height
BROWSER_CAMERA_FPS = 30  # Browser camera FPS

# Local Camera (for local development)
USE_LOCAL_CAMERA = False  # Use local webcam on server

# IP Camera Configuration (for local deployment)
USE_IP_CAMERA = False  # Set to True to use IP camera, False for local webcam
IP_CAMERA_URL = "http://192.168.1.100:8080/video"  # Replace with your IP camera URL
IP_CAMERA_USERNAME = ""  # Leave empty if no authentication
IP_CAMERA_PASSWORD = ""  # Leave empty if no authentication

# RTSP Stream Configuration (for cloud deployment)
RTSP_URL = "rtsp://username:password@your-camera-ip:554/stream"  # RTSP stream URL
RTSP_USERNAME = ""  # RTSP username
RTSP_PASSWORD = ""  # RTSP password

# Web URL Configuration (for cloud deployment)
WEB_CAMERA_URL = "https://your-webcam-service.com/video"  # Web-based camera service
WEB_CAMERA_API_KEY = ""  # API key if required

# YOLO Detection Configuration
YOLO_MODEL = "yolov8n.pt"  # YOLOv8 nano model (fastest)
YOLO_CONFIDENCE_THRESHOLD = 0.5  # Minimum confidence for detection
YOLO_IOU_THRESHOLD = 0.45  # Intersection over Union threshold
YOLO_CLASSES = [0]  # Class 0 = person in COCO dataset

# Legacy Haar Cascade Settings (kept for fallback)
FACE_DETECTION_SCALE_FACTOR = 1.05  # Lower = more sensitive detection
FACE_DETECTION_MIN_NEIGHBORS = 5    # Higher = fewer false positives
FACE_DETECTION_MIN_SIZE = (30, 30)  # Minimum face size to detect
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

# Video Quality Settings
VIDEO_JPEG_QUALITY = 95            # JPEG quality for video stream (1-100)
VIDEO_FRAME_WIDTH = 640            # Video frame width
VIDEO_FRAME_HEIGHT = 480           # Video frame height

# Flask Configuration
FLASK_HOST = '0.0.0.0'
FLASK_PORT = 2000
FLASK_DEBUG = True

# Email Alert Configuration
EMAIL_ENABLED = True
EMAIL_SMTP_SERVER = 'smtp.gmail.com'
EMAIL_SMTP_PORT = 587
EMAIL_USERNAME = 'YOUR_EMAIL@gmail.com'  # Your Gmail address
EMAIL_PASSWORD = 'YOUR_APP_PASSWORD'     # Gmail App Password (not regular password)
EMAIL_FROM_NAME = 'Nexora Alert System'

# Email Recipients
EMAIL_RECIPIENTS = [
    'admin@example.com',  # Add recipient emails here
    'manager@example.com'
]

# Alert Thresholds
PEOPLE_COUNT_THRESHOLD = 5  # Send alert when people count exceeds this
ALERT_COOLDOWN_MINUTES = 5  # Minimum time between alerts (in minutes)
ALERT_ON_ENTRY = False      # Send alert when someone enters
ALERT_ON_EXIT = False       # Send alert when someone exits
ALERT_ON_THRESHOLD = True   # Send alert when threshold is exceeded
ALERT_ONLY_THRESHOLD_CROSS = True  # Only alert when crossing threshold (up or down)
