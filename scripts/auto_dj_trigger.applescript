tell application "System Events"
	delay 5 -- Give Mixxx time to launch
	tell application "Mixxx" to activate
	delay 1
	key code 111 using {shift down}


end tell
