#!/bin/bash

CURR_BRIGHT=$(cat /sys/class/backlight/intel_backlight/actual_brightness)

echo "Choose a brightness level (current level $CURR_BRIGHT)"
select brt in "100" "200" "300" "400" "500" 
do
    case $brt in
        100 ) newbrt=100; break;;
        200 ) newbrt=200; break;;
        300 ) newbrt=300; break;;
        400 ) newbrt=400; break;;
        500 ) newbrt=500; break;;
    esac


done

echo $newbrt > /sys/class/backlight/intel_backlight/brightness


