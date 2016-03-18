#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'dong'

try:
    import psyco

    psyco.full()
except:
    pass


import tornado.gen
from base import BaseHandler
from decorators import tornados
from models.user.user import User


class VerificationHandler(BaseHandler):

    @tornados.wrap_request(need_token=False, body_fields=['mobile', 'type'])
    @tornado.gen.coroutine
    def post(self):

        assert self.body.get('mobile'), u'手机号码错误'

        verify_type = int(self.body['type'] or 0)

        mobile = self.body.get('mobile')

        accout = User.find_one_by(User.mobile == mobile)

        if verify_type == 0:
            assert not accout, u'号码已注册，请直接登陆'



class UserHandler():

    @tornados.wrap_request(need_token=False, body_fields=['mobile'])
    @tornado.gen.coroutine
    def post(self):
        '''
        创建用户
        :return:
        '''