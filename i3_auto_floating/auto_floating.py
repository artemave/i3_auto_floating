#!/usr/bin/env python3

from i3ipc import Connection
from i3ipc import Event
from i3_auto_floating.shared import cacheKey, cacheFilePath


def on_window_new(_, e):
    key = cacheKey(e.container)

    with open(cacheFilePath, 'r') as f:
        if key in f.read():
            e.container.command('floating enable')


def main():
    i3 = Connection()
    i3.on(Event.WINDOW_NEW, on_window_new)

    i3.main()
