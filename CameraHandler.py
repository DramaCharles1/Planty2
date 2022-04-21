import os
import time
from picamera import PiCamera

class CameraHandler:
    '''PiCamera module'''
    def __init__(self) -> None:
        try:
            self.camera = PiCamera()
        except Exception as camera_error:
            #print(f"[DEBUG] {camera_error}")
            raise camera_error

    def take_picture(self, path, picture_name, nightmode=False):
        '''Take and save picture picture_name to path'''
        if not os.path.isdir:
            raise FileExistsError(f"[DEBUG] Directory {path} does not exist")
        full_path = os.path.join(path, picture_name)
        print(f"Full path: {full_path}")
        if nightmode:
            self.camera.iso = 100
        else:
            self.camera.iso = 800

        self.camera.start_preview()
        time.sleep(2) #Camera warm up time
        self.camera.capture(full_path)
        self.camera.stop_preview()
        if not self._check_picture_exist(path, picture_name):
            raise Exception(f"[DEBUG] Picture {full_path} could not be saved")

    def _check_picture_exist(self, path, picture_name) -> bool:
        return os.path.isfile(os.path.join(path, picture_name))

if __name__ == "__main__":
    print("Camera test")
    path = ""
    test_picture = "awbgains.jpg"
    cam = CameraHandler()
    cam.take_picture(path, test_picture)
