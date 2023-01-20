import cv2
import datetime
from src.sms import SMS


class Classification_Model:

    def __init__(self):
        self.config_path = 'objectdetection/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
        self.weights_path = 'objectdetection/frozen_inference_graph.pb'
        self.class_file = 'objectdetection/coco.names'

    def create_model(self):
        """ Creates the detection model with weights found in the .pb file
        and the path to the pbtxt file containing key - value pairs for COCO dataset
        elements to be identified
        Returns:
            Model: returns the trained detection model
        """
        net = cv2.dnn_DetectionModel(self.weights_path, self.config_path)
        net.setInputSize(320,320)
        net.setInputScale(1.0/127.5)
        net.setInputMean((127.5, 127.5, 127.5))
        net.setInputSwapRB(True)
        return net

    def get_object_classifiers(self):
        """ Derives the names in the COCO data set
        Returns:
            List: names of object classifiers that can be detected
        """
        class_names = []
        with open(self.class_file, 'rt') as f:
            class_names = f.read().rstrip('\n').split('\n')
        return class_names

    def classify_object(self, frame, box, class_names, confidence, classId):
        """ Classified any object gets green frame showing user that an item from
        COCO dataset has been found
        """
        cv2.rectangle(frame, box, color=(0,255,0), thickness=2)
        cv2.putText(frame, class_names[classId-1].upper(), (box[0]+10, box[1]+30), cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
        cv2.putText(frame, str(round(confidence*100, 2)),(box[0]+150, box[1]+30), cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2) 

    def classified_new_person(self, vid, video):
        """ When person from COCO dataset has been identified then starts
        a counter then begins recording a video instances, then sends sms 
        message to phone number, then returns the video instance being recorded

        Returns:
            VideoWriter: returns the video being recorded
        """
        ct = datetime.datetime.now().replace(microsecond=0)
        result = vid.record_video(ct, video)
        sms = SMS(ct)
        sms.send_sms()
        return result
    

