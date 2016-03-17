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
from decorators import tornados as decoractor
import tornado.gen


class BlogHandler(BaseHandler):


    @decoractor.wrap_request(need_token=False)
    @tornado.gen.coroutine
    def get(self):
        doc = Post.find_one_by(Post.slug == self.slug)
        raise tornado.gen.Return(doc)


    @decoractor.wrap_request(need_token=False)
    @tornado.gen.coroutine
    def post(self):
        pass