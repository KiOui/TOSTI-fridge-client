"""
This is the configuration file for the TOSTI fridge client.
"""
from scanners import Console

SCANNER_CLASS = Console
CLIENT_SECRET = "wYQ8OJyEK85G7bN6DFuE5SekD8noHK0R3CoF6piVtX68Mv21vyQxhcmXtsJtR7y5dDgw7a0ldOLOcH4mYFC8ziyPVgQZjjoS" \
                "R8azEjcVO01TWpAfT3p3aC0uA9Z1qMUY"
CLIENT_ID = "SwdUUTX5vdtsh0HIQxpQ4oZJHYWxz6mNfLkwWUR9"
API_BASE_URL = "http://localhost:8000"

LOCK_CONFIGURATION = [
    {
        "slug": "beerfridge",
        "connected_gpio_pins": [2],
    },
]
