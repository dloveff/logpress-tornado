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
            'verify_token': 'd4a4e8bfa653438da63447324aeff7f7',
            'verify_code': '422283',
        }

        r = requests.post(url, json.dumps(data))
        return r.text


    @classmethod
    def signup_code(cls, url):
        '''
        注册
        :param url:
        :return:
        '''
        url = url + 'user/signup'

        data = {
            'verify_token': 'd4a4e8bfa653438da63447324aeff7f7',
            'password': '123456',
            'username': 'user_name',
        }

        r = requests.post(url, json.dumps(data))
        return r.text


    @classmethod
    def login(cls, url):
        '''

        :param url:
        :return:
        '''
        url = url + 'user/login'
        data = {
            'mobile': 123,
            'password': '123456',
        }

        r = requests.post(url, json.dumps(data))
        return r.text


    @classmethod
    def logout(cls, url):
        '''

        :param url:
        :return:
        '''
        url = url + 'user/logout'
        data = {
            'user_id': '5182068393d841cb9ef540960b3b9a8a',
            'token': 'cc027f6ec20a43f2943f15bdf3762dbc',
        }

        r = requests.post(url, json.dumps(data))
        return r.text


if __name__ == '__main__':

    url = 'http://127.0.0.1:9000/api/'

    # print blog.get_blog(url)

    # print User.get_verification(url)    # 获取验证码
    # print User.verify_code(url)    # 判断验证码有效性

    print User.signup_code(url)     # 注册

    print User.login(url)     # 登录
    print User.logout(url)      # 登出