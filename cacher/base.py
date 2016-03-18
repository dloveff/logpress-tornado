#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'dong'

from memcached_holder import mc


class BaseMc(object):

    @classmethod
    def set(cls, key, *args, **kwargs):
        '''
        set
        :param key:
        :param kwargs:
        :return:
        '''

        ttl = kwargs.pop('ttl', 0)
        l = []
        for i in args:
            l.append(str(i))

        value = ':'.join(l)

        if ttl:
            mc.set(key, value, ttl)
        else:
            mc.set(key, value)