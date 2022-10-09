import os
import boto3
import cv2
from twilio.rest import Client
from stopwatch import Stopwatch
import datetime

def clear_local_videos(data_file_folder):
    for file in os.listdir(data_file_folder):
        os.remove(os.path.join(data_file_folder, file))

def post_video():
    client_s3 = boto3.client('s3', 
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_KEY"))

    data_file_folder = os.path.join(os.getcwd(), 'objectdetection/Video')
    for file in os.listdir(data_file_folder):
        if not file.startswith('~'):
            client_s3.upload_file(os.path.join(data_file_folder, file),
            os.environ.get("AWS_SECURITY_BUCKET_NAME"), file)
        os.remove(os.path.join(data_file_folder, file))