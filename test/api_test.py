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
        url = url + 'blog'
        # url = url + 'blog?&slug=slug9'
        # r = requests.get(url)
        # return r.text

        data = {
            'slug': 123,
        }

        r = requests.post(url, data)
        return r.text


if __name__ == '__main__':

    url = 'http://127.0.0.1:9000/api/'

    print blog.get_blog(url)