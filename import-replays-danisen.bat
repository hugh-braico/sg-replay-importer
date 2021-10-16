Rem Helper batch script to launch the python script by dragging files onto this.
Rem Danisen mode is enabled on this one.

py -3 %~dp0import-replays.py --danisen --replayfolder %~dp0 --inputfiles %*