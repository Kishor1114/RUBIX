import logging
from cube.model import Cube
from cube.validate import validate_cube

# Pure Python Kociemba (embedded, no pip)
from solver.kociemba_python.search import solve as kociemba_solve

logger = logging.getLogger("pure_kociemba")


def solve_cube(facelet_string: str) -> str:
    """
    Solve cube from a 54-character facelet string
    using pure-Python Kociemba algorithm.
    Compatible with Python 3.13.
    """
    logger.info(f"Solving cube for facelets: {facelet_string}")

    cube = Cube(facelet_string)
    validate_cube(cube)

    solution = kociemba_solve(facelet_string)
    logger.info(f"Solution: {solution}")
    return solution


# 🔥 REQUIRED by rubik_solver_wrapper.py
def solve(facelet_string: str) -> str:
    return solve_cube(facelet_string)


def color_to_face_letter(color: str) -> str:
    COLOR_TO_FACE = {
        "white": "U",
        "red": "R",
        "green": "F",
        "yellow": "D",
        "orange": "L",
        "blue": "B",
    }

    if color not in COLOR_TO_FACE:
        raise RuntimeError(f"Unknown color detected: {color}")

    return COLOR_TO_FACE[color]
