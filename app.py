from flask import Flask, render_template, jsonify, Response
import requests
import cv2
import numpy as np
import threading
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from datetime import datetime, timedelta
from ultralytics import YOLO
from config import *

app = Flask(__name__)

# ThingSpeak configuration
THINGSPEAK_URL = f"https://api.thingspeak.com/channels/{THINGSPEAK_CHANNEL_ID}/feeds/last.json"

# Global variables for camera
camera = None
yolo_model = None
detection_history = []  # Store recent detection counts for smoothing
current_detection_data = {  # Store current detection data for API
    'people_count': 0,
    'detections': [],
    'confidence': 'LOW',
    'model': 'YOLO'
}

# Email alert tracking
last_alert_time = None
previous_people_count = 0
alert_history = []  # Store alert history
threshold_crossed_up = False  # Track if threshold was crossed upward
threshold_crossed_down = False  # Track if threshold was crossed downward

def init_camera():
    """Initialize camera and YOLO model"""
    global camera, yolo_model
    
    # Initialize camera
    camera = cv2.VideoCapture(CAMERA_INDEX)
    if not camera.isOpened():
        print("Error: Could not open camera")
        return False
    
    # Set camera properties for better detection and quality
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, VIDEO_FRAME_WIDTH)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, VIDEO_FRAME_HEIGHT)
    camera.set(cv2.CAP_PROP_FPS, 30)
    camera.set(cv2.CAP_PROP_BRIGHTNESS, 0.5)  # Adjust brightness for better text visibility
    camera.set(cv2.CAP_PROP_CONTRAST, 0.5)     # Adjust contrast for better text visibility
    
    # Initialize YOLO model
    try:
        print(f"Loading YOLO model: {YOLO_MODEL}")
        yolo_model = YOLO(YOLO_MODEL)
        print("YOLO model loaded successfully!")
        return True
    except Exception as e:
        print(f"Error loading YOLO model: {e}")
        print("Falling back to Haar cascades...")
        return init_camera_fallback()
    
def init_camera_fallback():
    """Fallback initialization with Haar cascades"""
    global camera
    print("Using Haar cascade fallback")
    return True

def detect_people_yolo(frame):
    """YOLO-based people detection with smoothing"""
    global detection_history, current_detection_data, yolo_model
    
    if yolo_model is None:
        return 0, []
    
    # Run YOLO detection
    results = yolo_model(frame, 
                         conf=YOLO_CONFIDENCE_THRESHOLD,
                         iou=YOLO_IOU_THRESHOLD,
                         classes=YOLO_CLASSES,
                         verbose=False)
    
    # Extract person detections
    detections = []
    if len(results) > 0:
        for result in results:
            boxes = result.boxes
            if boxes is not None:
                for box in boxes:
                    # Get bounding box coordinates
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    confidence = box.conf[0].cpu().numpy()
                    class_id = int(box.cls[0].cpu().numpy())
                    
                    # Only process person detections (class 0)
                    if class_id == 0:
                        detections.append({
                            'bbox': [int(x1), int(y1), int(x2), int(y2)],
                            'confidence': float(confidence),
                            'class': 'person'
                        })
    
    detected_count = len(detections)
    
    # Apply smoothing to reduce false positives/negatives
    detection_history.append(detected_count)
    if len(detection_history) > 10:  # Keep only last 10 detections
        detection_history.pop(0)
    
    # Use median of recent detections for stability
    smoothed_count = int(np.median(detection_history)) if detection_history else 0
    
    # Calculate confidence based on detection consistency
    confidence = "LOW"
    if len(detection_history) >= 5:
        recent_detections = detection_history[-5:]
        if len(set(recent_detections)) <= 1:
            confidence = "HIGH"
        elif len(set(recent_detections)) <= 2:
            confidence = "MEDIUM"
    
    # Update global detection data for API
    current_detection_data.update({
        'people_count': smoothed_count,
        'detections': detections,
        'confidence': confidence,
        'model': 'YOLO'
    })
    
    # Check alert conditions every 30 frames (about once per second)
    if len(detection_history) % 30 == 0:
        avg_confidence = np.mean([d['confidence'] for d in detections]) if detections else 0
        print(f"YOLO Detection: {smoothed_count} people, {len(detections)} detections, avg confidence: {avg_confidence:.2f}, stability: {confidence}")
        
        # Check and send email alerts
        alerts_sent = check_alert_conditions(smoothed_count)
        if alerts_sent:
            print(f"Email alerts sent: {', '.join(alerts_sent)}")
    
    return smoothed_count, detections

# Email Alert Functions
def send_email_alert(subject, message, image_data=None):
    """Send email alert via Gmail SMTP"""
    global last_alert_time
    
    if not EMAIL_ENABLED:
        return False
    
    # Check cooldown period
    if last_alert_time:
        time_since_last = datetime.now() - last_alert_time
        if time_since_last < timedelta(minutes=ALERT_COOLDOWN_MINUTES):
            print(f"Email alert skipped - cooldown period active ({ALERT_COOLDOWN_MINUTES} minutes)")
            return False
    
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = f"{EMAIL_FROM_NAME} <{EMAIL_USERNAME}>"
        msg['To'] = ", ".join(EMAIL_RECIPIENTS)
        msg['Subject'] = f"[Nexora Alert] {subject}"
        
        # Add text content
        body = f"""
Nexora Room Monitoring System Alert

{message}

Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
System: Nexora by Clumsy Coders
Location: Room Monitoring Station

This is an automated alert from the Nexora monitoring system.
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Add image if provided
        if image_data is not None:
            image_part = MIMEImage(image_data)
            image_part.add_header('Content-Disposition', 'attachment', filename='detection_snapshot.jpg')
            msg.attach(image_part)
        
        # Send email
        server = smtplib.SMTP(EMAIL_SMTP_SERVER, EMAIL_SMTP_PORT)
        server.starttls()
        server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        
        text = msg.as_string()
        server.sendmail(EMAIL_USERNAME, EMAIL_RECIPIENTS, text)
        server.quit()
        
        # Update last alert time
        last_alert_time = datetime.now()
        
        # Log alert
        alert_history.append({
            'timestamp': datetime.now(),
            'subject': subject,
            'recipients': len(EMAIL_RECIPIENTS)
        })
        
        print(f"Email alert sent successfully: {subject}")
        return True
        
    except Exception as e:
        print(f"Failed to send email alert: {e}")
        return False

def check_alert_conditions(current_count):
    """Check if alert conditions are met and send alerts - only on threshold crossings"""
    global previous_people_count, threshold_crossed_up, threshold_crossed_down
    
    alerts_sent = []
    
    if ALERT_ONLY_THRESHOLD_CROSS:
        # Only alert when crossing the threshold (up or down)
        
        # Check if crossing threshold upward
        if (previous_people_count <= PEOPLE_COUNT_THRESHOLD and 
            current_count > PEOPLE_COUNT_THRESHOLD and 
            not threshold_crossed_up):
            
            subject = f"Threshold Exceeded - {current_count} People Detected"
            message = f"The room occupancy has crossed the threshold!\n\nPrevious count: {previous_people_count} people\nCurrent count: {current_count} people\nThreshold: {PEOPLE_COUNT_THRESHOLD} people\n\nAlert: Occupancy is now above the limit."
            
            if send_email_alert(subject, message):
                alerts_sent.append("threshold_crossed_up")
                threshold_crossed_up = True
                threshold_crossed_down = False  # Reset downward flag
        
        # Check if crossing threshold downward
        elif (previous_people_count > PEOPLE_COUNT_THRESHOLD and 
              current_count <= PEOPLE_COUNT_THRESHOLD and 
              not threshold_crossed_down):
            
            subject = f"Threshold Cleared - {current_count} People Detected"
            message = f"The room occupancy has returned below the threshold.\n\nPrevious count: {previous_people_count} people\nCurrent count: {current_count} people\nThreshold: {PEOPLE_COUNT_THRESHOLD} people\n\nAlert: Occupancy is now within normal limits."
            
            if send_email_alert(subject, message):
                alerts_sent.append("threshold_crossed_down")
                threshold_crossed_down = True
                threshold_crossed_up = False  # Reset upward flag
    
    else:
        # Legacy behavior - alert on every threshold exceed
        if ALERT_ON_THRESHOLD and current_count > PEOPLE_COUNT_THRESHOLD:
            subject = f"High Occupancy Alert - {current_count} People Detected"
            message = f"The room occupancy has exceeded the threshold of {PEOPLE_COUNT_THRESHOLD} people.\n\nCurrent count: {current_count} people\nThreshold: {PEOPLE_COUNT_THRESHOLD} people"
            if send_email_alert(subject, message):
                alerts_sent.append("threshold")
        
        # Check entry alert
        if ALERT_ON_ENTRY and current_count > previous_people_count:
            subject = f"Person Entered - {current_count} People Now in Room"
            message = f"Someone has entered the room.\n\nPrevious count: {previous_people_count} people\nCurrent count: {current_count} people"
            if send_email_alert(subject, message):
                alerts_sent.append("entry")
        
        # Check exit alert
        if ALERT_ON_EXIT and current_count < previous_people_count:
            subject = f"Person Exited - {current_count} People Now in Room"
            message = f"Someone has exited the room.\n\nPrevious count: {previous_people_count} people\nCurrent count: {current_count} people"
            if send_email_alert(subject, message):
                alerts_sent.append("exit")
    
    # Update previous count
    previous_people_count = current_count
    
    return alerts_sent

# Note: detect_people() function removed - now using synchronized detection in generate_frames()

def get_thingspeak_data():
    """Fetch data from ThingSpeak"""
    try:
        response = requests.get(THINGSPEAK_URL, timeout=5)
        if response.status_code == 200:
            data = response.json()
            # Assuming the entry count is in field1, adjust as needed
            entry_count = data.get('field1', 0)
            return int(entry_count) if entry_count else 0
        else:
            print(f"ThingSpeak API error: {response.status_code}")
            return 0
    except Exception as e:
        print(f"Error fetching ThingSpeak data: {e}")
        return 0

def generate_frames():
    """Generate video frames for streaming with YOLO detection"""
    global camera, yolo_model
    while True:
        if camera is None:
            break
            
        ret, frame = camera.read()
        if not ret:
            print("Failed to read frame from camera")
            break
        
        # Apply YOLO detection
        current_count, detections = detect_people_yolo(frame)
        
        # Draw YOLO detection rectangles with confidence scores
        for i, detection in enumerate(detections):
            x1, y1, x2, y2 = detection['bbox']
            confidence = detection['confidence']
            
            # Draw thick border
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)  # Black border
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Green rectangle
            
            # Draw person label with confidence score
            label = f'Person {i+1}: {confidence:.2f}'
            cv2.putText(frame, label, (x1, y1-15), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 3)  # Black border
            cv2.putText(frame, label, (x1, y1-15), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)  # Green text
        
        # Add comprehensive status information with better text rendering
        # Main count with thick border for better visibility
        cv2.putText(frame, f'People Count: {current_count}', (10, 35), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 4)  # Black border
        cv2.putText(frame, f'People Count: {current_count}', (10, 35), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)  # Green text
        
        # Detection count with border
        cv2.putText(frame, f'Detections: {len(detections)}', (10, 70), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 3)  # Black border
        cv2.putText(frame, f'Detections: {len(detections)}', (10, 70), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)  # Green text
        
        # Model info with border
        cv2.putText(frame, f'Model: YOLO', (10, 105), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 3)  # Black border
        cv2.putText(frame, f'Model: YOLO', (10, 105), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 255), 2)  # Magenta text
        
        # Add detection confidence indicator with border
        confidence = current_detection_data['confidence']
        cv2.putText(frame, f'Stability: {confidence}', (10, 140), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 3)  # Black border
        cv2.putText(frame, f'Stability: {confidence}', (10, 140), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)  # Yellow text
        
        # Add timestamp with border
        timestamp = time.strftime("%H:%M:%S")
        cv2.putText(frame, timestamp, (frame.shape[1] - 120, frame.shape[0] - 25), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 3)  # Black border
        cv2.putText(frame, timestamp, (frame.shape[1] - 120, frame.shape[0] - 25), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)  # White text
        
        # Encode frame as JPEG with high quality settings for better text visibility
        encode_param = [
            int(cv2.IMWRITE_JPEG_QUALITY), VIDEO_JPEG_QUALITY,
            int(cv2.IMWRITE_JPEG_OPTIMIZE), 1,  # Enable optimization
            int(cv2.IMWRITE_JPEG_PROGRESSIVE), 1  # Progressive JPEG for better streaming
        ]
        ret, buffer = cv2.imencode('.jpg', frame, encode_param)
        if not ret:
            print("Failed to encode frame")
            break
            
        frame_bytes = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/entry_count')
def api_entry_count():
    """API endpoint for IoT entry count"""
    count = get_thingspeak_data()
    return jsonify({'entry_count': count})

@app.route('/api/people_count')
def api_people_count():
    """API endpoint for current people count from camera"""
    global current_detection_data
    return jsonify({'people_count': current_detection_data['people_count']})

@app.route('/video_feed')
def video_feed():
    """Video streaming route"""
    if camera is None:
        return "Camera not initialized", 500
    return Response(generate_frames(),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/camera_status')
def api_camera_status():
    """API endpoint for camera status"""
    global camera
    if camera is None:
        return jsonify({'status': 'error', 'message': 'Camera not initialized'})
    
    if not camera.isOpened():
        return jsonify({'status': 'error', 'message': 'Camera not opened'})
    
    return jsonify({'status': 'active', 'message': 'Camera is working'})

@app.route('/api/detection_details')
def api_detection_details():
    """API endpoint for detailed detection information"""
    global current_detection_data, detection_history, yolo_model
    
    return jsonify({
        'people_count': current_detection_data['people_count'],
        'confidence': current_detection_data['confidence'],
        'detection_history': detection_history[-10:],  # Last 10 detections
        'model': current_detection_data['model'],
        'detections': current_detection_data['detections'],
        'detection_count': len(current_detection_data['detections']),
        'yolo_enabled': yolo_model is not None,
        'avg_confidence': np.mean([d['confidence'] for d in current_detection_data['detections']]) if current_detection_data['detections'] else 0
    })

@app.route('/api/email_status')
def api_email_status():
    """API endpoint for email alert status"""
    global last_alert_time, alert_history, threshold_crossed_up, threshold_crossed_down
    
    return jsonify({
        'email_enabled': EMAIL_ENABLED,
        'last_alert_time': last_alert_time.isoformat() if last_alert_time else None,
        'alert_count': len(alert_history),
        'recipients': len(EMAIL_RECIPIENTS),
        'threshold': PEOPLE_COUNT_THRESHOLD,
        'cooldown_minutes': ALERT_COOLDOWN_MINUTES,
        'threshold_crossing_mode': ALERT_ONLY_THRESHOLD_CROSS,
        'threshold_status': {
            'crossed_up': threshold_crossed_up,
            'crossed_down': threshold_crossed_down,
            'currently_above': current_detection_data['people_count'] > PEOPLE_COUNT_THRESHOLD
        },
        'alert_types': {
            'on_entry': ALERT_ON_ENTRY,
            'on_exit': ALERT_ON_EXIT,
            'on_threshold': ALERT_ON_THRESHOLD,
            'only_threshold_cross': ALERT_ONLY_THRESHOLD_CROSS
        }
    })

@app.route('/api/send_test_email')
def api_send_test_email():
    """API endpoint to send a test email"""
    subject = "Test Alert - Nexora System"
    message = "This is a test email from the Nexora room monitoring system.\n\nIf you receive this email, the email alert system is working correctly!"
    
    success = send_email_alert(subject, message)
    
    return jsonify({
        'success': success,
        'message': 'Test email sent successfully' if success else 'Failed to send test email'
    })

if __name__ == '__main__':
    # Initialize camera
    if init_camera():
        print("Starting Nexora by Clumsy Coders...")
        print("Camera initialized successfully!")
        print("Make sure to update THINGSPEAK_CHANNEL_ID and THINGSPEAK_API_KEY in config.py")
        print(f"Access the application at: http://{FLASK_HOST}:{FLASK_PORT}")
        app.run(debug=FLASK_DEBUG, host=FLASK_HOST, port=FLASK_PORT)
    else:
        print("Failed to initialize camera. Please check your camera connection.")
