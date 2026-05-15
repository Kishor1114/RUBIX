import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import cv2
import numpy as np
import logging

logger = logging.getLogger("color_detector")

CENTER_COLORS = {}   # { "U": hsv, "R": hsv, ... }

def average_hsv(image):
    if image is None or image.size == 0:
        return None

    h, w, _ = image.shape
    x1, x2 = int(w * 0.35), int(w * 0.65)
    y1, y2 = int(h * 0.35), int(h * 0.65)

    center = image[y1:y2, x1:x2]
    hsv = cv2.cvtColor(center, cv2.COLOR_BGR2HSV)
    return hsv.mean(axis=(0,1))


def classify_colors(sticker_img, face_hint=None, is_center=False):
    hsv = average_hsv(sticker_img)
    if hsv is None:
        return "unknown"

    # Learn center
    if is_center and face_hint:
        CENTER_COLORS[face_hint] = hsv
        logger.info(f"Learned center color for {face_hint}: {hsv}")
        return face_hint

    # 🔒 LOCK to own face center
    if face_hint in CENTER_COLORS:
        return face_hint

    # Fallback: global nearest
    if len(CENTER_COLORS) == 6:
        return min(CENTER_COLORS, key=lambda c:
            np.linalg.norm(hsv - CENTER_COLORS[c])
        )

    return "unknown"
