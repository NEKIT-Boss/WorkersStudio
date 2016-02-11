# coding=utf-8
#!/usr/bin/env python
import json
CONFIG = {}
with open('config.json', 'r') as f:
    CONFIG = json.load(f)
import os
import dbController
from gi.repository import Gtk
from MainWindowHandler import MainWindowHandler

def run():        
    builder = Gtk.Builder()
    builder.add_from_file( CONFIG["BUILDER_FILE"].format(CONFIG["STYLING_DIRECTORY"], os.path.sep))

    builder.connect_signals(MainWindowHandler(builder))
    builder.get_object("main_window").show_all()

    Gtk.main()
