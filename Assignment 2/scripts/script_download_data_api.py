"""Download historical Tankerkoenig price CSV files for the assignment."""

from datetime import date, timedelta
import os
import time
from pathlib import Path

import requests


def load_dotenv(path):
    """Load simple NAME=value entries from the project's ignored .env file."""
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        name, value = line.split("=", 1)
        os.environ.setdefault(name.strip(), value.strip().strip("'\""))


load_dotenv(Path(__file__).with_name(".env"))

USERNAME = os.environ.get("TANKERKOENIG_DATA_USERNAME")
PASSWORD = os.environ.get("TANKERKOENIG_DATA_PASSWORD")
if not USERNAME or not PASSWORD:
    raise RuntimeError(
        "Add TANKERKOENIG_DATA_USERNAME and TANKERKOENIG_DATA_PASSWORD to .env"
    )

start_date = date(2026, 5, 1)
end_date = date(2026, 9, 30)

# Match IPDA_Assignment2.ipynb's TANKER_DIR/read_day folder structure.
output_dir = Path("tankerkoenig-data/prices")

current = start_date

while current <= end_date:
    filename = f"{current}-prices.csv"
    filepath = output_dir / f"{current:%Y}" / f"{current:%m}" / filename

    if filepath.exists():
        print(f"Already exists: {filename}")
        current += timedelta(days=1)
        continue

    url = (
        "https://data.tankerkoenig.de/"
        "tankerkoenig-organization/tankerkoenig-data/"
        f"raw/branch/master/prices/{current:%Y/%m}/"
        f"{filename}"
    )

    try:
        response = requests.get(
            url,
            auth=(USERNAME, PASSWORD),
            timeout=120
        )
        response.raise_for_status()

        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_bytes(response.content)
        print(f"Downloaded: {filename}")

    except requests.RequestException as e:
        print(f"Failed: {filename} — {e}")

    current += timedelta(days=1)
    time.sleep(0.3)

print("Download process finished!")
