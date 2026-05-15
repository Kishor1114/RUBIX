import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import cv2
import logging
from .camera import Camera
from ui import overlay
from .face_detector import extract_face_stickers
from scanner.color_detector import classify_colors

logger = logging.getLogger("scan_face")


def scan_single_face(face_name: str, camera_cfg: dict, colors_cfg: dict = None):
    logger.info(f"--- Scan face: {face_name} ---")

    index = camera_cfg.get("index", 0)
    width = camera_cfg.get("width", 640)
    height = camera_cfg.get("height", 480)

    with Camera(index=index, width=width, height=height) as cam:
        while True:
            frame = cam.read()
            grid = overlay.draw_grid(frame.copy())

            cv2.putText(
                grid,
                f"Align {face_name}. SPACE=capture | ESC=cancel",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2,
            )

            cv2.imshow("Scan Face", grid)
            key = cv2.waitKey(1) & 0xFF

            if key == 27:
                return None
            if key == 32:
                capture = frame.copy()
                break

        cv2.destroyWindow("Scan Face")

    stickers = extract_face_stickers(capture)
    if stickers is None or len(stickers) != 9:
        logger.error("Sticker extraction failed")
        return None

    detected = []

    # Learn center
    for i, sticker in enumerate(stickers):
        if i == 4:
            classify_colors(sticker, face_hint=face_name, is_center=True)
        detected.append(sticker)

    logger.info(f"{face_name} scanned")
    return detected
