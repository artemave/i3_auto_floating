import json
from pathlib import Path

STATE_PATH = Path.home() / ".config/sway_auto_floating/floating-state.json"


def load_state():
    try:
        return json.loads(STATE_PATH.read_text())
    except Exception:
        return {}


def save_state(state):
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    tmp = STATE_PATH.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, indent=2, sort_keys=True))
    tmp.replace(STATE_PATH)


def key_for(conn, container):
    base_key = f"wayland::{container.app_id}"

    # Check if another window with same app_id exists
    all_windows = conn.get_tree().leaves()

    for w in all_windows:
        # If it does, use more specific key
        if w.id != container.id and w.app_id == container.app_id:
            return f"{base_key}::{container.name[:50]}"

    return base_key
