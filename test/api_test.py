#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'dong'

import requests
import json


class blog:

    @classmethod
    def get_blog(cls, url):
        '''
        获取blog内容
        :param url:
        :return:
        '''
        url = url + 'blog?&slug=slug0'
        r = requests.get(url)
        return r.text

        # url = url + 'blog'
        # data = {
        #     'slug': 123,
        # }
        #
        # r = requests.post(url, json.dumps(data))
        # return r.text


class User:

    @classmethod
    def get_verification(cls, url):
        '''
        获取验证码
        :param url:
        :return:
        '''
        url = url + 'user/verifiaction'

        data = {
            'mobile': 123,
            'type': 0,
        }

        r = requests.post(url, json.dumps(data))
        return r.text

    @classmethod
    def verify_code(cls, url):
        '''
        判断验证码有效性
        :param url:
        :return:
        '''
        url = url + 'user/verify_code/validate'

        data = {
            'verify_token': '2d080a2ccee748ada4e8f6d7f1c286dd',
            'verify_code': '573386',
        }

        r = requests.post(url, json.dumps(data))
        return r.text

if __name__ == '__main__':

    url = 'http://127.0.0.1:9000/api/'

    # print blog.get_blog(url)

    print User.get_verification(url)    # 获取验证码
    # print User.verify_code(url)    # 判断验证码有效性