# Voyage Beyond — Python Space Platform

This is the Python-powered enhancement of the existing Voyage Beyond website. The original HTML/CSS/JavaScript pages remain in the repository. The new Flask application is a separate implementation entry point, preserving the existing website.

## Features
- Search and filter a curated dataset of Solar System objects.
- Compare two objects using consistent properties and units.
- View Pandas descriptive summaries and a diameter ranking.
- Complete a five-question quiz and save attempts in SQLite.
- Explore a Jupyter Notebook for data quality checks and visualizations.

## Setup
Use Python 3.10 or newer.

    python -m venv .venv
    # Windows PowerShell:
    .venv\Scripts\Activate.ps1
    # macOS/Linux:
    source .venv/bin/activate
    pip install -r requirements.txt
    python app.py

Open the local address printed by Flask. Useful routes are /explorer, /compare, /analytics, /quiz, and /health.

## Tests
    pytest -q

## Notebook
Open notebooks/space_data_analysis.ipynb in Jupyter. Run it from the notebook directory so the relative path to data/planets.csv resolves.

## Data provenance and limitations
The included dataset is a starter transcription based on the planetary fact-sheet table supplied during project planning. Verify all values against the original source before final submission, cite the source and access date in the report, and review values that may change (especially moon counts). Blank values represent unavailable data. Some source tables use different definitions or units for distance, rotation, and temperature; keep the definitions in the data dictionary consistent. The Moon's distance fields refer to Earth, not the Sun, so exclude the Moon from planet-only solar-distance analysis. Pluto is a dwarf planet. The dataset is small and intended for descriptive analysis, not machine learning or broad statistical claims.

## Next improvements
- Add verified source links and citations to each record.
- Add form-level CSRF protection and move the development secret key into an environment variable before deployment.
- Add quiz explanations and randomized questions.
- Add tests for comparison calculations and missing-data cases.
- Add measured test results and screenshots to the final report.
