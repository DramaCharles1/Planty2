import os
from typing import List
import cv2
import numpy as np

class PlantyColor:
    '''Class that handles everything related to OpenCV, filtering
    and image calculation. Everything is calculated from original_image open from
    path and image name'''
    def __init__(self, path, image_name) -> None:
        full_path = os.path.join(path, image_name)
        if not os.path.isfile(full_path):
            raise FileExistsError(f"[DEBUG] Image: {full_path}")
        self.original_image = cv2.imread(full_path)

    def color_filter_image(self,lower_filter: List[int], upper_filter: List[int]):
        '''Save a color filtered version of the original image'''
        hsv = cv2.cvtColor(self.original_image,cv2.COLOR_BGR2HSV)
        lower = np.array(lower_filter)
        upper = np.array(upper_filter)
        mask = cv2.inRange(hsv, lower, upper)
        color_version_image = cv2.bitwise_and(self.original_image,self.original_image,mask=mask)

        return color_version_image

    def save_image(self, image, result_path, result_name):
        if not os.path.isdir(result_path):
            raise FileExistsError(f"[DEBUG] Directory: {result_path} does not exist")
        full_path = os.path.join(result_path, result_name)
        cv2.imwrite(full_path, image)

if __name__ == "__main__":
    print("PlantyColor test")
    plantycolor = PlantyColor("", "default.jpg")
    print(f"Pixels: {np.count_nonzero(plantycolor.original_image)}")
    print(f"Filter image")
    lower_green = [40, 50, 50]
    upper_greeen = [80, 250, 250]
    curr_dir = os.curdir
    plantycolor.save_image(plantycolor.color_filter_image(lower_green, upper_greeen), curr_dir, "filtered.jpg")
