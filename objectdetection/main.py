import os
import cv2
from stopwatch import Stopwatch
import datetime
import asyncio
import aioboto3
from src.sms import SMS
from src.video import Video
from src.classification_model import Classification_Model

def capture_images():

    vid = Video()
    video = vid.create_video()


    classNames = []
    classFile = 'objectdetection/coco.names'
    with open(classFile, 'rt') as f:
        classNames = f.read().rstrip('\n').split('\n') 

    ai = Classification_Model()
    net = ai.create_model()
    
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
                            result = cv2.VideoWriter("objectdetection/Video/{}.webm".format(str(ct)), 
                                                cv2.VideoWriter_fourcc('V','P','8','0'),
                                                10, size)
                            isPersonActive = True
                            sms = SMS(ct)
                            sms.send_sms()
                    elif classNames[classId-1].upper() != "PERSON" and isPersonActive and int(personMissingStopwatch.duration) == 0:
                        personMissingStopwatch.start()        
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            if isPersonActive:
                result.write(frame)
                if int(personMissingStopwatch.duration) > 30:
                    result.release()
                    isPersonActive = False
                    personMissingStopwatch.reset()
            cv2.imshow('Object Detector', frame)
        except:
            continue
    try:
        video.release()
        result.release()
        cv2.destroyAllWindows()
    except:
        print("No videos to upload")
    finally:
        asyncio.run(vid.async_post_videos())
        vid.clear_local_videos(vid.data_file_folder)



def main():
    capture_images()
    

if __name__ == "__main__":
    main()