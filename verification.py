import time

import cv2
from imutils.video import VideoStream
from pyzbar import pyzbar

from data_processing import get_vaccine_data, get_triangulated_data
from ocr_extractor import execute

vs = VideoStream(src=0).start()
time.sleep(2)
countdown_timer = 20
prev_time = time.time()
vaccine_data = {}
hkid_data = ''
final_results = {'vaccination_date': '12234234',
                 'vaccine': 'Comirnaty',
                 'hkid_number': '',
                 'name': '',
                 }
BARCODE_SCAN = 0
HKID_SCAN = 1
RESULTS = 2
mode = BARCODE_SCAN


def get_text():
    return execute('temp.jpg')


while True:
    frame = vs.read()
    frame = cv2.resize(frame, (800, 450))
    height, width, channels = frame.shape
    upper_left = (width // 5, height // 5)
    bottom_right = (width * 4 // 5, height * 4 // 5)
    curr_time = time.time()

    if mode == RESULTS:
        if all(list(final_results.values())):
            cv2.putText(frame, "Welcome!", (width // 5, height // 7),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 150), 2)
            cv2.putText(frame, "Name: " + final_results['name'], (width // 5, height * 2 // 7),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 150), 2)
            cv2.putText(frame, "Vaccination Date: " + final_results['vaccination_date'], (width // 5, height * 3 // 7),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 150), 2)
            cv2.putText(frame, "Vaccine: " + final_results['vaccine'], (width // 5, height * 4 // 7),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 150), 2)
            cv2.putText(frame, "HKID Number: " + final_results['hkid_number'], (width // 5, height * 5 // 7),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 150), 2)

        else:
            cv2.putText(frame, "Verification Failed.", (width // 5, height // 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    elif mode == HKID_SCAN:
        if countdown_timer > 5:
            cv2.rectangle(frame, upper_left, bottom_right, (0, 255, 150), thickness=2)
            cv2.putText(frame, "Please prepare your HKID for scanning", (width // 6, height // 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 150), 2)

        elif 5 >= countdown_timer > 0:
            cv2.rectangle(frame, upper_left, bottom_right, (0, 255, 150), thickness=2)
            cv2.putText(frame, str(countdown_timer), (width // 4, height // 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 150), 2)

        elif countdown_timer == 0:
            cv2.rectangle(frame, upper_left, bottom_right, (0, 255, 150), thickness=2)
            cv2.putText(frame, "Capturing HKID...", (width // 6, height // 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 150), 2)
            cv2.imwrite("temp.jpg", frame)

        elif countdown_timer == -1:
            cv2.putText(frame, "HKID Captured. Waiting for results...", (width // 5, height // 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 150), 2)
            hkid_data = get_text()['raw_text']

        elif countdown_timer == -2:
            mode = RESULTS
            final_results = get_triangulated_data(vaccine_data, hkid_data)

    elif vaccine_data and countdown_timer <= 10:
        mode = HKID_SCAN

    elif not vaccine_data and countdown_timer <= 10:
        cv2.putText(frame, "ERROR! Please restart the COVID vaccine verification process", (width // 6, height // 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        if countdown_timer < 5:
            break

    elif mode == BARCODE_SCAN:
        cv2.putText(frame, "Please present your vaccination QR code", (width // 6, height // 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 150), 2)
        barcodes = pyzbar.decode(frame)
        for barcode in barcodes:
            (x, y, w, h) = barcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            barcodeData = barcode.data.decode("utf-8")
            try:
                vaccine_data = get_vaccine_data(barcodeData)
            except:
                vaccine_data = {}

            text = vaccine_data['name'] + "(" + vaccine_data['hkid'] + ")"
            cv2.putText(frame, text, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    if curr_time - prev_time >= 1:
        countdown_timer -= 1
        prev_time = curr_time

    cv2.imshow("COVID-19 Vaccine Verification System", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key is pressed, break from the loop
    if key == ord("q"):
        break

cv2.destroyAllWindows()
vs.stop()
