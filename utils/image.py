import cv2
import numpy as np


def crop_center(frame, percent=0.5):
    """
    Crops the center portion of an image.
    percent=0.5 means keep 50% of width & height.
    """

    h, w = frame.shape[:2]
    cw, ch = int(w * percent), int(h * percent)

    x1 = (w - cw) // 2
    y1 = (h - ch) // 2

    return frame[y1:y1 + ch, x1:x1 + cw]


def resize_keep_ratio(img, width=None, height=None):
    """
    Resize while keeping aspect ratio.
    """
    h, w = img.shape[:2]

    if width is None and height is None:
        return img

    if width is not None:
        scale = width / w
    else:
        scale = height / h

    new_w = int(w * scale)
    new_h = int(h * scale)

    return cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)


def perspective_warp(img, src_points, dst_size):
    """
    src_points = 4 corner points of region.
    dst_size = (width, height)

    Useful for advanced face alignment (optional).
    """
    dst_points = np.array([
        [0, 0],
        [dst_size[0], 0],
        [dst_size[0], dst_size[1]],
        [0, dst_size[1]]
    ], dtype=np.float32)

    M = cv2.getPerspectiveTransform(np.array(src_points, dtype=np.float32),
                                    dst_points)

    warped = cv2.warpPerspective(img, M, dst_size)
    return warped
