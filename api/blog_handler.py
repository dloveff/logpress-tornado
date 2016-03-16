#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'dong'

try:
    import psyco

    psyco.full()
except:
    pass

from models import Post
from base import BaseHandler


class BlogHandler(BaseHandler):

    def get(self):
        # print self.slug
        # doc = Post.find_one_by(Post.slug == self.slug)
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        doc = Post.find_one_by(Post.slug == 'slug')
        self.write(doc)

    def post(self):
        slug = self.slug
        print slug