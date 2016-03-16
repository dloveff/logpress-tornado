#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'dong'

try:
    import psyco

    psyco.full()
except:
    pass

from handlers import BaseHandler
from models import Post
from base import BaseModel as m
from helpers.utils import json_dumps


class BlogHandler(BaseHandler):
    def get(self):

        criteria = {
            'id': 1,
        }
        doc = m.find_by(criteria=criteria, fields=Post.public_fields)

        self.write(doc)
