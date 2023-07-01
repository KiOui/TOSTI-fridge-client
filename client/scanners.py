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
