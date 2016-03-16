#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'dong'

from peewee import *
from models import *
from playhouse.shortcuts import model_to_dict, dict_to_model
import json
from helpers import utils

class BaseModel(Model):
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
        try:
            doc = Post.get(id=1, slug='slug')
            # doc = Post.select().where(Post.slug == 'slug').get()
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
        json_data = utils.json_dumps(model_to_dict(doc))
        return json_data