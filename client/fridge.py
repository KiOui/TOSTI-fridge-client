from lock import Lock
from observer import Observer
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


class Fridge(Observer):
    """
    Fridge class.

    This class takes care of the actual locking and unlocking of the electromagnetic lock.
    """

    def __init__(self, gpio_pin, default_value=GPIO.LOW):
        """Initialize Fridge class."""
        self.gpio_pin = gpio_pin
        self.setup(default_value)

    def setup(self, default_value):
        """Set up GPIO pin."""
        GPIO.setup(self.gpio_pin, GPIO.OUT)
        GPIO.output(self.gpio_pin, default_value)

    def lock(self):
        """Lock a Fridge."""
        GPIO.output(self.gpio_pin, GPIO.HIGH)

    def unlock(self):
        """Unlock a fridge."""
        GPIO.output(self.gpio_pin, GPIO.LOW)

    def observe(self, instance, *args, **kwargs):
        """Observe function."""
        if instance.state == Lock.STATE_LOCKED:
            self.lock()
        else:
            self.unlock()

    def __del__(self):
        """Cleanup GPIO."""
        GPIO.cleanup()
