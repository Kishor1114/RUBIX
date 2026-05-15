import cv2
import logging

logger = logging.getLogger("camera")


class Camera:
    """
    Simple webcam wrapper.
    Usage:
        cam = Camera(index=0, width=640, height=480)
        frame = cam.read()
        cam.release()

    or:

        with Camera(0) as cam:
            frame = cam.read()
    """

    def __init__(self, index=0, width=640, height=480):
        self.index = index
        self.width = width
        self.height = height
        self.cap = None

    def open(self):
        """Open the webcam."""
        self.cap = cv2.VideoCapture(self.index)
        if not self.cap.isOpened():
            raise RuntimeError(f"Failed to open camera at index {self.index}")

        # Set resolution if supported
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

        logger.info(f"Camera opened at index {self.index} ({self.width}x{self.height})")

    def read(self):
        """
        Read a frame from the camera.
        Returns the frame (ndarray), or raises error if failed.
        """
        if self.cap is None:
            raise RuntimeError("Camera is not opened. Call open() first.")

        ret, frame = self.cap.read()
        if not ret:
            raise RuntimeError("Failed to read frame from camera")

        return frame

    def release(self):
        """Release the camera and close windows."""
        if self.cap is not None:
            self.cap.release()
            self.cap = None
        cv2.destroyAllWindows()
        logger.info("Camera released and windows closed.")

    # Context manager support
    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.release()
