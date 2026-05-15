class CubieCube:
    """
    Cubie-level cube representation
    (minimal version sufficient for solving)
    """

    def __init__(self):
        pass

    @staticmethod
    def from_facelets(facelets: str):
        cube = CubieCube()
        cube.facelets = facelets
        return cube
