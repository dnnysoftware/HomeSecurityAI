import os
from time import sleep
import boto3
import cv2
from twilio.rest import Client
from stopwatch import Stopwatch
import datetime


def send_sms(ct):
    ct = datetime.datetime.now().replace(microsecond=0)

    account_sid = os.environ.get("ACCOUNT_SID")

    auth_token  = os.environ.get("AUTH_TOKEN")

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to=os.environ.get("TARGET_NUMBER"), 
        from_=os.environ.get("TWILIO_NUMBER"),
        body="There was a Person Detected by your camera at " + str(ct))

    print(message.sid)

def capture_images():
    ct = datetime.datetime.now().replace(microsecond=0)

    video = cv2.VideoCapture(0)
    video.set(3, 640)
    video.set(4, 480)
    if video.isOpened() == False:
        print("Error reading video file")

    # frame_width = int(video.get(3))
    # frame_height = int(video.get(4))
    # size = (frame_width, frame_height)
    # result = cv2.VideoWriter("objectdetection/media/{}.avi".format(str(ct)), 
    #                      cv2.VideoWriter_fourcc(*'MJPG'),
    #                      10, size)

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
    
    result = 0
    isPersonActive = False
    personMissingStopwatch = Stopwatch(0)
    personMissingStopwatch.reset()
    while True:
        try: 
            _ , frame = video.read()
            classIds, confs, bbox = net.detect(frame, confThreshold=0.5)
            print(personMissingStopwatch.duration, classIds, bbox)      
            if len(classIds) != 0:
                for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
                    cv2.rectangle(frame, box, color=(0,255,0), thickness=2)
                    cv2.putText(frame, classNames[classId-1].upper(), (box[0]+10, box[1]+30), cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                    cv2.putText(frame, str(round(confidence*100, 2)),(box[0]+150, box[1]+30), cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                    if classNames[classId-1].upper() == "PERSON" and confidence*100>70:
                        personMissingStopwatch.reset()
                        personMissingStopwatch.stop()
                        if not isPersonActive:
                            frame_width = int(video.get(3))
                            frame_height = int(video.get(4))
                            size = (frame_width, frame_height)
                            ct = datetime.datetime.now().replace(microsecond=0)
                            result = cv2.VideoWriter("objectdetection/media/{}.avi".format(str(ct)), 
                                                cv2.VideoWriter_fourcc(*'MJPG'),
                                                10, size)
                            isPersonActive = True
                            send_sms(ct)
                    elif classNames[classId-1].upper() != "PERSON" and isPersonActive and int(personMissingStopwatch.duration) == 0:
                        personMissingStopwatch.start()        
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            if isPersonActive:
                result.write(frame)
                if int(personMissingStopwatch.duration) > 30:
                    result.release()
                    post_media()
                    isPersonActive = False
                    personMissingStopwatch.reset()
            cv2.imshow('Object Detector', frame)
        except:
            continue
    try:
        video.release()
        result.release()
        cv2.destroyAllWindows()
    finally:
        print("No videos to upload")

def post_media():
    client_s3 = boto3.client('s3', 
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_KEY"))

    data_file_folder = os.path.join(os.getcwd(), 'objectdetection/media')
    for file in os.listdir(data_file_folder):
        if not file.startswith('~'):
            client_s3.upload_file(os.path.join(data_file_folder, file),
            os.environ.get("AWS_SECURITY_BUCKET_NAME"), file)
        os.remove(os.path.join(data_file_folder, file))

def main():
    capture_images()
    


if __name__ == "__main__":
    main()