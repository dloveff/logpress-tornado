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
from helpers.utils import get_random_verify_code, get_random_token, gen_digest
from settings import config
from cacher.base import BaseMc
from cacher.memcached_holder import mc


class User(BaseModel):
    user_id = peewee.CharField(index=True, max_length=30)
    username = peewee.CharField()
    password = peewee.CharField()
    salt = peewee.CharField()
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


    @classmethod
    def verification_info(cls, verify_token):
        '''
        验证码信息
        :param verify_token:
        :return:
        '''
        k = cls.r_verification % (verify_token, )
        result = mc.get(k)
        return result


    @classmethod
    def signup(self, mobile, **profile):
        '''
        用户注册
        :param mobile:
        :param password:
        :param user_alias:
        :param profile:
        :return:
        '''
        password = profile.get('password')
        username = profile.get('username')
        assert not User.find_one_by(User.mobile == mobile), u'号码已注册，请直接登录'
        assert password, u'密码不能为空'
        assert 6 <= len(password) <= 100, u'密码至少为6位'
        assert username, u'用户名不能为空'
        assert 2 <= len(username) <= 32, u'用户名长度必须在2 ~ 32'

        base = {
            'password': password,
            'salt': get_random_token()
        }

        password = gen_digest(base)


        user_id = self.get_user_id()

        User.create(user_id=user_id, username=username, password=password, salt=base.get('salt'), mobile=mobile)

        return User.find_one_by(User.user_id == user_id)


    @classmethod
    def get_user_id(cls):
        user_id = get_random_token()
        if User.select().where(User.user_id == user_id):
            cls.get_user_id()
        else:
            return user_id


    @classmethod
    def verification_destroy(cls, verify_token):
        '''
        注册完成
        :param verify_token:
        :return:
        '''
        k = cls.r_verification % (verify_token, )
        result = mc.get(k)
        mc.delete(k)
        return result


    @classmethod
    def login(cls, mobile, password):
        '''
        登陆
        :param mobile:
        :param password:
        :return:
        '''
        account = User.find_one_by(User.mobile == mobile)
        assert account, u'手机号码尚未注册'
        base = {
            'password': password,
            'salt': account.get('salt')
        }

        assert gen_digest(base) == account.get('password'), u'手机号码或密码错误'
        user_id = account.get('user_id')
        return cls.get_login_info_by_id(user_id)


    @classmethod
    def get_login_info_by_id(self, user_id, reset_token=False, account=None):
        '''
        获取登录信息
        :param user_id:
        :param reset_token:
        :param account:
        :return:
        '''
        result = BaseMc.login(user_id, reset_token)
        profile = User.find_one_by(User.user_id == user_id)
        result.update(profile)
        return result


    @classmethod
    def logout(cls, token, user_id):
        '''

        :param token:
        :param user_id:
        :return:
        '''
        return BaseMc.logout(token, user_id)