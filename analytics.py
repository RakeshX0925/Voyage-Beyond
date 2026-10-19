from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "planets.csv"

NUMERIC_COLUMNS = {
    "diameter_km": "Diameter (km)",
    "gravity_m_s2": "Gravity (m/s²)",
    "orbital_period_days": "Orbital period (days)",
    "mean_temperature_c": "Mean temperature (°C)",
    "distance_from_sun_million_km": "Distance from Sun (million km)",
}


def load_planets():
    """Load the curated local CSV and parse blank cells as missing values."""
    return pd.read_csv(DATA_PATH)


def get_analytics():
    """Calculate descriptive summaries using available numeric observations."""
    data = load_planets()
    summary = []
    for column, label in NUMERIC_COLUMNS.items():
        if column not in data.columns:
            continue
        values = pd.to_numeric(data[column], errors="coerce").dropna()
        if values.empty:
            continue
        summary.append({
            "key": column,
            "label": label,
            "count": int(values.count()),
            "minimum": round(float(values.min()), 3),
            "maximum": round(float(values.max()), 3),
            "mean": round(float(values.mean()), 3),
        })
    diameter_data = data[["name", "diameter_km"]].copy()
    diameter_data["diameter_km"] = pd.to_numeric(diameter_data["diameter_km"], errors="coerce")
    diameter_data = diameter_data.dropna().sort_values("diameter_km", ascending=False)
    return {
        "object_count": int(len(data)),
        "planet_count": int((data["category"] == "Planet").sum()),
        "summary": summary,
        "diameter_chart": diameter_data.to_dict(orient="records"),
    }
