#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'dong'

import peewee
from models import *


class BaseModel():
    # 公共字段
    public_fields = []

    # 最少字段
    min_fields = []

    @classmethod
    def find_by(self, criteria, fields, **kwargs):
        '''
        查找
        :param kwargs:
        :return:
        '''
        print criteria
        print fields
        doc = Post.get(id=1, slug='slug')
        print doc.id
        print doc.slug
        return doc.id
