#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'dong'

import os
from helpers import tools

path = os.path.join(os.path.dirname(__file__), 'config/config.toml')
config = tools.load_config(path)
