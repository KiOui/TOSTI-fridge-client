"""
This is the configuration file for the TOSTI fridge client.

The development settings are configured in such a way that they don't make use of GPIO pins (because these are only
present on a Raspberry Pi). These settings can also be configured to run with a FakeFridge (that just outputs its
locked value when changed).
"""
from fakefridge import FakeFridge
from scanners import Console

SCANNER_CLASS = Console
SCANNER_INPUT_PARAMETERS = ()
FRIDGE_CLASS = FakeFridge
CLIENT_SECRET = (
    "sEHsTqXuwdyukAKdAqaumX2cg3GH7yYNgCzNdjHLWkI4YjxKQu2un58Z5uTyESnJ8UZaiJZBeF5xiIlzygNLreWpKeGEPY4oN8aIJG4i97ZjAJJCRffGdGXChuuWnW7b"
)
CLIENT_ID = "YN5zU6MXkkqly7DqowO739c9DDZxENsNiaVIXvp4"
API_BASE_URL = "https://tosti.science.ru.nl"

LOCK_CONFIGURATION = [
    {
        "slug": "beerfridge",
        "connected_gpio_pins": [2],
    },
]
