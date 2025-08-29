import json
from pathlib import Path

STATE_PATH = Path.home() / ".config/i3_auto_floating/floating-state.json"

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

def key_for(con):
    """Generate a unique key for a window container that works with both i3 and Sway."""
    # Wayland-native apps have app_id; Xwayland apps use class/instance.
    if hasattr(con, 'app_id') and con.app_id:
        return f"wayland::{con.app_id}"
    wc = getattr(con, "window_class", None)
    wi = getattr(con, "window_instance", None)
    if wc or wi:
        return f"x11::{wc or ''}::{wi or ''}"
    # Fallback to workspace+title (last resort; can be noisy)
    return f"other::{con.workspace().name if con.workspace() else ''}::{con.name or ''}"
