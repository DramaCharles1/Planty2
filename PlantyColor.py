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

    def count_pixels(self, image) -> int:
        '''Count amount pf pixels in image'''
        return np.nonzero(image)

    def color_filter_image(self,lower_filter: List[int], upper_filter: List[int],save_result=False, result_path=None, result_name=None):
        '''Save a color filtered version of the original image'''
        hsv = cv2.cvtColor(self.original_image,cv2.COLOR_BGR2HSV)
        lower = np.array(lower_filter)
        upper = np.array(upper_filter)
        mask = cv2.inRange(hsv, lower, upper)
        color_version_image = cv2.bitwise_and(self.original_image,self.original_image,mask=mask)

        if save_result:
            result_path = os.path.join(result_path, result_name)
            cv2.imwrite(result_path, color_version_image)

        return color_version_image
