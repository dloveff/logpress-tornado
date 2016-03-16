#!/usr/bin/env python
# coding=utf8
try:
    import psyco

    psyco.full()
except:
    pass
from tornado.web import url

from handlers import account, admin, blog
from handlers import ErrorHandler
from api import *


routes = []
routes.extend(blog.routes)
routes.extend(account.routes)
routes.extend(admin.routes)
routes.extend(api_urls)
routes.append((r"/(.*)", ErrorHandler))
