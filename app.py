from pathlib import Path
import json

from fastapi import FastAPI, Form
from fastapi.responses import FileResponse
from pydantic import BaseModel
from fastapi.responses import RedirectResponse

from datetime import datetime

from fastapi.templating import Jinja2Templates
from fastapi import Request

# Passing .astimezone() without arguments automatically applies your local system timezone

templates = Jinja2Templates(directory="templates")


app = FastAPI()

DATA_FILE = Path("habits.json")
HTML_FILE = Path("templates/tracker.html")


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
def home(request: Request):
    data = load_data()

    return templates.TemplateResponse(
        "tracker.html",
        {
            "request": request,
            "habits": data
        }
    )

@app.post("/api/habits")
def add_habit(
    name: str = Form(...),
    icon: str = Form(...),
    goal: str = Form(...),
    color: str = Form(...)
):


    current_local_iso = datetime.now().astimezone().isoformat()

    info = {
        f"{icon} {name}": {
            "created": current_local_iso,
            "completions": [
            ]
        }
    }

        # 1. Open the old file, or start with an empty DICTIONARY if it doesn't exist
    try:
        with open("habits.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}  # Changed from [] to {}

    # 2. Merge the new data into the existing dictionary
    data.update(info)

    # 3. Save everything back
    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)


    print(name, icon, goal, color)

    return {"success": True}