from re import T
import cv2
import sys
from datetime import datetime
from threading import Thread
from multiprocessing import Process
import os

video_stream_link = 'rtsp://A6S2qUFT:kKMzrKzKJm4vZqu1@192.168.86.31:554/live/ch1'

def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())

class VideoCaptureObject(object):
    def __init__(self, src=0):
        # Create a VideoCapture object
        self.capture = cv2.VideoCapture(src)
        # Default resolutions of the frame are obtained (system dependent)
        self.frame_width = int(self.capture.get(3))
        self.frame_height = int(self.capture.get(4))
        # Set up codec and output video settings
#        self.codec = cv2.VideoWriter_fourcc('M','J','P','G')
#        self.output_video = cv2.VideoWriter('output.avi', self.codec, 30, (self.frame_width, self.frame_height))
        # Start the thread to read frames from the video stream
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

    def update(self):
        # Read the next frame from the stream in a different thread
        while True:
            if self.capture.isOpened():
                (self.status, self.frame) = self.capture.read()

    def show_frame(self):
        # Display frames in main program
        if self.capture.isOpened():
            if self.status:
                cv2.imshow('frame', self.frame)
                return True
            else:
                now = datetime.now()
                print('err: no frame!', now, self.frame, self.capture.isOpened())
                self.capture.release()
                return False
        else:
            print('err2: not opened!', self.capture.isOpened())
            self.capture.release()
            return False

#    def save_frame(self):
#        # Save obtained frame into video output file
#        self.output_video.write(self.frame)

def video_preview(fn):
    info('video_preview')
    video_stream_widget = VideoCaptureObject(fn)
    print(video_stream_widget)

    isOpened = True
    while isOpened and cv2.waitKey(1) != 27: # Escape
        try:
            isOpened = video_stream_widget.show_frame()
        except AttributeError:
            pass

#    video_stream_widget.release()
    cv2.destroyAllWindows()
    exit(1)

if __name__ == '__main__':
    while True:
        info('main line')
        p = Process(target=video_preview, args=(video_stream_link,))
        p.start()
        p.join()
