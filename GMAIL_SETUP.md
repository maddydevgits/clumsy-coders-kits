# Gmail SMTP Setup Guide for Nexora Email Alerts

This guide will help you set up Gmail SMTP for email alerts in the Nexora room monitoring system.

## Step 1: Enable 2-Factor Authentication

1. Go to your Google Account settings: https://myaccount.google.com/
2. Click on "Security" in the left sidebar
3. Under "Signing in to Google", click "2-Step Verification"
4. Follow the prompts to enable 2-factor authentication

## Step 2: Generate App Password

1. In your Google Account settings, go to "Security"
2. Under "Signing in to Google", click "App passwords"
3. Select "Mail" as the app
4. Select "Other (custom name)" as the device
5. Enter "Nexora Alert System" as the name
6. Click "Generate"
7. **Copy the 16-character password** (it will look like: abcd efgh ijkl mnop)

## Step 3: Configure Nexora

1. Open `config.py` in your Nexora project
2. Update the email settings:

```python
# Email Alert Configuration
EMAIL_ENABLED = True
EMAIL_SMTP_SERVER = 'smtp.gmail.com'
EMAIL_SMTP_PORT = 587
EMAIL_USERNAME = 'your-email@gmail.com'  # Your Gmail address
EMAIL_PASSWORD = 'abcd efgh ijkl mnop'   # The 16-character app password
EMAIL_FROM_NAME = 'Nexora Alert System'

# Email Recipients
EMAIL_RECIPIENTS = [
    'admin@yourcompany.com',  # Add recipient emails here
    'manager@yourcompany.com'
]
```

## Step 4: Test Email Setup

1. Start the Nexora application:
   ```bash
   python app.py
   ```

2. Open the web interface: http://localhost:2000

3. Scroll down to the "Email Alert System" section

4. Click "Send Test Email" button

5. Check your email inbox for the test message

## Alert Types

The system can send alerts for:

- **Threshold Crossing Alerts**: When occupancy crosses the threshold (up or down)
  - **Threshold Exceeded**: When people count goes above the threshold
  - **Threshold Cleared**: When people count returns below the threshold
- **Entry Alerts**: When someone enters the room (disabled by default)
- **Exit Alerts**: When someone leaves the room (disabled by default)

## Configuration Options

In `config.py`, you can customize:

```python
# Alert Thresholds
PEOPLE_COUNT_THRESHOLD = 5  # Send alert when people count exceeds this
ALERT_COOLDOWN_MINUTES = 5  # Minimum time between alerts (in minutes)
ALERT_ON_ENTRY = False      # Send alert when someone enters
ALERT_ON_EXIT = False       # Send alert when someone exits
ALERT_ON_THRESHOLD = True   # Send alert when threshold is exceeded
ALERT_ONLY_THRESHOLD_CROSS = True  # Only alert when crossing threshold (up or down)
```

## Troubleshooting

### "Authentication failed" error
- Make sure you're using the App Password, not your regular Gmail password
- Ensure 2-factor authentication is enabled
- Double-check the email address and app password

### "Connection refused" error
- Check your internet connection
- Verify the SMTP server and port settings
- Some networks block SMTP ports - try using a different network

### Emails not being received
- Check spam/junk folder
- Verify recipient email addresses are correct
- Check the cooldown period - alerts are limited to prevent spam

### Test email fails
- Verify all email settings in config.py
- Check console output for error messages
- Ensure Gmail account is not locked or restricted

## Security Notes

- Never commit your email credentials to version control
- Use App Passwords instead of your main Gmail password
- Consider using a dedicated Gmail account for alerts
- Regularly rotate your App Passwords

## Email Template

The system sends emails with:
- Clear subject line with alert type
- Detailed message with current and previous counts
- Timestamp and system information
- Professional formatting

Example emails:

**Threshold Exceeded:**
```
Subject: [Nexora Alert] Threshold Exceeded - 6 People Detected

Nexora Room Monitoring System Alert

The room occupancy has crossed the threshold!

Previous count: 4 people
Current count: 6 people
Threshold: 5 people

Alert: Occupancy is now above the limit.

Timestamp: 2024-01-15 14:30:25
System: Nexora by Clumsy Coders
Location: Room Monitoring Station

This is an automated alert from the Nexora monitoring system.
```

**Threshold Cleared:**
```
Subject: [Nexora Alert] Threshold Cleared - 4 People Detected

Nexora Room Monitoring System Alert

The room occupancy has returned below the threshold.

Previous count: 6 people
Current count: 4 people
Threshold: 5 people

Alert: Occupancy is now within normal limits.

Timestamp: 2024-01-15 14:35:10
System: Nexora by Clumsy Coders
Location: Room Monitoring Station

This is an automated alert from the Nexora monitoring system.
```

## Support

If you encounter issues:
1. Check the console output for error messages
2. Verify your Gmail settings
3. Test with a simple email client first
4. Check the Nexora documentation for updates
