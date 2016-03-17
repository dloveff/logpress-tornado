#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'dong'

from peewee import *
from playhouse.shortcuts import model_to_dict
from core import db


class BaseModel(db.Model):

    @classmethod
    def find_one_by(self, *query, **kwargs):
        '''
        查找
        :param kwargs:
        :return:
        '''
        try:
            doc = self.get(*query, **kwargs)
            return self.format(doc)
        except DoesNotExist:
            return ''

    @classmethod
    def format(cls, doc, **kwargs):
        '''
        格式化内容
        :param doc:
        :param kwargs:
        :return:
        '''
        json_data = model_to_dict(doc)
        return json_data