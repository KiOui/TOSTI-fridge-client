from sched import scheduler
import time

from observer import Observer
from threading import RLock


class BaseLock:
    """Base Lock class."""

    STATE_LOCKED = "locked"
    STATE_UNLOCKED = "unlocked"

    def __init__(self, state=STATE_LOCKED):
        """Initialize method."""
        self._state = state
        self._observers = list()
        self._lock = RLock()

    @property
    def state(self):
        """Retrieve state."""
        return self._state

    def notify_observers(self):
        """Notify observers."""
        for observer in self._observers:
            observer.observe(self)

    @property
    def observers(self):
        """Get observers."""
        return self._observers

    def set_state(self, state):
        """Set the state of the lock."""
        if state != BaseLock.STATE_LOCKED and state != BaseLock.STATE_UNLOCKED:
            raise ValueError(
                "Parameter 'state' should have a value of {} or {}.".format(
                    BaseLock.STATE_LOCKED, BaseLock.STATE_UNLOCKED
                )
            )
        with self._lock:
            if state != self.state:
                if state == BaseLock.STATE_UNLOCKED:
                    self._state = BaseLock.STATE_UNLOCKED
                else:
                    self._state = BaseLock.STATE_LOCKED
                self.notify_observers()

    def register_observer(self, observer: Observer):
        """Register a change listener."""
        if observer not in self._observers:
            self._observers.append(observer)


class Lock(BaseLock):
    """Lock class."""

    def __init__(self, identifier, state=BaseLock.STATE_LOCKED):
        """Initialize a Lock."""
        super().__init__(state=state)
        self.unlock_until = time.time()
        self.identifier = identifier

    def _callback_lock(self):
        """Automatically lock the lock after x seconds (callback method)."""
        with self._lock:
            current_time = time.time()
            if self.unlock_until < current_time and self.state != BaseLock.STATE_LOCKED:
                self.set_state(BaseLock.STATE_LOCKED)

    def unlock_for(self, time_in_seconds):
        """Unlock a Lock until a certain moment in time."""
        with self._lock:
            self.unlock_until = time.time() + time_in_seconds - 1
            self.set_state(BaseLock.STATE_UNLOCKED)
        event_scheduler = scheduler()
        event_scheduler.enter(time_in_seconds, 1, self._callback_lock)
        event_scheduler.run()
