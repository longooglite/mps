#!/bin/bash
#
# Script cargo.sh
# Launch CAR applications in assorted Terminal tabs.

function new_tab() {
  TAB_NAME=$1
  COMMAND=$2
  osascript \
    -e "tell application \"Terminal\"" \
    -e "tell application \"System Events\" to keystroke \"t\" using {command down}" \
    -e "do script \"printf '\\\e]1;$TAB_NAME\\\a'\" in front window" \
    -e "do script \"$COMMAND\" in front window" \
    -e "end tell" > /dev/null
}

set -v
new_tab "MPSLogin" "python $CAR_HOME/MPSLogin.py"
new_tab "MPSAuthSvc" "python $CAR_HOME/MPSAuthSvc.py"
new_tab "MPSAdmin" "python $CAR_HOME/MPSAdmin.py"
new_tab "MPSCV" "python $CAR_HOME/MPSCV.py"
new_tab "MPSAppt" "python $CAR_HOME/MPSAppt.py"
new_tab "Utility" "python $CAR_HOME/commands/skynyrd.py"
