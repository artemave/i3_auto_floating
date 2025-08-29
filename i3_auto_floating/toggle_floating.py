#!/usr/bin/env python3

import i3ipc
from i3_auto_floating.shared import load_state, save_state, key_for

def main():
    # Connect to i3/Sway
    conn = i3ipc.Connection()

    # Get the focused window
    focused = conn.get_tree().find_focused()
    if not focused:
        return

    # Toggle floating
    focused.command('floating toggle')

    # Load current state
    state = load_state()

    # Update state based on new floating status
    # Note: we need to check the floating state after the toggle
    focused = conn.get_tree().find_focused()  # Refresh the window info
    if focused:
        k = key_for(focused)
        is_floating = (focused.floating in ("auto_on", "user_on"))
        state[k] = bool(is_floating)
        save_state(state)
