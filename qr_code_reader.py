import math

import cv2
from pyzbar import pyzbar  # if you get errors, do brew install zbar on terminal


def execute_from_image(img):
    image = cv2.imread(img)
    img_height = math.ceil(image.shape[0] * 0.5)  # Crop ratio for height
    img_width = math.ceil(image.shape[1] * 0.5)  # Crop ratio for width
    cropped = image[-img_height:, 0:img_width]  # little confusing, but image starts from top left, not bottom
    barcodes = pyzbar.decode(cropped)
    for barcode in barcodes:
        barcode_data = barcode.data.decode("utf-8")
        return barcode_data


def get_vaccine_data(vaccine_raw_data):
    vaccine_data = {'hkid': vaccine_raw_data[5],
                    'name': vaccine_raw_data[6],
                    'date': vaccine_raw_data[17],
                    'vaccine': vaccine_raw_data[8]}
    return (vaccine_data)


if __name__ == '__main__':
    try:
        vaccine_raw_data = execute_from_image('./Vaccine_Record_Ritvik.jpg').split('|')
        print(get_vaccine_data(vaccine_raw_data))

    except:
        print('Cannot Read QR code')
