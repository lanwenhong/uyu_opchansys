#coding: utf-8

import os, sys
HOME = os.path.dirname(os.path.abspath(__file__))
#from zbase.base import loader

#loader.loadconf_argv(HOME)
import config
import redis

class Runtime:
    def __init__(self):
        self.redis_pool = redis.ConnectionPool.from_url(config.redis_url)

global g_rt
g_rt = Runtime()
