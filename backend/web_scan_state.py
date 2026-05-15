import yaml
from pathlib import Path
import os


class ScanState:
    """
    Stores scanned cube faces coming from the web frontend.
    """

    def __init__(self):
        self.reset()

        # Always resolve config relative to project root (rubix/)
        BASE_DIR = Path(__file__).resolve().parents[1]   # rubix/
        colors_path = BASE_DIR / "config" / "colors.yaml"

        with open(colors_path, "r") as f:
            self.colors_cfg = yaml.safe_load(f)

    def reset(self):
        self.faces = {
            "F": None,
            "R": None,
            "B": None,
            "L": None,
            "U": None,
            "D": None,
        }

    def set_face(self, face, colors):
        if face not in self.faces:
            raise ValueError(f"Invalid face '{face}'")

        if len(colors) != 9:
            raise ValueError("Each face must have exactly 9 colors")

        self.faces[face] = colors

    def is_complete(self):
        return all(self.faces[face] is not None for face in self.faces)

    def faces_scanned(self):
        return [face for face, data in self.faces.items() if data is not None]

    def get_faces(self):
        return self.faces
