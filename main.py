import socket
import re
import sys
import cv2
import threading
import sys
import copy
import numpy as np
import tkinter as tk
from PIL import ImageTk, Image
import platform
import time
import contextlib

def start():
    sock.sendto('command'.encode(encoding="utf-8"), tello_address)
    time.sleep(5)

def recv():
    count = 0
    while True:
        try:
            global executed
            executed = ''
            data, server = sock.recvfrom(1518)
            executed = data.decode(encoding="utf-8")
            print(data.decode(encoding="utf-8"))
        except Exception:
            print(Exception)
            break

recvThread = threading.Thread(target=recv)
recvThread.start()


video = None

host = ''
port = 9000
locaddr = (host, port)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tello_address = ('192.168.10.1', 8889)
sock.bind(locaddr)

def start():
    sock.sendto('command'.encode(encoding="utf-8"), tello_address)
    time.sleep(5)


class Streaming:

    started = False
    thread = None
    kill_event = None
    frame = None
    windows = {}
    screen = None

    def stream(self):
        sock.sendto('streamon'.encode(encoding="utf-8"), tello_address)
        time.sleep(1)
        self.kill_event = threading.Event()
        self.thread = threading.Thread(target=self.cv2Video, args=[self.kill_event])
        self.thread.start()
        self.started = True

    def cv2Video(self, stop_event):

        root = tk.Tk()
        cap = cv2.VideoCapture("udp://0.0.0.0:11111", cv2.CAP_FFMPEG)
        _moved = False
        while not stop_event.is_set():
                flag, img = cap.read()
                if flag == True:
                    self.img = img
                    img = cv2.resize(img, (int(img.shape[1] // (2 ** 0.5)), int(img.shape[0] // (2 ** 0.5))))
                    crange = [0,0,0, 0,0,0]
                    color_red=(0,0,255)
                    color_blue=(255,0,0)
                    width = root.winfo_screenwidth()
                    height = root.winfo_screenheight()
                    Centr_X=int(width/2)
                    Centr_Y=int(height/2)
                    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV )
                    h1 = cv2.getTrackbarPos('h1', 'settings')
                    s1 = cv2.getTrackbarPos('s1', 'settings')
                    v1 = cv2.getTrackbarPos('v1', 'settings')
                    h2 = cv2.getTrackbarPos('h2', 'settings')
                    s2 = cv2.getTrackbarPos('s2', 'settings')
                    v2 = cv2.getTrackbarPos('v2', 'settings')

                    # формируем начальный и конечный цвет фильтра
                    h_min = np.array((h1, s1, v1), np.uint8)
                    h_max = np.array((h2, s2, v2), np.uint8)

                    # накладываем фильтр на кадр в модели HSV
                    thresh = cv2.inRange(hsv, h_min, h_max)

                    moments=cv2.moments(thresh,1)
                    dM01 = moments['m01']
                    dM10 = moments['m10']
                    dArea = moments['m00']

                    if dArea>100:
                        x=int(dM10 / dArea)
                        y=int(dM01 / dArea)

                        cv2.circle(img,(x,y),5,color_blue,2)
                        cv2.putText(img,"x%d;y%d" % (x,y),(x+10,y-10),cv2.FONT_HERSHEY_SIMPLEX,1,color_blue,2)

                        cv2.circle(img,(Centr_X,Centr_Y),5,color_red,2)
                        cv2.putText(img,"x%d;y%d" % (Centr_X-x,Centr_Y-y),(Centr_X+10,Centr_Y-10),cv2.FONT_HERSHEY_SIMPLEX,1,color_red,2)

                        cv2.line(img,(x,y),(Centr_X,Centr_Y),color_blue,2)

                    cv2.imshow('Origin',img)
                    cv2.imshow('result', thresh)
                    #cv2.imshow("result", img)
                    if not _moved:
                        crange = [0,0,0, 0,0,0]
                        color_red=(0,0,255)
                        color_blue=(255,0,0)
                        width = root.winfo_screenwidth()
                        height = root.winfo_screenheight()
                        Centr_X=int(width/2)
                        Centr_Y=int(height/2)
                        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV )

                        # формируем начальный и конечный цвет фильтра
                        h_min = np.array((168, 110, 108), np.uint8)
                        h_max = np.array((255, 255, 255), np.uint8)

                        # накладываем фильтр на кадр в модели HSV
                        thresh = cv2.inRange(hsv, h_min, h_max)

                        moments=cv2.moments(thresh,1)
                        dM01 = moments['m01']
                        dM10 = moments['m10']
                        dArea = moments['m00']

                        if dArea>100:
                            x=int(dM10 / dArea)
                            y=int(dM01 / dArea)

                            cv2.circle(img,(x,y),5,color_blue,2)
                            cv2.putText(img,"x%d;y%d" % (x,y),(x+10,y-10),cv2.FONT_HERSHEY_SIMPLEX,1,color_blue,2)

                            cv2.circle(img,(Centr_X,Centr_Y),5,color_red,2)
                            cv2.putText(img,"x%d;y%d" % (Centr_X-x,Centr_Y-y),(Centr_X+10,Centr_Y-10),cv2.FONT_HERSHEY_SIMPLEX,1,color_red,2)

                            cv2.line(img,(x,y),(Centr_X,Centr_Y),color_blue,2)

                            #cv2.imshow('Origin',img)
                        cv2.imshow('result', thresh)

                        cv2.moveWindow("result", width - img.shape[1], 0)
                        _moved = True

                    cv2.waitKey(1)
                    if cv2.getWindowProperty("result", 0) < 0:
                        self.stop()

       # cap.release()
        cv2.destroyAllWindows()

recvThread = threading.Thread(target=recv)
recvThread.start()

# Запуск видео
start()
video = Streaming()
video.stream()

