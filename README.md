# Skullgirls Replay Importer

Convenient tool to append new Skullgirls replay files to your existing ones 
without manually renaming them all. Only Windows is supported.

## How to use

1. Download the 
   [latest exe](https://github.com/hugh-braico/sg-replay-importer/releases/download/v0.3/import-replays.exe).
1. Put the release exe in your replays folder.
1. Drag and drop new replay files (or zips containing replay files) onto the 
   exe. The importer will rename them and then append them onto your existing
   replays.

**NOTE:** Don't put replay files or zips in the replay folder before dragging 
them onto the importer. The importer will get confused and think that they are
part of the existing replays. Drag them from a different location.

## What about MacOS/Linux? 

No idea how to do this drag-and-drop thing on Unix-based systems, sorry.

Pull requests welcome!

## Building your own exe from source

If you're not the type to trust a random exe that someone else built and could
potentially do anything, you can build your own from source by cloning this
repo and running these commands from the root directory.

You'll need python3 and pip.

```bash
pip install -U pyinstaller
pyinstaller --onefile -i bigband.ico import-replays.py
```

You'll find the built exe in the `dist/` directory.
