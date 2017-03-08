#coding:utf-8

import os, sys
import uuid, redis, json

from zbase.base import dbpool
from uyubase.base import response
from uyubase.base.response import UAURET
from uyubase.uyu import define

import logging, datetime, time
log = logging.getLogger()


class USession:
    def __init__(self, redis_pool, c_conf, sk=None):
        self.sk = sk
        self.redis_pool = redis_pool 
        self.c_conf = c_conf
    
    def gen_skey(self):
        self.sk = str(uuid.uuid4())

    def set_session(self, value, sys_role):
        svalue = {}
        svalue["userid"] = value["userid"]
        svalue["user_type"] = sys_role

        client = redis.StrictRedis(connection_pool=self.redis_pool)
        client.set(self.sk, json.dumps(svalue))
        client.expire(self.sk, self.c_conf["expires"])

    def get_session(self):
        client = redis.StrictRedis(connection_pool=self.redis_pool)
        v = client.get(self.sk)
        if not v:
            return None
        return json.loads(v)

    def expire_session(self):
        client = redis.StrictRedis(connection_pool=self.redis_pool)
        client.expire(self.sk, self.c_conf["expires"])

class SUser:
    def __init__(self, userid, session, sys_role):
        #session 检查， SESSION中的USERID和传上来的USERID是否一致
        self.sauth = False
        #标记系统是渠道系统或者渠道运营系统或者门店系统后台
        self.sys_role = sys_role 
        self.userid = int(userid)
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
        log.debug("cuserid: %d", self.userid)
        log.debug("suserid: %d", v["userid"])

        #session中的用户角色和系统是否一致
        user_type = v.get("user_type")
        plist = define.PERMISSION_CHECK.get(self.sys_role, None)  
        if not plist:
            return False
        
        log.debug("get plist: %s", plist)
        if user_type not in plist:
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
        

def uyu_check_session(redis_pool, cookie_conf, sys_role):
    def f(func):
        def _(self, *args, **kwargs):
            sk = self.get_cookie("sessionid")
            log.debug("sk: %s", sk)
            self.session = USession(redis_pool, cookie_conf, sk)

            params = self.req.input()
            userid = params.get("userid", -1)
            self.user = SUser(userid, self.session, sys_role)
            self.user.check_permission()
                
            x = func(self, *args, **kwargs)
            #set cookie
            self.session.expire_session()
            return x
        return _
    return f

def uyu_set_cookie(redis_pool, cookie_conf, user_role):
    def f(func):
        def _(self, *args, **kwargs):
            x = func(self, *args, **kwargs) 
            #创建SESSION
            self.session = USession(redis_pool, cookie_conf)
            self.session.gen_skey()

            v = json.loads(x)
            if v["respcd"] == UAURET.OK:
                self.session.set_session(v["data"], user_role)
                self.set_cookie("sessionid", self.session.sk, **cookie_conf)
            return x
        return _
    return f
