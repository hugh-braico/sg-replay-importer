# Skullgirls Replay Importer

Convenient tool to append new Skullgirls replay files to your existing ones 
in bulk without manually renaming them all.

Only Windows is supported.

## How to use

1. Download the 
   [latest exe](https://github.com/hugh-braico/sg-replay-importer/releases/download/v0.4/import-replays.exe).
1. Put the exe in your replays folder (`Documents\Skullgirls\Replays_SG2EPlus\<steam_user_number>`).
1. Drag and drop new replay files (and/or zip files containing replay files) onto
   the exe. The importer will rename them and then append them onto your existing
   replays. You can drag lots of them at once if you want.

**NOTE:** Don't put replay files or zips in the replay folder before dragging 
them onto the importer. The importer will get confused and think that they are
part of the existing replays. Drag them from a different location.

Right now archive file formats other than zip (rar, 7z, tar, etc) are not 
supported. Pull requests welcome!

## What about MacOS/Linux? 

No idea how to do this drag-and-drop thing on Unix-based systems, sorry.

Pull requests welcome!

## Building your own exe from source

If you're not the type to trust a random exe that someone else built and could
potentially do anything, you can build your own from source by cloning this
repo and running these commands from the root directory. If you're going to do
this out of caution, it makes sense to also give `import-replays.py` a thorough
read to make sure you understand what it's doing.

You'll need python3 and pip.

```bash
pip install -U pyinstaller
pyinstaller --onefile -i bigband.ico import-replays.py
```

You'll find the built exe in the `dist/` directory.
