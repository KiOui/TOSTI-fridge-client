from lock import Lock
from observer import Observer


class FakeFridge(Observer):
    """
    Fake Fridge class.

    This class fakes a fridge class for testing on other computers than Raspberry Pi.
    """

    def __init__(self, gpio_pin):
        """Initialize Fridge class."""
        self.gpio_pin = gpio_pin

    def lock(self):
        """Lock a Fridge."""
        print("Locked")

    def unlock(self):
        """Unlock a fridge."""
        print("Unlocked")

    def observe(self, instance, *args, **kwargs):
        """Observe function."""
        if instance.state == Lock.STATE_LOCKED:
            self.lock()
        else:
            self.unlock()
