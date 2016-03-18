#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'dong'

import pylibmc
from settings import config

mc = pylibmc.Client([config.memcached.host])
