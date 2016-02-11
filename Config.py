# coding=utf-8
#!/usr/bin/env python

import os
import json

Config = None
with open("config.json", "rb") as config_file:
    Config = json.load(config_file)
