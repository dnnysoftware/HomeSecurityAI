import os
import cv2
import aioboto3

"""
Responsible for creating video display, recording video from that display, 
temporarily saving recorded videos, sending video data to an AWS s3 bucket 
using the aioboto3 which does asynchronous s3 operations.
"""
class Video:

    def __init__(self):
        self.data_file_folder = os.path.join(os.getcwd(), 'objectdetection/Video')
    
    def create_video(self):
        """ Video capture creates the display with cv2
        Returns:
            VideoCapture: to be used in the video capture algorithm for object classification & detection
        """
        video = cv2.VideoCapture(0) # gets data from first webcam on local machine
        video.set(3, 1280)
        video.set(4, 720)
        if video.isOpened() == False:
            print("Error reading video file")
        return video
    
    def record_video(self, ct, video):
        """ Records new video and names file with current datetime, finally save/writes to Video folder
        Returns:
            VideoWriter: Object that writes frames onto a .webm formatted file
        """
        frame_width = int(video.get(3))
        frame_height = int(video.get(4))
        size = (frame_width, frame_height)
        recorder = cv2.VideoWriter("objectdetection/Video/{}.webm".format(str(ct)), 
                            cv2.VideoWriter_fourcc('V','P','8','0'),
                            10, size)
        return recorder

    def clear_videos(self):
        """Deletes videos in Video directory
        """
        for file in os.listdir(self.data_file_folder):
            os.remove(os.path.join(self.data_file_folder, file))
    
    async def post_videos(self):
        """ asynchronously post videos into AWS s3 bucket.
        """
        client_session = aioboto3.Session(aws_access_key_id=os.environ.get("AWS_ACCESS_KEY"), aws_secret_access_key=os.environ.get("AWS_SECRET_KEY"))
        async with client_session.client('s3') as client_s3:
            for file in os.listdir(self.data_file_folder):
                if not file.startswith('~'):
                    try:
                        print("UPLOADING FILE: {}".format(file))
                        await client_s3.upload_file(os.path.join(self.data_file_folder, file), os.environ.get("AWS_SECURITY_BUCKET_NAME"), file)
                        print("UPLOAD COMPLETE")
                    except Exception as e:
                        print("Error Upload: {}".format(e))
                os.remove(os.path.join(self.data_file_folder, file))