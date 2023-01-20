import cv2
from stopwatch import Stopwatch
import asyncio
from src.video import Video
from src.class_detect_model import Classification_Detection_Model


def security_program():
    """ Creates the video to be displayed, creates the object classification and detection
    model, then begins surveying environment data within capture() and records the video from
    the display once it classifies a person, saves that recording to a local directory until the
    recording is quit by pressing 'q' on the display, uploads all stored videos to AWS s3 and removes
    all videos from local directory.
    """
    vid = Video()
    video = vid.create_video()

    ai = Classification_Detection_Model()
    net = ai.create_model()
    class_names = ai.get_object_classifiers()
    
    capture(vid, video, net, ai, class_names)
    asyncio.run(vid.post_videos())
    vid.clear_videos()
    
def capture(vid, video, net, ai, class_names):
    """ Captures the video, records the video once classId/ className is a Person based on
    the COCO image dataset and having a confidence of > 70% . Once recording checks if classified
    "Person" is gone and starts a counter, once that counter reaches 30 seconds then saves the recording
    and begins surveying for the next instance of "Person" from the environment.

    The user needs to key press 'q' on the cv2 display to upload the videos to s3 which in turn quits the 
    program soon after.
    """
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