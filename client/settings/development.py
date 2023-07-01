"""
This is the configuration file for the TOSTI fridge client.

The development settings are configured in such a way that they don't make use of GPIO pins (because these are only
present on a Raspberry Pi). These settings can also be configured to run with a FakeFridge (that just outputs its
locked value when changed).
"""
from fakefridge import FakeFridge
from scanners import Console

SCANNER_CLASS = Console
FRIDGE_CLASS = FakeFridge
CLIENT_SECRET = (
    "wYQ8OJyEK85G7bN6DFuE5SekD8noHK0R3CoF6piVtX68Mv21vyQxhcmXtsJtR7y5dDgw7a0ldOLOcH4mYFC8ziyPVgQZjjoS"
    "R8azEjcVO01TWpAfT3p3aC0uA9Z1qMUY"
)
CLIENT_ID = "SwdUUTX5vdtsh0HIQxpQ4oZJHYWxz6mNfLkwWUR9"
API_BASE_URL = "http://localhost:8000"

LOCK_CONFIGURATION = [
    {
        "slug": "beerfridge",
        "connected_gpio_pins": [2],
    },
]
