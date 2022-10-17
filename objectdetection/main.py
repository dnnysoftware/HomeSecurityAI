import cv2
from stopwatch import Stopwatch
import datetime
import asyncio
from src.sms import SMS
from src.video import Video
from src.classification_model import Classification_Model

def capture_images():

    vid = Video()
    video = vid.create_video()

    ai = Classification_Model()
    net = ai.create_model()
    class_names = ai.get_object_classifiers()
    
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
                    ai.classify_object(frame, box, class_names, confidence, classId)
                    if class_names[classId-1].upper() == "PERSON" and confidence*100>70:
                        personMissingStopwatch.reset()
                        personMissingStopwatch.stop()
                        if not isPersonActive:
                            ct = datetime.datetime.now().replace(microsecond=0)
                            result = vid.record_video(ct, video)
                            sms = SMS(ct)
                            sms.send_sms()
                            isPersonActive = True
                    elif class_names[classId-1].upper() != "PERSON" and isPersonActive and int(personMissingStopwatch.duration) == 0:
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
        result.release()
        video.release()
        cv2.destroyAllWindows()
    except:
        print("No videos to upload")
    finally:
        asyncio.run(vid.post_videos())
        vid.clear_videos(vid.data_file_folder)
    

def main():
    capture_images()
    

if __name__ == "__main__":
    main()