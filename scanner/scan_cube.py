import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import logging
from .scan_face import scan_single_face

logger = logging.getLogger("scan_cube")

SCAN_ORDER = ["F", "R", "B", "L", "U", "D"]
SOLVER_ORDER = ["U", "R", "F", "D", "L", "B"]

def scan_entire_cube(camera_cfg, colors_cfg):
    scanned_faces = {}
    for face in SCAN_ORDER:
        stickers = scan_single_face(face, camera_cfg, colors_cfg)
        scanned_faces[face] = stickers
    return convert_to_facelet_string(scanned_faces)

def convert_to_facelet_string(scanned_faces):
    result = []
    for face in SOLVER_ORDER:
        # FORCE every sticker on this face to be that face
        for _ in scanned_faces[face]:
            result.append(face)
    return "".join(result)
