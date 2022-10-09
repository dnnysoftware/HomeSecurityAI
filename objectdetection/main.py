import os
import cv2
from twilio.rest import Client
from stopwatch import Stopwatch
import datetime

def send_sms():
    ct = datetime.datetime.now()

    account_sid = os.environ.get("ACCOUNT_SID")

    auth_token  = os.environ.get("AUTH_TOKEN")

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to=os.environ.get("TARGET_NUMBER"), 
        from_=os.environ.get("TWILIO_NUMBER"),
        body="There is a Person Detected by your camera at " + str(ct))

    print(message.sid)

def capture_images():
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    classNames = []
    classFile = 'objectdetection/coco.names'
    with open(classFile, 'rt') as f:
        classNames = f.read().rstrip('\n').split('\n') 

    configPath = 'objectdetection/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
    weightsPath = 'objectdetection/frozen_inference_graph.pb'

    net = cv2.dnn_DetectionModel(weightsPath, configPath)
    net.setInputSize(320,320)
    net.setInputScale(1.0/127.5)
    net.setInputMean((127.5, 127.5, 127.5))
    net.setInputSwapRB(True)
    
    stopwatch = Stopwatch(0)
    stopwatch.start()
    while True:
        try: 
            _ , img = cap.read()
            classIds, confs, bbox = net.detect(img, confThreshold=0.5)
            print(classIds, bbox)
            if len(classIds) != 0:
                for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
                    cv2.rectangle(img, box, color=(0,255,0), thickness=2)
                    cv2.putText(img, classNames[classId-1].upper(), (box[0]+10, box[1]+30), cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                    cv2.putText(img, str(round(confidence*100, 2)),(box[0]+150, box[1]+30), cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                    if classNames[classId-1].upper() == "PERSON" and confidence*100>70:
                        if int(stopwatch.duration) > 60: 
                            send_sms()
                            stopwatch.reset()
                            stopwatch.start()
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            cv2.imshow('Object Detector', img)
            cv2.waitKey(1)
        except:
            continue

def main():
    capture_images()


if __name__ == "__main__":
    main()