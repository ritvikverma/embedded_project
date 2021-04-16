import time

import cv2
import imutils
from imutils.video import VideoStream
from pyzbar import pyzbar

vs = VideoStream(src=0).start()  # Uncomment this if you are using Webcam
time.sleep(2.0)


def get_vaccine_data(vaccine_raw_data):
    vaccine_raw_data = vaccine_raw_data.split('|')
    vaccine_data = {'hkid': vaccine_raw_data[5],
                    'name': vaccine_raw_data[6],
                    'date': vaccine_raw_data[7],
                    'vaccine': vaccine_raw_data[8]}
    return vaccine_data


while True:
    frame = vs.read()
    frame = imutils.resize(frame, width=800)
    barcodes = pyzbar.decode(frame)
    for barcode in barcodes:
        (x, y, w, h) = barcode.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        barcodeData = barcode.data.decode("utf-8")
        vaccine_data = get_vaccine_data(barcodeData)
        text = vaccine_data['name'] + "(" + vaccine_data['hkid'] + ")"
        cv2.putText(frame, text, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    cv2.imshow("COVID-19 Vaccine Verification System", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key is pressed, break from the loop
    if key == ord("q"):
        break

print("[INFO] cleaning up...")
cv2.destroyAllWindows()
vs.stop()
