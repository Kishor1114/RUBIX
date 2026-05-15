"""
cube/model.py

Lightweight Rubik’s Cube facelet model (54 characters).
Useful for debugging and internal state visualization.
"""

import logging

logger = logging.getLogger("cube_model")

FACE_ORDER = ["U", "R", "F", "D", "L", "B"]


class Cube:
    """
    Represents a 3×3 cube by its 54 facelets in solver order:

        U (9), R (9), F (9), D (9), L (9), B (9)

    Example:
        cube = Cube("UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB")
    """

    def __init__(self, facelet_string: str):
        if len(facelet_string) != 54:
            raise ValueError("Cube must be initialized with 54-character facelet string.")

        self.facelets = facelet_string

    def __repr__(self):
        return f"<Cube: {self.facelets}>"

    # ---------- Face access helpers ----------

    def get_face(self, face: str):
        """
        Returns list of 9 characters for the specified face.
        Faces: U, R, F, D, L, B
        """
        if face not in FACE_ORDER:
            raise ValueError(f"Invalid face '{face}'")

        idx = FACE_ORDER.index(face)
        start = idx * 9
        return list(self.facelets[start:start + 9])

    # ---------- Pretty printing ----------

    def pretty_print(self):
        """
        Displays cube in a human-readable unfolded format:

                 UUU
                 UUU
                 UUU
            LLL  FFF  RRR  BBB
            LLL  FFF  RRR  BBB
            LLL  FFF  RRR  BBB
                 DDD
                 DDD
                 DDD
        """
        U = self.get_face("U")
        R = self.get_face("R")
        F = self.get_face("F")
        D = self.get_face("D")
        L = self.get_face("L")
        B = self.get_face("B")

        def row(face, r):
            return "".join(face[r * 3:(r + 1) * 3])

        print("\n=== Cube State ===\n")

        # U face
        for r in range(3):
            print(" " * 6 + row(U, r))

        # L F R B row
        for r in range(3):
            print(row(L, r) + "   " + row(F, r) + "   " + row(R, r) + "   " + row(B, r))

        # D face
        for r in range(3):
            print(" " * 6 + row(D, r))

        print("\n===================\n")

    # ---------- Utility ----------

    def as_string(self):
        """Return the raw 54-character facelet string."""
        return self.facelets
