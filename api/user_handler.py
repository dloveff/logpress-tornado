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
from decorators import tornados as decoractor
from models.user.user import User, UserCook


class VerificationHandler(BaseHandler):

    @decoractor.wrap_request(need_token=False, body_fields=['mobile', 'type'])
    @tornado.gen.coroutine
    def post(self):
        '''
        获取验证码
        :return:
        '''

        assert self.body.get('mobile'), u'手机号码错误'
        verify_type = int(self.body['type'] or 0)
        mobile = self.body.get('mobile')
        accout = User.find_one_by(User.mobile == mobile)

        if verify_type == 0:
            assert not accout, u'号码已注册，请直接登陆'

        # user_id = accout.get('user_id')
        user_id = None
        result = UserCook.verification_init(mobile, type=verify_type, user_id=user_id)

        # 这里要发送短信
        code = result.pop('verify_code', None)
        print '这个是验证码:', code

        raise tornado.gen.Return(result)



class VerificationValidateHandler(BaseHandler):

    @decoractor.wrap_request(need_token=False, body_fields=["verify_token", "verify_code"])
    @tornado.gen.coroutine
    def post(self):
        '''
        判断验证码有效性
        :return:
        '''
        result = UserCook.verification_validate(**self.body)
        raise tornado.gen.Return(result)


class UserHandler():

    @decoractor.wrap_request(need_token=False, body_fields=['mobile', 'type'])
    @tornado.gen.coroutine
    def post(self):
        '''
        创建用户
        :return:
        '''
        raise tornado.gen.Return()