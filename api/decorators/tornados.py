#!/usr/bin/env python
# -*- coding: utf-8 -*-


import time
import logging
import traceback

from tornado.escape import json_decode
from tornado import web
from tornado import gen
from tornado.concurrent import TracebackFuture
from helpers import utils


class TornadoRequestWrapper(object):
    def __call__(self, *args, **kwargs):
        return self.wrap_request(*args, **kwargs)

    def wrap_request(_self,
                     function=None,
                     query_fields=[],
                     body_fields=[],
                     need_token=True,
                     checkers=[],
                     cache_marker=None,
                     post_calls=[]):

        def actual_decorator(function=None,
                             query_fields=query_fields,
                             body_fields=body_fields,
                             need_token=need_token,
                             checkers=checkers,
                             cache_marker=cache_marker,
                             post_calls=post_calls):
            @web.asynchronous
            @gen.coroutine
            def new_func(client, *args, **kwargs):
                # 初始化
                yield _self.do_init(client)

                # 进入业务逻辑
                yield _self.set_query_args(client, query_fields)

                # 提取Body
                yield _self.set_body_args(client, body_fields)

                # 处理token
                yield _self.validate_token(client, need_token)

                # 执行检查
                yield _self.invoke_checkers(client, checkers, *args, **kwargs)

                # 处理缓存
                yield _self.invoke_cache_marker(client, cache_marker, *args, **kwargs)

                # 业务逻辑
                yield _self.invoke_service(client, function, *args, **kwargs)

                # 标记缓存
                yield _self.invoke_cache_marker(client, cache_marker, *args, **kwargs)

                # post call
                yield _self.invoke_post_calls(client, post_calls, *args, **kwargs)

                # 结束
                yield _self.do_finish(client)

            return new_func

        if function:
            return actual_decorator(function, query_fields, body_fields, need_token, checkers)

        return actual_decorator


    @gen.coroutine
    def do_init(self, client):
        client.ok = True
        client.result = {}
        client.set_header('Access-Control-Allow-Origin', '*')

    @gen.coroutine
    def validate_token(self, client, need_token):
        '''
        验证token。
        :param client:
        :param need_token:
        :return:
        '''
        pass
        # 这里是验证用户token
        # token = client.get_argument('t', None)
        # user_id = AccountCook.to_user_id(token)
        # if need_token:
        #     if not token:
        #         client.ok = False
        #         client.result = Result.token_needed()
        #     elif not user_id:
        #         client.ok = False
        #         client.result = Result.token_invalid()
        # client.user_id = user_id
        # client.token = token

    @gen.coroutine
    def set_query_args(self, client, query_fields):
        '''
        query参数设置。
        :param client:
                    增加属性：
                        query_args，指定的query参数
                        _query_args，所有query参数
        :param query_fields:
        :return:
        '''
        args = {}
        for field in query_fields:
            args[field] = client.get_query_argument(field, None)
        client.query = args
        client._query = client.request.query_arguments

    @gen.coroutine
    def set_body_args(self, client, body_fields):
        '''
        body参数设置。
        :param client:
                 增加属性：
                        body，指定的body参数
                        _body，所有body参数
        :param body_fields:
        :return:
        '''
        client.body = {}
        client._body = {}
        if not client.ok:
            return
        if client.request.method in ("POST", "PUT", "DELETE") and body_fields:
            try:
                json = json_decode(client.request.body)
                body = {}
                for f in body_fields:
                    body[f] = json.get(f)
                client.body = body
                client._body = json
            except Exception, e:
                msg = traceback.format_exc()
                logging.warn(msg)
                if not 'No JSON object' in e.message:
                    client.ok = False
                    client.result = Result.failed(e.message)

    @gen.coroutine
    def invoke_checkers(self, client, checkers, *args, **kwargs):
        '''
        checkers调用。
        :param client:
        :param need_token:
        :return:
        '''
        if not client.ok:
            return
        for checker in checkers:
            yield checker(client, *args, **kwargs)

    @gen.coroutine
    def invoke_cache_marker(self, client, cache_marker, *args, **kwargs):
        '''
        缓存调用。
        :param client:
        :param cache_marker:
        :param args:
        :param kwargs:
        :return:
        '''
        if not client.ok:
            return
        if cache_marker and cache_marker._for == 'get':
            yield cache_marker(client, *args, **kwargs)

    @gen.coroutine
    def invoke_service(self, client, function, *args, **kwargs):
        '''
        执行业务逻辑。
        :param client:
        :param function:
        :param args:
        :param kwargs:
        :return:
        '''
        if not client.ok:
            return
        try:
            result = function(client, *args, **kwargs)
            if isinstance(result, TracebackFuture):
                result = yield result
                client.result = Result.succeeded(result)
                client.ok = True
        except (AssertionError, Exception), e:
            print traceback.format_exc()
            msg = None
            if isinstance(e, (AssertionError)):
                msg = e.message
            elif isinstance(e, ()):
                msg = u'数据格式错误'
            msg = msg or u'系统繁忙，请稍候重试'
            client.ok = False
            client.result = Result.failed(msg)

    def send_result(self, client, result):
        '''
        返回结果。
        :param client:
        :param result:
        :return:
        '''
        client.set_header("Content-Type", "application/json; charset=UTF-8")
        client.write(utils.json_dumps(result, ensure_ascii=False))

    @gen.coroutine
    def invoke_post_calls(self, client, post_calls, *args, **kwargs):
        '''
        post call调用。
        :param post_calls:
        :param args:
        :param kwargs:
        :return:
        '''
        if not client.ok:
            return
        for post_call in post_calls:
            yield post_call(client, *args, **kwargs)

    @gen.coroutine
    def do_finish(self, client):
        self.send_result(client, client.result)
        if getattr(client, '_finish_callback', None):
            yield client._finish_callback()
            del client._finish_callback


class Result():
    '''
        返回结果。
        字段描述：
            status: 接口调用状态
               success：接口调用成功
               failed：接口调用失败
               waiting：接口调用等待，返回task_id
            result: 接口调用结果
               -1：客户端缓存有效
               0：正常
               1：失败
               2：token过期，需要重新登录
               3：数据已被删除
               4：权限设置原因拒绝请求
            msg: 接口操作提示，譬如：用户名已存在
            data: 业务数据
            ts: 系统返回当前结果的时间
    '''

    @classmethod
    def cache_valid(cls, msg=None):
        msg = msg or u'客户端缓存有效'
        return Result.init(msg, status='success', code=-1)

    @classmethod
    def token_needed(cls, msg=None):
        msg = msg or u'操作失败，请先登录！'
        return Result.init(msg, status='failed', code=2)

    @classmethod
    def token_invalid(cls, msg=None):
        msg = msg or u'无效token，请先登陆！'
        return Result.init(msg, status='failed', code=2)

    @classmethod
    def token_expired(cls, msg=None):
        msg = msg or u'token过期，需要重新登录！'
        return Result.init(msg, status='failed', code=2)

    @classmethod
    def data_deleted(cls, msg=None):
        msg = msg or u'数据已被删除！'
        return Result.init(msg, status='failed', code=3)

    @classmethod
    def access_denied(cls, msg=None):
        msg = msg or u'权限设置原因拒绝请求！'
        return Result.init(msg, status='failed', code=4)

    @classmethod
    def failed(cls, msg=None):
        msg = msg or u'请求处理失败，请重试！'
        return Result.init(msg, status='failed', code=1)

    @classmethod
    def succeeded(cls, data):
        return Result.init(data=data)

    @classmethod
    def waiting(cls, data, msg=None):
        msg = msg or u'请求正在处理中，请稍后！'
        return Result.init(msg, status='waiting', code=0, data=data)

    @classmethod
    def init(cls, msg='', data=None, status='success', code=0):
        result = {
            'msg': msg,
            'data': data or {},
            'code': code,
            'status': status,
            'ts': time.time(),
        }
        return result


wrap_request = TornadoRequestWrapper()
