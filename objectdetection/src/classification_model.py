import os
import cv2
from stopwatch import Stopwatch
import datetime
import asyncio
from src.sms import SMS
from src.video import Video

class Classification_Model:

    def __init__(self):
        self.config_path = 'objectdetection/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
        self.weights_path = 'objectdetection/frozen_inference_graph.pb'

    def create_model(self):
        net = cv2.dnn_DetectionModel(self.weights_path, self.config_path)
        net.setInputSize(320,320)
        net.setInputScale(1.0/127.5)
        net.setInputMean((127.5, 127.5, 127.5))
        net.setInputSwapRB(True)
        return net