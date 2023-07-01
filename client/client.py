import logging
from threading import Lock as ThreadLock

from api.clientcredentials import TostiClientCredentialsAPIService
from exceptions import ImproperlyConfigured
from lock import Lock
import threading
from optparse import OptionParser

from settings.settings import Settings


logger = logging.getLogger()


class Main:
    """Main class."""

    def __init__(self, settings):
        """Initialize main class."""
        self.settings = settings
        self._currently_processing_records = list()
        self._lock = ThreadLock()
        self.scanner = self.settings.SCANNER_CLASS()

        if not hasattr(self.settings, "CLIENT_ID"):
            raise ImproperlyConfigured("CLIENT_ID setting should be specified in settings config.")

        if not hasattr(self.settings, "CLIENT_SECRET"):
            raise ImproperlyConfigured("CLIENT_SECRET setting should be specified in settings config.")

        if not hasattr(self.settings, "API_BASE_URL"):
            raise ImproperlyConfigured("API_BASE_URL setting should be specified in settings config.")

        self.tosti_client = TostiClientCredentialsAPIService(
            self.settings.API_BASE_URL, self.settings.CLIENT_ID, self.settings.CLIENT_SECRET
        )

        self.fridge_locks = dict()
        if self.settings.LOCK_CONFIGURATION:
            for lock_configuration in self.settings.LOCK_CONFIGURATION:
                lock_identifier = lock_configuration["slug"]
                lock_connected_gpio_pins = lock_configuration["connected_gpio_pins"]
                lock = Lock(lock_identifier)
                for gpio_pin in lock_connected_gpio_pins:
                    lock.register_observer(self.settings.FRIDGE_CLASS(gpio_pin))
                self.fridge_locks[lock_identifier] = lock

    def _process(self, to_process: str):
        """Process a non-duplicate entry from the scanner."""
        logger.debug("Processing {}".format(to_process))
        answer = self.tosti_client.post("/api/v1/fridges/unlock/", {"user_token": to_process})
        if answer.status_code == 200:
            data = answer.json()
            logger.debug("Received {} from the server.".format(data))
            for fridge_unlock_information in data["unlock"]:
                fridge_name = fridge_unlock_information["fridge"]
                if fridge_name in self.fridge_locks.keys():
                    unlock_for = float(fridge_unlock_information['unlock_for'])
                    logger.debug("Unlocking fridge {} for {} seconds".format(fridge_name, unlock_for))
                    self.fridge_locks[fridge_name].unlock_for(unlock_for)
        else:
            logger.debug("Server responded with status code {}".format(answer.status_code))

    def process_scanner_result(self, scanner_result):
        """Process a result from the scanner."""
        logging.debug("Scan result found: {}".format(scanner_result))
        with self._lock:
            if scanner_result in self._currently_processing_records:
                # Do not process a record that is currently being processed.
                logger.debug("Scanner result is already being processed, skipping.")
                return
            else:
                self._currently_processing_records.append(scanner_result)
        try:
            self._process(scanner_result)
        finally:
            with self._lock:
                self._currently_processing_records.remove(scanner_result)

    def run(self):
        """Run the main loop."""
        logger.debug("Startup complete, starting main loop.")
        try:
            while True:
                next_input = self.scanner.scan()
                if next_input:
                    process_thread = threading.Thread(
                        target=self.process_scanner_result,
                        args=(next_input,),
                    )
                    process_thread.start()
        except KeyboardInterrupt:
            pass


def parse_arguments():
    """Parse arguments from command line."""
    parser = OptionParser()
    parser.add_option(
        "--settings",
        dest="settings",
        help="The settings file to use.",
        default="settings",
    )
    parser.add_option(
        "--verbose",
        dest="verbose",
        action="store_true",
        help="Enable verbose logging.",
        default=False,
    )
    options, arguments = parser.parse_args()
    return options, arguments


def main(options, arguments):
    """Load settings and run the main thread."""
    settings = Settings(options.settings)
    if options.verbose:
        logging.basicConfig(level=logging.DEBUG)
    main_thread = Main(settings)
    main_thread.run()


if __name__ == "__main__":
    main(*parse_arguments())
