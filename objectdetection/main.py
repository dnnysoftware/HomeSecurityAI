import cv2
from stopwatch import Stopwatch
import asyncio
from src.video import Video
from src.classification_model import Classification_Model

def security_program():
    vid = Video()
    video = vid.create_video()

    ai = Classification_Model()
    net = ai.create_model()
    class_names = ai.get_object_classifiers()
    
    capture(vid, video, net, ai, class_names)
    asyncio.run(vid.post_videos())
    vid.clear_videos(vid.data_file_folder)
    
def capture(vid, video, net, ai, class_names):
    result = None
    is_active = False
    stopwatch = Stopwatch(0)
    stopwatch.reset()
    while True:
        try: 
            _ , frame = video.read()
            class_ids, confs, bbox = net.detect(frame, confThreshold=0.5)
            print(stopwatch.duration, class_ids, bbox)      
            if len(class_ids) != 0:
                for classId, confidence, box in zip(class_ids.flatten(), confs.flatten(), bbox):
                    ai.classify_object(frame, box, class_names, confidence, classId)
                    if class_names[classId-1].upper() == "PERSON" and confidence*100>70:
                        stopwatch.reset()
                        stopwatch.stop()
                        if not is_active:
                            result = ai.classified_new_person(vid, video)
                            is_active = True
                    elif class_names[classId-1].upper() != "PERSON" and is_active and int(stopwatch.duration) == 0:
                        stopwatch.start()        
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
            if is_active:
                result.write(frame)
                if int(stopwatch.duration) > 30:
                    result.release()
                    is_active = False
                    stopwatch.reset()
            cv2.imshow('Object Detector', frame)
        except:
            continue
    

def main():
    security_program()
    

if __name__ == "__main__":
    main()