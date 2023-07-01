from lock import Lock
from observer import Observer


class Fridge(Observer):
    """
    Fridge class.

    This class takes care of the actual locking and unlocking of the electromagnetic lock.
    """

    def __init__(self, gpio_pin):
        """Initialize Fridge class."""
        self.gpio_pin = gpio_pin

    def lock(self):
        """Lock a Fridge."""
        # TODO: Implement this method.
        print("Locked")

    def unlock(self):
        """Unlock a fridge."""
        # TODO: Implement this method.
        print("Unlocked")

    def observe(self, instance, *args, **kwargs):
        """Observe function."""
        if instance.state == Lock.STATE_LOCKED:
            self.lock()
        else:
            self.unlock()
