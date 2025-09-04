#!/usr/bin/env python3

import i3ipc
from sway_auto_floating.shared import load_state, key_for


def apply_remembered(conn, container, state):
    k = key_for(conn, container)

    if state.get(k):
        container.command('floating enable')


def main():
    conn = i3ipc.Connection()
    state = load_state()

    # Apply to existing windows at startup
    for container in conn.get_tree().leaves():
        apply_remembered(conn, container, state)

    def on_window(conn, e):
        state = load_state()
        container = e.container
        apply_remembered(conn, container, state)

    # container.name is empty on WINDOW_NEW, hence using WINDOW_TITLE
    conn.on(i3ipc.Event.WINDOW_TITLE, on_window)

    conn.main()


if __name__ == "__main__":
    main()
