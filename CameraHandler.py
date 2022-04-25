import os
from shutil import copyfile
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
        full_path = os.path.join(path, f"{picture_name}.jpg")
        if nightmode:
            self.camera.iso = 800
        else:
            self.camera.iso = 100

        self.camera.start_preview()
        time.sleep(2) #Camera warm up time
        self.camera.capture(full_path)
        self.camera.stop_preview()
        if not self._check_picture_exist(path, picture_name):
            raise Exception(f"[DEBUG] Picture {full_path} could not be saved")

    def copy_picture(self, source_path, original_name, dest_path, copy_name):
        '''Copy picture and save in path as picture_name'''
        if not self._check_picture_exist(source_path, original_name):
            raise FileExistsError(f"[DEBUG] File {source_path}/{original_name} does not exist")
        copyfile(os.path.join(source_path, f"{original_name}.jpg"),
        os.path.join(dest_path, f"{copy_name}.jpg"))

    def _check_picture_exist(self, path, picture_name) -> bool:
        return os.path.isfile(os.path.join(path, f"{picture_name}.jpg"))

if __name__ == "__main__":
    print("Camera test")
    path = ""
    test_picture = "test_night"
    cam = CameraHandler()
    cam.take_picture(path, test_picture, nightmode=True)
