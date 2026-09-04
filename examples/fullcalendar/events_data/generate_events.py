"""
Generate 1 year of sample events and save them to ``events_full.json``.

This script is independent from the web app.  Run it once (or whenever you
want to refresh the demo data) before starting ``main.py``:

    python generate_events.py

What it produces
----------------
A JSON file containing ~500-600 events spread across the current year
(January 1st to December 31st).
Each event has:
    - title   : randomly chosen from a list of common meeting names
    - start   : ISO datetime string (e.g. "2025-08-31T10:00:00")
    - end     : ISO datetime string
    - color   : one of several preset colors

Why this file?
--------------
The web app's ``fetch_events_from_python`` function loads this file and
returns only the events relevant to the calendar's currently visible date
range.  This keeps the UI fast even with hundreds of events in the dataset.
"""
import json
import random
from datetime import datetime, timedelta

# Fixed seed so the same sample data is generated every time.
# Change or remove the seed line if you want different data each run.
random.seed(42)

titles = [
    "Team meeting", "Project sync", "Design workshop",
    "Code review", "Sprint planning", "Client demo",
    "Internal training", "Maintenance", "Deployment",
    "Stand-up", "Retrospective", "Brainstorming",
]

events = []
now = datetime.now()
start_date = datetime(now.year, 1, 1, 0, 0, 0, 0)
end_date = datetime(now.year, 12, 31, 23, 59, 59, 0)

for day in range((end_date - start_date).days + 1):
    current = start_date + timedelta(days=day)
    n_events = random.randint(0, 3)
    for _ in range(n_events):
        hour = random.randint(8, 16)
        duration = random.choice([1, 2])
        events.append(
            {
                "title": random.choice(titles),
                "start": (current + timedelta(hours=hour)).isoformat(),
                "end": (current + timedelta(hours=hour + duration)).isoformat(),
                "color": random.choice(["blue", "green", "red", "orange", "purple", "teal"]),
            }
        )

with open("events_full.json", "w", encoding="utf-8") as f:
    json.dump(events, f, indent=2, ensure_ascii=False)

print(f"Generated {len(events)} events in {start_date.year} in events_full.json")
