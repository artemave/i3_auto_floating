# i3 auto floating

Remember floating state of [i3wm](https://i3wm.org/) and [Sway](https://swaywm.org/) windows and automatically set it when a new window of the same app is created.

## Description

One can set certain apps to start in floating mode in i3/Sway config, but that's a bit too manual. Wouldn't it be nice if your window manager just remembered your choice when you turn on floating and then apply it next time you start the same app? Well, i3/Sway can't do that natively, but this tool can.

Works with both X11 (i3wm) and Wayland (Sway) environments, automatically detecting Wayland-native apps via `app_id` and X11 apps via window class/instance.

## Install

```sh
pip install i3_auto_floating
```

## Configure

### For i3wm
In `~/.config/i3/config` replace your existing floating toggle and start the auto toggle watcher:

```
bindsym $mod+Shift+space exec --no-startup-id i3_toggle_floating

exec --no-startup-id i3_auto_floating &
```

### For Sway
In `~/.config/sway/config` replace your existing floating toggle and start the auto toggle watcher:

```
bindsym $mod+Shift+space exec i3_toggle_floating

exec i3_auto_floating &
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
twine upload dist/i3_auto_floating-X.Y.tar.gz
```
