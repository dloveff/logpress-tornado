#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'dong'

import json
import datetime
import random
from uuid import uuid4
from manager import config


def __default(obj):
    '''
    转换时间
    :param obj:
    :return:
    '''
    if isinstance(obj, datetime.datetime):
        return obj.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(obj, datetime.date):
        return obj.strftime('%Y-%m-%d')
    elif isinstance(obj, datetime.time):
        return '%s' % obj
    return str(obj)


def json_dumps(dict, **kwargs):
    '''
    转换json
    :param dict:
    :param kwargs:
    :return:
    '''
    kwargs['default'] = __default
    return json.dumps(dict, **kwargs)


def get_random_token():
    '''
    生成随机token
    :return:
    '''
    return uuid4().hex


def get_random_verify_code(source=None, size=None):
    '''
    生成随机验证码
    :param source:
    :param size:
    :return:
    '''
    source = source or config.verify_code.source
    size = size or config.verify_code.size
    return ''.join([random.choice(source) for _ in xrange(size)])
