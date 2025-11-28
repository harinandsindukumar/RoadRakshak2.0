import cv2
import time
import winsound   # Built-in sound - works on Python 3.13 Windows

# Load OpenCV HAAR eye detector
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

# Variables
eye_closed_start = None
last_blink_time = 0
BLINK_SPEED_LIMIT = 0.15  # seconds
DROWSY_LIMIT = 3          # seconds

def alert_sound():
    # frequency, duration(ms)
    winsound.Beep(2000, 700)   # loud beep

print("RoadRakshak AI Started...")
print("Press 'q' to quit\n")

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)

    if len(eyes) == 0:
        if eye_closed_start is None:
            eye_closed_start = time.time()
        else:
            closed_time = time.time() - eye_closed_start

            cv2.putText(frame, f"Eyes Closed: {closed_time:.1f}s",
                        (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            if closed_time >= DROWSY_LIMIT:
                cv2.putText(frame, "⚠ DROWSINESS ALERT!", (20, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
                alert_sound()

    else:
        if eye_closed_start is not None:
            blink_time = time.time() - eye_closed_start
            now = time.time()

            if now - last_blink_time < BLINK_SPEED_LIMIT:
                cv2.putText(frame, "⚠ FAST BLINK ALERT!", (20, 150),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 3)
                alert_sound()

            last_blink_time = now

        eye_closed_start = None

        for (x, y, w, h) in eyes:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow("RoadRakshak AI - Webcam Monitor", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
