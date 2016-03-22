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

        # 注册
        if verify_type == 0:
            assert not accout, u'号码已注册，请直接登陆'
        # 忘记密码
        elif verify_type == 1:
            assert accout, u'手机号暂未注册，请先注册'

        try:
            user_id = accout.get('user_id')
        except:
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


class SignupHandler(BaseHandler):

    @decoractor.wrap_request(need_token=False, body_fields=['verify_token', 'password', 'username'])
    @tornado.gen.coroutine
    def post(self):
        '''
        注册
        :return:
        '''

        assert self.body['password'], u'密码不能为空'
        assert 6 <= len(self.body['password']) <= 100, u'密码至少为6位'
        assert self.body['username'], u'用户名不能为空'
        assert 2 <= len(self.body['username']) <= 32, u'用户名长度必须在2 ~ 32'

        verify_token = self.body.pop('verify_token')
        result = UserCook.verification_info(verify_token)
        assert result, u'号码未通过验证，请先获取验证码'
        result = UserCook.signup(mobile=str(result).split(':')[0], **self.body)
        UserCook.verification_destroy(verify_token)
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


class LoginHandler(BaseHandler):

    @decoractor.wrap_request(need_token=False, body_fields=['mobile', 'password'])
    @tornado.gen.coroutine
    def post(self):
        '''
        登录
        :return:
        '''
        result = UserCook.login(**self.body)
        raise tornado.gen.Return(result)


class LogoutHandler(BaseHandler):

    @decoractor.wrap_request(need_token=True, body_fields=['user_id', 'token'])
    @tornado.gen.coroutine
    def post(self):
        '''
        登出
        :return:
        '''
        result = UserCook.logout(**self.body)
        raise tornado.gen.Return(result)