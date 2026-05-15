import logging
from cube.model import Cube
from cube.validate import validate_cube
from solver.pure_kociemba import solve_cube
from scanner.color_detector import classify_colors





logger = logging.getLogger("web_solver")


def solve_from_scanned_faces(scan_state):

    faces = scan_state.get_faces()
    SOLVER_ORDER = ["U", "R", "F", "D", "L", "B"]
    facelet = []

    for face in SOLVER_ORDER:
        for sticker in faces[face]:
            color = classify_colors(sticker)
            facelet.append(color_to_face_letter(color))

    facelet_string = "".join(facelet)
    logger.info(f"Facelet string: {facelet_string}")

    cube = Cube(facelet_string)
    validate_cube(cube)

    return solve_cube(facelet_string)


def color_to_face_letter(color):
    COLOR_TO_FACE = {
        "white": "D",
        "yellow": "U",
        "green": "F",
        "blue": "B",
        "red": "R",
        "orange": "L",
    }

    if color not in COLOR_TO_FACE:
        raise RuntimeError(f"Unknown color detected: {color}")

    return COLOR_TO_FACE[color]
