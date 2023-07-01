class Observer:
    """Observer class."""

    def observe(self, *args, **kwargs):
        """Listen method."""
        raise NotImplementedError("This method should be implemented by a subclass of Observer.")
