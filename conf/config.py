# -*- coding: utf-8 -*-
import os
HOME = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'bin')
rtenv = 'product'
LOGFILE = {
    'root': {
        'filename': {
            'DEBUG': os.path.join(HOME, '../log/channel_op_debug.log'),
            'WARN': os.path.join(HOME, '../log/channel_op_warn.log'),
        }
    }
}

# 数据库配置
database = {
    'uyu_core': {
        'token': 'server_core_uyu',
        'conn': 10,
        'engine': 'pymysql'
    },
}

# web config
# URLS配置
URLS = None
# 静态路径配置
STATICS = {'/static/':'/static/'}
# 模板配置
TEMPLATE = {
    'cache': True,
    'path': '',
    'tmp': os.path.join(HOME, '../tmp'),
}
# 中间件
MIDDLEWARE = ()
# WEB根路径
DOCUMENT_ROOT = HOME
# 页面编码
CHARSET = 'UTF-8'
# APP就是一个子目录
APPS = ()
DATABASE = {}
# 调试模式: True/False
# 生产环境必须为False
DEBUG = True
# 模版路径
template = os.path.join(HOME, 'template')

# 服务地址
HOST = '0.0.0.0'
# 服务端口
PORT = 8084
