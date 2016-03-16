#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'dong'

import tornado.web
import tornado.gen
import tornado.ioloop

class BaseHandler(tornado.web.RequestHandler):

    @property
    def slug(self):
        '''
        id
        :return:
        '''
        slug = self.get_argument('slug', '')
        return slug