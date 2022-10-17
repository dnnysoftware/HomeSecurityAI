import os
import cv2
import aioboto3
from src.sms import SMS

class Video:

    def __init__(self):
        self.data_file_folder = os.path.join(os.getcwd(), 'objectdetection/Video')
    
    def create_video(self):
        video = cv2.VideoCapture(0)
        video.set(3, 1280)
        video.set(4, 720)
        if video.isOpened() == False:
            print("Error reading video file")
        return video
    
    def record_video(self, ct, video):
        frame_width = int(video.get(3))
        frame_height = int(video.get(4))
        size = (frame_width, frame_height)
        recorder = cv2.VideoWriter("objectdetection/Video/{}.webm".format(str(ct)), 
                            cv2.VideoWriter_fourcc('V','P','8','0'),
                            10, size)
        return recorder

    def clear_videos(self, data_file_folder):
        for file in os.listdir(data_file_folder):
            os.remove(os.path.join(data_file_folder, file))
    
    async def post_videos(self):
        client_session = aioboto3.Session(aws_access_key_id=os.environ.get("AWS_ACCESS_KEY"), aws_secret_access_key=os.environ.get("AWS_SECRET_KEY"))
        async with client_session.client('s3') as client_s3:
            data_file_folder = os.path.join(os.getcwd(), 'objectdetection/Video')
            for file in os.listdir(data_file_folder):
                if not file.startswith('~'):
                    try:
                        print("UPLOADING FILE: ", file)
                        await client_s3.upload_file(os.path.join(data_file_folder, file), os.environ.get("AWS_SECURITY_BUCKET_NAME"), file)
                        print("UPLOAD COMPLETE")
                    except Exception as e:
                        print("Error Upload: ", e)
                os.remove(os.path.join(data_file_folder, file))