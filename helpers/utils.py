#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'dong'

import json
import datetime


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