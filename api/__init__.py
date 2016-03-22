#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'dong'

from blog_handler import *
from user_handler import *

api_urls = [
    (r'/api/blog/?', BlogHandler),

    # 用户
    (r'/api/user/verifiaction/?', VerificationHandler),     # 获取验证码
    (r'/api/user/verify_code/validate/?', VerificationValidateHandler),  # 判断验证码有效性

    (r'/api/user/signup/?', SignupHandler), #注册
    (r'/api/user/login/?', LoginHandler), #登录
    (r'/api/user/logout/?', LogoutHandler), #登出
]
