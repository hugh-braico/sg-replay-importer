# Skullgirls Replay Importer

Convenient tool to append new Skullgirls replay files to your existing ones 
without manually renaming them all.

Written in Python and compiled to exe using pyinstaller. Only Windows x64 is 
supported at the moment.

## How to use

1. Download the 
   [latest exe](https://github.com/hugh-braico/sg-replay-importer/releases/download/v0.3/import-replays.exe).
1. Put the release exe in your replays folder.
1. Drag and drop new replay files (or zips containing replay files) onto the 
   exe. The importer will rename them and then append them onto your existing
   replays.

**NOTE:** Don't put replay files or zips in the replay folder before dragging 
them onto the importer. The importer will get confused and think that they are
part of the existing replays.

## How to package your own release to exe

```bash
pyinstaller --onefile -i bigband.ico import-replays.py
```
