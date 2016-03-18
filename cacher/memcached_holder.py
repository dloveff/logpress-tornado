#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'dong'

import pylibmc
from manager import config

mc = pylibmc.Client([config.memcached.host])


mc.set('log', 'log test')
print mc.get('log')