import os
import requests
from pathlib import Path

# Existing .env credentials
from dotenv import load_dotenv
load_dotenv()

USERNAME = os.environ["TANKERKOENIG_DATA_USERNAME"]
PASSWORD = os.environ["TANKERKOENIG_DATA_PASSWORD"]

date = "2026-09-30"

url = (
    "https://data.tankerkoenig.de/"
    "tankerkoenig-organization/tankerkoenig-data/"
    f"raw/branch/master/stations/2026/09/{date}-stations.csv"
)

response = requests.get(
    url,
    auth=(USERNAME, PASSWORD),
    timeout=120
)

response.raise_for_status()

folder = Path("tankerkoenig-data/stations/2026/09")
folder.mkdir(parents=True, exist_ok=True)

filepath = folder / f"{date}-stations.csv"
filepath.write_bytes(response.content)

print("Stations downloaded successfully!")
print("File:", filepath)