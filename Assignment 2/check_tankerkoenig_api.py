"""Test a Tankerkoenig API key without placing it in source code.

The script reads TANKERKOENIG_API_KEY from the ignored .env file and performs
one nearby-station request. It is only a connectivity/key check; the API
returns current data and cannot download the historical CSV archive.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen


API_URL = "https://creativecommons.tankerkoenig.de/json/list.php"


def load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        name, value = line.split("=", 1)
        os.environ.setdefault(name.strip(), value.strip().strip("'\""))


def main() -> int:
    load_dotenv(Path(__file__).with_name(".env"))
    api_key = os.environ.get("TANKERKOENIG_API_KEY", "").strip()
    if not api_key:
        print("Missing TANKERKOENIG_API_KEY. Add it to .env; see .env.example.")
        return 2

    # Dortmund city centre, 25 km: enough to check access and see nearby data.
    query = urlencode(
        {
            "lat": 51.5136,
            "lng": 7.4653,
            "rad": 25,
            "type": "all",
            "apikey": api_key,
        }
    )
    try:
        with urlopen(f"{API_URL}?{query}", timeout=30) as response:
            payload = json.load(response)
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as error:
        print(f"API request failed: {error}")
        return 1

    if not payload.get("ok"):
        print("API rejected the request:", payload.get("message", "unknown error"))
        return 1

    stations = payload.get("stations", [])
    print(f"API key works. Received {len(stations)} stations near Dortmund.")

    wanted = ("am hartweg", "hebewerk", "lütgendortmunder", "luetgendortmunder")
    matches = [
        station
        for station in stations
        if any(term in str(station.get("street", "")).casefold() for term in wanted)
    ]
    if matches:
        print("Possible assignment stations returned by the live API:")
        for station in matches:
            print(
                f"- {station.get('id')} | {station.get('brand') or station.get('name')} | "
                f"{station.get('street')} {station.get('houseNumber', '')} | "
                f"{station.get('postCode')} {station.get('place')}"
            )
    else:
        print("The live nearby search did not return the assignment streets.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
