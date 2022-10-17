import cv2
import datetime
from src.sms import SMS


class Classification_Model:

    def __init__(self):
        self.config_path = 'objectdetection/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
        self.weights_path = 'objectdetection/frozen_inference_graph.pb'
        self.class_file = 'objectdetection/coco.names'

    def create_model(self):
        net = cv2.dnn_DetectionModel(self.weights_path, self.config_path)
        net.setInputSize(320,320)
        net.setInputScale(1.0/127.5)
        net.setInputMean((127.5, 127.5, 127.5))
        net.setInputSwapRB(True)
        return net

    def get_object_classifiers(self):
        class_names = []
        with open(self.class_file, 'rt') as f:
            class_names = f.read().rstrip('\n').split('\n')
        return class_names

    def classify_object(self, frame, box, class_names, confidence, classId):
        cv2.rectangle(frame, box, color=(0,255,0), thickness=2)
        cv2.putText(frame, class_names[classId-1].upper(), (box[0]+10, box[1]+30), cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
        cv2.putText(frame, str(round(confidence*100, 2)),(box[0]+150, box[1]+30), cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2) 

    def classified_person(self, stopwatch, vid, video):
        stopwatch.reset()
        stopwatch.stop()
        if not isPersonActive:
            ct = datetime.datetime.now().replace(microsecond=0)
            result = vid.record_video(ct, video)
            sms = SMS(ct)
            sms.send_sms()
            isPersonActive = True

    def process_video(self):
        print()