# GPU Benchmark Tracker

This is a small Flask web app for tracking GPU benchmark results. It stores GPUs,
benchmark suites, and benchmark result entries in a SQLite database.

The app lets you:

- view benchmark results
- add, edit, and delete benchmark entries
- generate a filtered benchmark report by GPU, manufacturer, benchmark suite,
  resolution, and date range
- view summary stats like average score, average FPS, max temperature, and power
  draw

## How to run

From the project folder:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

## Reset/sample data

The project includes a seed script with sample GPUs, benchmark suites, and
benchmark results.

Run this if you want to recreate the database with the sample data:

```bash
python seed.py
```

Note: running `seed.py` resets the existing database tables.

## Tech used

- Python
- Flask
- Flask-SQLAlchemy
- SQLite
- Bootstrap templates
