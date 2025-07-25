"""
This is the configuration file for the TOSTI fridge client.
"""
import os

from fridge import Fridge
from scanners import SerialPort

SCANNER_CLASS = SerialPort
SCANNER_INPUT_PARAMETERS = (os.getenv("TOSTI_SERIAL_DEVICE"),)
FRIDGE_CLASS = Fridge
CLIENT_SECRET = os.getenv("TOSTI_CLIENT_SECRET")
CLIENT_ID = os.getenv("TOSTI_CLIENT_ID")
API_BASE_URL = os.getenv("TOSTI_API_BASE_URL", "https://tosti.science.ru.nl")

LOCK_CONFIGURATION = [
    {
        "slug": "bierkoelkast-zuid",
        "connected_gpio_pins": [4],
    },
]
