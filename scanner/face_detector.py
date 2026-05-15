import cv2
import numpy as np
import logging

logger = logging.getLogger("face_detector")


def extract_face_stickers(frame):
    """
    Extracts the 9 grid regions (stickers) from the given frame.
    This matches the 3×3 grid drawn in ui/overlay.py.

    Returns:
        List of 9 sticker images (cropped), ordered row-wise:
        [top-left, top-mid, top-right, mid-left, ..., bottom-right]
    """

    if frame is None:
        logger.error("extract_sticker_regions(): frame is None")
        return None

    h, w, _ = frame.shape

    # Define margins so the stickers fall inside the overlay grid
    margin_w = int(w * 0.20)   # 20% left/right margin
    margin_h = int(h * 0.15)   # 15% top/bottom margin

    grid_w = w - 2 * margin_w
    grid_h = h - 2 * margin_h

    cell_w = grid_w // 3
    cell_h = grid_h // 3

    stickers = []

    # Extract 9 subregions
    for row in range(3):
        for col in range(3):

            x_start = margin_w + col * cell_w
            y_start = margin_h + row * cell_h

            x_end = x_start + cell_w
            y_end = y_start + cell_h

            crop = frame[y_start:y_end, x_start:x_end]

            if crop.size == 0:
                logger.error("Invalid crop region detected!")
                return None

            stickers.append(crop)

    logger.debug("Extracted 9 sticker regions successfully")
    return stickers
