# sway auto floating

Remember floating state of [Sway](https://swaywm.org/) windows and automatically set it when a new window of the same app is created.

## Description

One can set certain apps to start in floating mode in Sway config, but that's a bit too manual. Wouldn't it be nice if your window manager just remembered your choice when you turn on floating and then apply it next time you start the same app? Well, Sway can't do that natively, but this tool can.

## Install

```sh
pip install sway_auto_floating
```

## Configure

In `~/.config/sway/config` replace your existing floating toggle and start the auto toggle watcher:

```
bindsym $mod+Shift+space exec sway_toggle_floating

exec sway_auto_floating &
```

## Run local version

```sh
pip install -e .
```

## Build

```sh
pip install build twine
python3 -m build
```

Then upload

```sh
twine upload dist/sway_auto_floating-X.Y.tar.gz
```
