# IPDA — Petrol Price Analysis & Forecast Evaluation

FH Dortmund | IPDA Assignment 2

Analysis of German petrol prices (May–September 2026) across four stations: HEM, STAR, SHELL and ARAL.

## Project Structure

```text
IPDA/
├── notebooks
    IPDA_Assignment2_FINAL_Combined.ipynb
├──scripts
   script_download_data_api.py
   script_download_station.py
├── requirements.txt
├── .env.example
├── .gitignore
│
├── data/                    # Forecast CSV files
│   └── forecasts/
│       └── Petrolforecastscsv/
│
└── tankerkoenig-data/
    ├── prices/2026/         # Historical price CSVs
    └── stations/2026/       # Station metadata
```

## Setup

**1. Create and activate virtual environment**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**2. Install dependencies**

```bash
python -m pip install -r requirements.txt
```

**3. Configure credentials**

```bash
cp .env.example .env
```

Add your own Tankerkönig historical-data credentials to `.env`:

```env
TANKERKOENIG_DATA_USERNAME=
TANKERKOENIG_DATA_PASSWORD=
```

**4. Download historical data**

```bash
python script_download_data_api.py
python script_download_station.py
```

Historical period: **May 1 – September 30, 2026**.

**5. Prepare forecast data**

Extract the university-provided `Petrol forecasts csv.7z` into:

```text
data/forecasts/Petrolforecastscsv/
```

**6. Run notebook**

Open `IPDA_Assignment2_FINAL_Combined.ipynb` in VS Code, select the `.venv` Python kernel, and click **Run All**.

## Analysis

- Daily, weekly and monthly price patterns
- Hourly price heatmaps and noon price increases
- Actual vs forecast comparison
- MAE, RMSE and forecast bias
- Forecast horizon and baseline comparison
- Optional holiday analysis

## Data Sources

- Historical prices: [Tankerkönig](https://creativecommons.tankerkoenig.de/)
- Forecast data: Provided by FH Dortmund

**Note:** Raw datasets, API credentials and `.env` files are excluded from GitHub. Each team member must obtain authorized access independently.
