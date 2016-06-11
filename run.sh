#!/bin/sh
[ "$(whoami)" != "root" ] && x-terminal-emulator -e "sh -c 'echo This app requires root access to send ordes to the HID device \(keyboard\); sudo -- "$0" "$@"' "
./main.py --size=600x300
