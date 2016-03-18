#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'dong'


try:
    import psyco
    psyco.full()
except:
    pass

import peewee
import datetime
from models.base import BaseModel
from helpers.utils import get_random_verify_code, get_random_token
from settings import config
from cacher.base import BaseMc
from cacher.memcached_holder import mc


class User(BaseModel):
    user_id = peewee.CharField(index=True, max_length=30)
    username = peewee.CharField()
    password = peewee.CharField()
    mobile = peewee.CharField(index=True, max_length=20)
    created_at = peewee.DateField(default=datetime.datetime.now)
    updated_at = peewee.DateField(default=datetime.datetime.now)

    class Meta:
        db_table = 'user'
        order_by = ('-updated_at',)


class UserCook():

    r_verification = r'd:verify:%s:signup'


    @classmethod
    def verification_init(cls, mobile, verify_code=None, type=None, user_id=None, expiration=None):
        '''
        注册初始化,初始化验证码
        :param mobile:
        :param verify_code:
        :param type:
        :param user_id:
        :param expiration:
        :return:
        '''
        verify_code = verify_code or get_random_verify_code()
        expiration = expiration or config.expiration.verify_code
        t = get_random_token()

        signup = {
            'mobile': mobile,
            'verify_code': verify_code,
            'verify_token': t,
            'user_id': user_id,
            'status': 0,
            'type': type,
            'expiration': expiration,
        }

        tsignup = (mobile, verify_code, t, user_id, 0, type, expiration)

        k = cls.r_verification % (t, )
        BaseMc.set(k, ttl=expiration, *tsignup)
        return signup


    @classmethod
    def verification_validate(cls, verify_token, verify_code):
        '''
        验证验证码
        :param verify_token:
        :param verify_code:
        :return:
        '''
        k = cls.r_verification % (verify_token, )
        result = mc.get(k)
        assert result, u'验证码已过期，请重新获取'

        mobile = str(result).split(':')[0]
        result_verify_code = str(result).split(':')[1]
        t = str(result).split(':')[2]
        user_id = str(result).split(':')[3]
        status = str(result).split(':')[4]
        type = str(result).split(':')[5]
        expiration = str(result).split(':')[6]

        assert int(status or 0) == 0, u'验证码不能重复验证'
        assert result_verify_code == verify_code, u'不合法的验证码，请重新获取'

        # 设置状态
        l = [mobile, verify_code, t, user_id, str(1), type, expiration]
        value = ':'.join(l)
        mc.set(k, value, int(expiration))

        result_doc = {
            'mobile': mobile,
            'verify_token': t,
            'user_id': user_id,
            'status': 1,
            'type': type,
            'expiration': expiration,
        }

        return result_doc