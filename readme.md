# i3 auto floating

Remember floating state of [i3wm](https://i3wm.org/) windows and automatically set it when a new window of the same app is created.

## Install

```sh
pip install i3_auto_floating
```

## Configure

In `~/.config/i3/config` replace your existing floating toggle and start the auto toggle watcher:

```
bindsym $mod+Shift+space exec --no-startup-id i3_toggle_floating

exec --no-startup-id i3_auto_floating &
```

## Build

```sh
pip instal build
python3 -m build
```

Then upload

```sh
twine upload dist/i3_auto_floating-X.Y.tar.gz
```
