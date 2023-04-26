import numpy as np
import cv2
import time
import HandTrackingModule as htm
import math

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volrange = volume.GetVolumeRange()
#volume.SetMasterVolumeLevel(-60.0, None)
minVol = volrange[0]
maxVol = volrange[1]
vol = 0
volbar = 150

ptime = 0 
ctime = 0
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('m','j','p','g'))
detector = htm.handDetector(detectionCon=0.7)
while cap.isOpened():
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) !=0:
        # print(lmList[4], lmList[8])
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1+x2)//2 , (y1+y2)//2
        cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)
        if y2<=y1:
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 2)
        else:
            cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
        
        length = math.hypot(x2-x1, y2-y1)
        if length<25:
            cv2.circle(img, (cx, cy), 10, (0, 0, 255), cv2.FILLED)
        
        # hand range 25 - 250
        # volume range -65 - 0

        vol = np.interp(length, [25, 300], [minVol, maxVol])
        volbar = np.interp(length, [25, 300], [400, 150])

        # print(int(length), vol)
        volume.SetMasterVolumeLevel(vol, None)
    
    cv2.rectangle(img, (50, 150), (75, 400), (0, 255, 0))
    cv2.rectangle(img, (50, int(volbar)), (75, 400), (0, 255, 0), cv2.FILLED)

    ctime = time.time()
    fps = 1/(ctime-ptime)
    ptime = ctime
    cv2.putText(img, f'FPS: {int(fps)}', (30, 30), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0), 2)
    if success:
        image = cv2.resize(img, (800,400))
        cv2.imshow('Camera', image)
        if cv2.waitKey(25) & 0xff == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()
