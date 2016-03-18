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
        print args
        ttl = kwargs.pop('ttl', 0)
        l = []
        tuple_len = len(args)
        for i in tuple_len:
            l.append(str(args[i]))

        print l
        # for k, v in kwargs.iteritems():
        #     l.append(str(v))

        value = ':'.join(l)

        # print value
        #
        # if ttl:
        #     mc.set(key, value, ttl)
        # else:
        #     mc.set(key, value)