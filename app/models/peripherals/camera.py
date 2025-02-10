import os
import cv2
from datetime import datetime

from app.helpers.time import TIME_HELPER
from app.models.base import BaseModel
from app.services.systems.config import CONFIG

class CameraModel(BaseModel):

    def __init__(self, index=0, name="front", resolution=(640, 480), fps=30):
        self.recording = None
        self.video_writer = None

        self.index = index
        self.name = name
        self.output_dir = str(os.path.join(CONFIG.storage_dir, CONFIG.cameras['output_dir'], name))
        self.resolution = resolution
        self.fps = fps

        try:
            self.camera = cv2.VideoCapture(self.index, cv2.CAP_V4L2)
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1])
            self.camera.set(cv2.CAP_PROP_FPS, self.fps)
        except Exception as e:
            raise f"Camera {self.name} not found!"

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    @classmethod
    def from_dict(cls, config: dict):
        return cls(index=config.get("index", 0),
                   name=config.get("name", "front"),
                   resolution=(config.get("resolution", {}).get("width", 640),
                               config.get("resolution", {}).get("height", 480)),
                   fps=config.get("fps", 30))

    def get_properties(self):
        return {
            "index": self.index,
            "resolution": self.resolution,
            "fps": self.fps,
            "output_dir": self.output_dir,
            "is_opened": self.camera.isOpened()
        }

    def is_opened(self):
        return self.camera.isOpened()

    def capture_image(self, filename=None, custom_path=None):
        if not self.camera.isOpened():
            raise Exception("Camera is not open!")

        ret, frame = self.camera.read()
        if not ret:
            raise Exception("Camera is not ready!")

        if filename is None:
            filename = TIME_HELPER.get_current_time_for_file() + ".jpg"

        file_path = os.path.join(self.output_dir, filename)

        cv2.imwrite(file_path, frame)

        return file_path

    def start_video_recording(self, filename=None):
        if not self.camera.isOpened():
            raise Exception("Camera is not open!")

        if filename is None:
            filename = TIME_HELPER.get_current_time_for_file() +".avi"

        file_path = os.path.join(str(self.output_dir), filename)

        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.video_writer = cv2.VideoWriter(str(file_path), fourcc, self.fps, self.resolution)

        self.recording = True
        while self.recording:
            ret, frame = self.camera.read()
            if not ret:
                break
            self.video_writer.write(frame)

        self.video_writer.release()
        return file_path

    def stop_video_recording(self):
        self.recording = False

    def show_live_feed(self):
        if not self.camera.isOpened():
            raise Exception("Camera is not open!")

        while True:
            ret, frame = self.camera.read()
            if not ret:
                break
            cv2.imshow('Live Feed', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()

    def release(self):
        self.camera.release()
        cv2.destroyAllWindows()