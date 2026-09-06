from pathlib import Path
import json

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from fastapi.responses import RedirectResponse


app = FastAPI()

DATA_FILE = Path("habits.json")
HTML_FILE = Path("tracker.html")


class Completion(BaseModel):
    datetime: str


def load_data() -> dict:
    if not DATA_FILE.exists():
        return {}

    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_data(data: dict):
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


@app.get("/api/completions")
def get_completions():
    return load_data()


@app.post("/api/completions/{habit}")
def toggle_completion(habit: str, completion: Completion):
    data = load_data()

    if habit not in data:
        data[habit] = []

    # The frontend sends something like:
    # 2026-09-05T12:00:00
    date = completion.datetime[:10]

    # Look for an existing completion on this date
    existing = None

    for value in data[habit]:
        if value[:10] == date:
            existing = value
            break

    if existing:
        # Already completed → remove it
        data[habit].remove(existing)
        completed = False
    else:
        # Not completed → add it
        data[habit].append(completion.datetime)
        completed = True

    save_data(data)

    return {
        "success": True,
        "habit": habit,
        "date": date,
        "completed": completed
    }


@app.get("/")
def home():
    return FileResponse(HTML_FILE)