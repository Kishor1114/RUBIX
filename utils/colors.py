import numpy as np
import cv2

def bgr_to_hsv(bgr):
    return cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)

def average_hsv_region(img):
    """
    Returns average HSV of given image region.
    """
    if img is None or img.size == 0:
        return None

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    avg = hsv.mean(axis=(0, 1))
    return avg

def hsv_distance(hsv1, hsv2):
    """
    Euclidean distance in HSV space.
    """
    hsv1 = np.array(hsv1)
    hsv2 = np.array(hsv2)
    return np.linalg.norm(hsv1 - hsv2)
