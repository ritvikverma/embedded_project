import time

import cv2
from imutils.video import VideoStream

vs = VideoStream(src=0).start()  # Uncomment this if you are using Webcam
time.sleep(2)
i = 8
prev_time = time.time()

while True:
    frame = vs.read()
    height, width, channels = frame.shape
    upper_left = (width // 4, height // 4)
    bottom_right = (width * 3 // 4, height * 3 // 4)
    curr_time = time.time()

    if i > 5:
        cv2.rectangle(frame, upper_left, bottom_right, (0, 255, 150), thickness=2)
        cv2.putText(frame, "Please prepare your HKID for scanning", (width // 6, height // 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 150), 2)

    elif 5 >= i > 0:
        cv2.rectangle(frame, upper_left, bottom_right, (0, 255, 150), thickness=2)
        cv2.putText(frame, str(i), (width // 4, height // 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 150), 2)

    elif i == 0:
        cv2.rectangle(frame, upper_left, bottom_right, (0, 255, 150), thickness=2)
        cv2.putText(frame, "Capturing HKID...", (width // 6, height // 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 150), 2)
        cv2.imwrite("temp.jpg", frame)

    elif i % 3 == 0:
        cv2.putText(frame, "HKID Captured. Waiting for results...", (width // 4, height // 2),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 150), 2)

    elif i % 3 == 1:
        cv2.putText(frame, "HKID Captured. Waiting for results..", (width // 4, height // 2),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 150), 2)

    elif i % 3 == 2:
        cv2.putText(frame, "HKID Captured. Waiting for results.", (width // 4, height // 2),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 150), 2)

    cv2.imshow("COVID-19 Vaccine Verification System", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key is pressed, break from the loop
    if key == ord("q"):
        break

    if curr_time - prev_time >= 1:
        i -= 1
        prev_time = curr_time

cv2.destroyAllWindows()
vs.stop()
