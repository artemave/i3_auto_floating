#!/usr/bin/env python3

import i3ipc
from i3_auto_floating.shared import load_state, save_state, key_for

def main():
    conn = i3ipc.Connection()

    focused = conn.get_tree().find_focused()

    focused.command('floating toggle')

    state = load_state()

    k = key_for(conn, focused)

    is_floating = (focused.floating in ("auto_off"))

    if is_floating:
        state[k] = True
    elif k in state:
        del state[k]

    save_state(state)

if __name__ == "__main__":
    main()
