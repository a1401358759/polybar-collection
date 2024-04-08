#!/usr/bin/env bash

THEME="gruvbox"

killall polybar
while pgrep -u $UID -x polybar >/dev/null; do sleep 1; done

CONFIG_DIR=$(dirname $0)/themes/$THEME/config.ini

# Launch polybar
if type "xrandr"; then
	for m in $(xrandr --query | grep " connected" | cut -d" " -f1); do
		MONITOR=$m polybar -r -c $CONFIG_DIR main &
	done
else
	polybar -r -c $CONFIG_DIR main &
fi
