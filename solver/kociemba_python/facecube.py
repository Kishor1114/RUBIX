class FaceCube:
    """
    Facelet representation of the cube
    """

    def __init__(self, facelets: str):
        self.facelets = facelets

    def to_cubie_cube(self):
        from .cubiecube import CubieCube
        return CubieCube.from_facelets(self.facelets)
