import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
HISTORY_FILE = PROJECT_ROOT / "data" / "history.json"


def load_history():
    try:
        with open(HISTORY_FILE, "r") as file:
            history = json.load(file)

    except FileNotFoundError:
        return []

    except json.JSONDecodeError:
        return []

    if not isinstance(history, list):
        return []

    return history


def save_result(result):
    history = load_history()

    history.append(result)

    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=4)


def get_service_history(service_name):
    history = load_history()

    return [
        item for item in history
        if item.get("service") == service_name and item.get("success")
    ]
