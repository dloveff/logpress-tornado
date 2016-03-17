#!/usr/bin/env python
# -*- coding: utf-8 -*-


import tomlpython as toml



def load_config(config):
    """
        读取toml配置文件，并讲dict转换为object，简化访问方式。
    """
    with open(config) as data:
        return Dict2Object(toml.parse(data))


class Dict2Object(dict):

    """
    将Dict转换为Object，简化Dict的访问方式。

    reference:
        http://stackoverflow.com/questions/1305532/convert-python-dict-to-object
        """

    def __init__(self, data=None):
        super(Dict2Object, self).__init__()
        if data:
            self.__update(data, {})

    def __update(self, data, did):
        dataid = id(data)
        did[dataid] = self

        for k in data:
            dkid = id(data[k])
            if did.has_key(dkid):
                self[k] = did[dkid]
            elif isinstance(data[k], Dict2Object):
                self[k] = data[k]
            elif isinstance(data[k], dict):
                obj = Dict2Object()
                obj.__update(data[k], did)
                self[k] = obj
                obj = None
            else:
                self[k] = data[k]

    def __getattr__(self, key):
        return self.get(key, None)

    def __setattr__(self, key, value):
        if isinstance(value, dict):
            self[key] = Dict2Object(value)
        else:
            self[key] = value

    def update(self, *args):
        for obj in args:
            for k in obj:
                if isinstance(obj[k], dict):
                    self[k] = Dict2Object(obj[k])
                else:
                    self[k] = obj[k]
                    return self

    def merge(self, *args):
        for obj in args:
            for k in obj:
                if self.has_key(k):
                    if isinstance(self[k], list) and isinstance(obj[k], list):
                        self[k] += obj[k]
                    elif isinstance(self[k], list):
                        self[k].append(obj[k])
                    elif isinstance(obj[k], list):
                        self[k] = [self[k]] + obj[k]
                    elif isinstance(self[k], Dict2Object) and isinstance(obj[k], Dict2Object):
                        self[k].merge(obj[k])
                    elif isinstance(self[k], Dict2Object) and isinstance(obj[k], dict):
                        self[k].merge(obj[k])
                    else:
                        self[k] = [self[k], obj[k]]
                else:
                    if isinstance(obj[k], dict):
                        self[k] = Dict2Object(obj[k])
                    else:
                        self[k] = obj[k]
                        return self


config = load_config('config/config.toml')