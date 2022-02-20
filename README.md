# sg-replay-importer

Convenient tool to append new Skullgirls replay files to your existing ones 
without manually renaming them all.

Written in Python and compiled to exe using pyinstaller. Only Windows x64 is 
supported at the moment.

## How to use

1. Download the 
   [release exe](https://github.com/hugh-braico/sg-replay-importer/releases).
1. Put the release exe in your replays folder.
1. Drag and drop new replay files (or zips containing replay files) onto the 
   exe. The importer will rename them and then append them onto your existing
   replays.

**NOTE:** Don't put loose replay files in the replay folder before dragging them 
onto the importer. The importer will get confused and think that they are part 
of the existing replays. Zip files can be inside the replay folder if you want
though.

## How to package your own release to exe

```bash
pyinstaller --onefile -i bigband.ico import-replays.py
```