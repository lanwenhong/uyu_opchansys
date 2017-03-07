# coding=utf-8
from zbase.web import core
from zbase.web import template
from zbase.web.validator import with_validator_self, Field, T_REG, T_INT, T_STR

from uyubase.base.response import success, error, UAURET, UYU_USER_ROLE_SUPER, UYU_USER_STATE_OK

from zbase.base.dbpool import with_database

from uyubase.base.usession import uyu_set_cookie, USession

from runtime import g_rt

import logging, datetime, time

log = logging.getLogger()


class Login(core.Handler):
    def GET(self):
        self.write(template.render('login.html'))



class ChangePassHandler(core.Handler):

    _post_handler_fields = [ 
        Field('mobile', T_REG, False, match=r'^(1\d{10})$'),
        Field('vcode', T_REG, False, match=r'^([0-9]{4})$'),
        Field('password', T_STR, False),
    ]
    
    @with_database('uyu_core')
    @with_validator_self
    def _post_handler(self, *args):
        params = self.validator.data
        mobile = params['mobile']
        vcode = params['vcode']
        password = params["password"]
        
        now = int(time.time())
        sql = "select * from verify_code where mobile='%s' and stime<%d and etime>%d" % (mobile,now,now)
        dbret = self.db.get(sql)
        log.debug("get from db: %s", dbret)
        if not dbret:
            return error(UAURET.VCODEERR)
        elif vcode != dbret["code"]:
            return error(UAURET.VCODEERR)

        sql = "update auth_user set password='%s' where phone_num='%s'" % (password, mobile)
        self.db.execute(sql)
        return success({})

    def POST(self, *args):
        ret = self._post_handler(self, args)
        self.write(ret)


class LoginHandler(core.Handler):
    _post_handler_fields = [ 
        Field('mobile', T_REG, False, match=r'^(1\d{10})$'),
        Field('password', T_STR, False),
    ]

    @uyu_set_cookie(g_rt, UYU_USER_ROLE_SUPER)
    @with_database('uyu_core')
    @with_validator_self 
    def _post_handler(self, *args):
        params = self.validator.data
        mobile = params['mobile']
        password = params["password"]
        sql = "select * from auth_user where phone_num='%s' and password='%s'" % (mobile, password)
        dbret = self.db.get(sql)
        
        log.debug("db ret: %s", dbret)
        if not dbret:
            return error(UAURET.USERERR)
        elif dbret["password"] != password:
            return error(UAURET.PWDERR)
        state = dbret.get("state", -1)
        user_type = dbret.get("user_type", -1)
        if user_type != UYU_USER_ROLE_SUPER or state != UYU_USER_STATE_OK:
            return error(UAURET.ROLEERR)
        ret = {"userid": dbret["id"]}
        return ret
        #return success(ret) 

    def POST(self, *args):
        ret = self._post_handler(args)
        self.write(success(ret))


class SmsHandler(core.Handler):
    _post_handler_fields = [ 
        Field('mobile', T_REG, False, match=r'^(1\d{10})$'),
    ]

    _get_handler_fields = [ 
        Field('mobile', T_REG, False, match=r'^(1\d{10})$'),
        Field('vcode', T_REG, False, match=r'^([0-9]{4})$'),
    ]


    @with_database('uyu_core')
    @with_validator_self
    def _post_handler(self, *args):
        params = self.validator.data
        mobile = params['mobile']

        now = int(time.time())
        sql = "select * from verify_code where mobile='%s' and stime<%d and etime>%d" % (mobile,now, now)
        dbret = self.db.get(sql)

        ret = None
        if not dbret:
            vcode = "1234"
            sql = "insert into verify_code set mobile='%s', code='%s', stime=%d, etime=%d" % (mobile, vcode, int(time.time()), int(time.time()) + 60)
            dbret = self.db.execute(sql)
            ret = {"vcode": vcode}
        else:
            vcode = dbret["code"]
            ret = {"vcode": vcode}
        return success(ret)

    def POST(self, *args):
        ret = self._post_handler(args) 
        self.write(ret)

    def GET(self, *args):
        pass
