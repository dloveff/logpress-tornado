#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'dong'

from memcached_holder import mc
from helpers.utils import get_random_token


class BaseMc(object):

    r_user_token = r'd:user:%s:token'
    r_token_user = r'd:token:%s:user'

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


    @classmethod
    def login(cls, user_id, reset_token=False):
        '''
        初始化登录token
            1. 若登录token存在，则直接返回
            2. 不存在，则生成新token
        :param user_id:
        :param reset_token:
        :return:
        '''
        result = {
            'user_id': user_id,
            'token': None,
        }

        k = cls.r_user_token % (user_id, )
        t = mc.get(k)
        if not reset_token and t:
            # e = mc.get(k)
            pass
        else:
            k = cls.r_token_user % (t, )
            mc.delete(k)

            t = get_random_token()
            k = cls.r_token_user % (t,)
            mc.set(k ,user_id, 0)

            k = cls.r_user_token % (user_id, )
            mc.set(k, t, 0)

        result.update({
            'token': t,
        })

        return result


    @classmethod
    def logout(cls, token, user_id):
        '''

        :return:
        '''
        k = cls.r_user_token % (user_id, )
        mc.delete(k)

        k = cls.r_token_user % (token, )
        mc.delete(k)

        result = None
        return result