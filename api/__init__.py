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
]
