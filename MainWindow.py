# coding=utf-8
#!/usr/bin/env python
import os
import json

import dbController

from gi.repository import Gtk
from Config import Config

def run():
    from MainWindowHandler import MainWindowHandler

    builder = Gtk.Builder()
    builder.add_from_file( Config["BUILDER_FILE"].format(os.path.sep, Config["STYLING_DIRECTORY"]))

    builder.connect_signals(MainWindowHandler(builder))
    builder.get_object("main_window").show_all()

    dbController.init_preview_db()
    Gtk.main()
