#coding:utf-8

import os, sys
import uuid, redis, json

from zbase.base import dbpool
from uyubase.base import response

import logging, datetime, time
log = logging.getLogger()


class USession:
    def __init__(self, g_rt, sk=None):
        self.sk = sk
        self.g_rt = g_rt
        #self.vlue = None
    
    def gen_skey(self):
        self.sk = str(uuid.uuid4())

    def set_session(self, value, sys_role):
        svalue = {}
        svalue["userid"] = value["userid"]
        svalue["user_type"] = sys_role

        client = redis.StrictRedis(connection_pool=self.g_rt.redis_pool)
        client.set(self.sk, json.dumps(svalue))
        client.expire(self.sk, 60*60*24*3)

    def get_session(self):
        client = redis.StrictRedis(connection_pool=self.g_rt.redis_pool)
        v = client.get(self.sk)
        return json.loads(v)

class SUser:
    def __init__(self, userid, session, sys_role):
        #session 检查， SESSION中的USERID和传上来的USERID是否一致
        self.sauth = False
        #标记系统是渠道系统或者渠道运营系统或者门店系统后台
        self.sys_role = sys_role 
        self.userid = userid
        self.udata = None
        self.pdata = None
        self.se = session
        
    
    #检查SESSION对应的USERID是否有权限获取用户数据
    def check_permission(self):
        #是否能获取SESSION
        v = self.se.get_session()
        if not v:
            return False
        log.debug("get session: %s", v)
        #session中的用户角色和系统是否一致
        user_type = v.get("user_type")
        if user_type != self.sys_role:
            return False

        if self.userid != v.get("userid"):
            return False

        self.sauth = True
        return True

        
    @dbpool.with_database('uyu_core')
    def load_user(self):
        sql = "select * from auth_user where userid=%d" % self.userid 
        ret = self.db.get(sql)
        self.udata = ret
    

    #load 渠道用户，门店用户的档案数据
    @dbpool.with_database("uyu_core")
    def load_profile(self):
        if not self.udata:
            return
        user_type = self.udata.get("user_type", -1)
        #门店和渠道才有profile信息
        if user_type != response.UYU_USER_ROLE_CHAN and user_type != response.UYU_USER_ROLE_STORE:
            return
        sql = "select * from profile where userid=%d" % self.userid
        self.pdata= self.db.get(sql)
        

def uyu_check_session(g_rt, sys_role):
    def f(func):
        def _(self, *args, **kwargs):
            sk = self.get_cookie("sessionid")
            log.debug("sk: %s", sk)
            self.session = USession(g_rt, sk)

            params = self.req.input()
            userid = params.get("userid", -1)
            self.user = SUser(userid, self.session, sys_role)
            self.user.check_permission()
                
            x = func(self, *args, **kwargs)
            #set cookie
            return x
        return _
    return f

def uyu_set_cookie(g_rt, sys_role):
    def f(func):
        def _(self, *args, **kwargs):
            x = func(self, *args, **kwargs) 
            #创建SESSION
            self.session = USession(g_rt)
            self.session.gen_skey()
            self.session.set_session(x, sys_role)

            self.set_cookie("sessionid", self.session.sk, domain='.uyu.com', expires=60*60*24*3, max_age=60*60*24*3, path='/')
            return x
        return _
    return f
