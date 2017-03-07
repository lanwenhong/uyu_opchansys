# coding=utf-8
from zbase.web import core
from zbase.web import template
from zbase.web.validator import with_validator_self, Field, T_REG, T_INT, T_STR

from uyubase.base.response import success, error, UAURET, UYU_USER_ROLE_SUPER, UYU_USER_STATE_OK

from zbase.base.dbpool import with_database

from uyubase.base.usession import uyu_set_cookie, USession
from uyubase.base.uyu_user import VCode, UUser

from runtime import g_rt
from config import cookie_conf

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
    
    @with_validator_self
    def _post_handler(self, *args):
        params = self.validator.data
        mobile = params['mobile']
        vcode = params['vcode']
        password = params["password"]
        
        u_op = UUser()
        respcd = u_op.change_password(mobile, vcode, password)
        if respcd != UAURET.OK:
            return error(respcd)
        return success({})
        
    def POST(self, *args):
        ret = self._post_handler(self, args)
        self.write(ret)


class LoginHandler(core.Handler):
    _post_handler_fields = [ 
        Field('mobile', T_REG, False, match=r'^(1\d{10})$'),
        Field('password', T_STR, False),
    ]

    @uyu_set_cookie(g_rt, cookie_conf, UYU_USER_ROLE_SUPER)
    @with_validator_self 
    def _post_handler(self, *args):
        params = self.validator.data
        mobile = params['mobile']
        password = params["password"]


        u_op = UUser()
        respcd, dbret = u_op.check_userlogin(mobile, password, UYU_USER_ROLE_SUPER)
        if respcd != UAURET.OK:
            return error(respcd)
        return success({"userid": dbret["id"]}) 
        #sql = "select * from auth_user where phone_num='%s' and password='%s'" % (mobile, password)
        #dbret = self.db.get(sql)
        #
        #log.debug("db ret: %s", dbret)
        #if not dbret:
        #    return error(UAURET.USERERR)
        #elif dbret["password"] != password:
        #    return error(UAURET.PWDERR)
        #state = dbret.get("state", -1)
        #user_type = dbret.get("user_type", -1)
        #if user_type != UYU_USER_ROLE_SUPER or state != UYU_USER_STATE_OK:
        #    return error(UAURET.ROLEERR)
        #ret = {"userid": dbret["id"]}
        #return ret

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

    @with_validator_self
    def _post_handler(self, *args):
        params = self.validator.data
        mobile = params['mobile']
        
        vop = VCode()
        vcode = vop.gen_vcode(mobile)

        log.debug("get vcode: %s", vcode)
        if not vcode:
            return error(UAURET.VCODEERR)

        return success({})

    def POST(self, *args):
        ret = self._post_handler(args) 
        self.write(ret)

    def GET(self, *args):
        pass
