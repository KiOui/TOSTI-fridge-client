import serial
import logging


logger = logging.getLogger()


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


class SerialPort(Scanner):
    """Serial port scanner."""

    def __init__(self, port: str):
        """Initialize Serial port scanner."""
        self.serial = serial.Serial(port, 9600, timeout=1)

    def scan(self):
        """Scan from serial port."""
        if self.serial.in_waiting:
            code = self.serial.readline()

            try:
                code = code.decode("utf-8")
            except UnicodeDecodeError as e:
                logger.debug(f"An error occurred while decoding the serial input: {e}")
                return False

            code = code.strip()
            logger.debug("Scanned code {code}")
            return code

        return False
