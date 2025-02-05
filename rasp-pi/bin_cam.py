import cv2
import time
import os
from datetime import datetime
import requests

PROJ = "test"
PATH = "/home/pi/telebrick/rasp-pi"
URL = "http://10.0.0.185:80/"

def cap_img(name):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error opening webcam")
        return False
    ret, img = cap.read()
    if not ret:
        return False
    cv2.imwrite(name, img)
    cap.release()
    return True

def send_img(name):
    with open(name, 'rb') as jpg:
        files = {"file": jpg}
        try:
            response = requests.post(URL + "upload", files=files)
        except Exception:
            print("Error sending img")
            return False
    return True

def is_full(url):
    status = requests.get(url + "full")
    return status.json()["full"]

if __name__ == "__main__":
    for f in os.listdir(PATH):
        if f.endswith(".jpg"):
            f_path = os.path.join(PATH, f)
            os.remove(f_path)

    while True:
        rn = datetime.now()
        im_name = rn.strftime("%Y%m%d%H%M") + PROJ + ".jpg"
        cap_img(im_name)
        send_img(im_name)
        os.remove(im_name)
        print(is_full(URL))
        time.sleep(5)

