#!/bin/bash

CURR_BRIGHT=$(cat /sys/class/backlight/intel_backlight/actual_brightness)

newbrt=$(zenity  --list  --text "Choose a brightness level (current level $CURR_BRIGHT)" --radiolist  --column "Select" --column "Brightness" 100 100 200 200 300 300 400 400 500 500 --width 300 --height 300)


echo $newbrt > /sys/class/backlight/intel_backlight/brightness


