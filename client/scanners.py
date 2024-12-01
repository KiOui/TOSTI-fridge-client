import cv2
from pyzbar.pyzbar import decode


class Scanner:
    """Abstract scanner class."""

    def scan(self):
        """Scan for image."""
        raise NotImplementedError("This method should be implemented by a subclass of Scanner.")


class Console(Scanner):
    """Console input scanner."""

    def scan(self):
        """Scan from terminal."""
        return input("Provide new input: ")


class Camera(Scanner):
    """Camera input scanner."""

    def __init__(self, camera_id=0):
        """Initialize the camera stream."""
        self.cap = cv2.VideoCapture(camera_id)
        self.detector = cv2.QRCodeDetector()

    def scan(self):
        """Scan from a camera image."""
        _, img = self.cap.read()
        data = decode(img)
        if len(data) > 0:
            data = data[0]
            return data.data.decode("utf-8")
        return None

    def __del__(self):
        """Stop camera stream."""
        self.cap.release()
