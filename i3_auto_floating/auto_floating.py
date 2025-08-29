#!/usr/bin/env python3

import signal
import i3ipc
from i3_auto_floating.shared import load_state, save_state, key_for

def apply_remembered(conn, con, state):
    k = key_for(con)
    want = state.get(k)
    if want is None:
        return
    cmd = "floating enable" if want else "floating disable"
    try:
        con.command(cmd)
    except Exception:
        pass

def main():
    conn = i3ipc.Connection()
    state = load_state()

    # Apply to existing windows at startup
    for con in conn.get_tree().leaves():
        apply_remembered(conn, con, state)

    def on_window(conn, e):
        nonlocal state
        con = e.container
        if e.change in ("new",):  # new window -> apply
            apply_remembered(conn, con, state)
        elif e.change in ("floating",):  # user toggled floating -> remember
            k = key_for(con)
            is_floating = (con.floating in ("auto_on", "user_on"))
            state[k] = bool(is_floating)
            save_state(state)

    conn.on("window", on_window)

    # graceful exit
    for sig in (signal.SIGINT, signal.SIGTERM):
        signal.signal(sig, lambda *_: exit(0))

    conn.main()

if __name__ == "__main__":
    main()
