# coding=utf-8
from zbase.web import core
from zbase.web import template
from zbase.web.validator import with_validator_self, Field, T_REG, T_INT, T_STR

from uyubase.base.response import success, error, UAURET
from uyubase.uyu import define
from uyubase.uyu.define import UYU_SYS_ROLE_OP, UYU_USER_ROLE_SUPER,UYU_OP_ERR

from zbase.base.dbpool import with_database

from uyubase.base.usession import uyu_set_cookie, USession
from uyubase.base.uyu_user import VCode, UUser
from uyubase.base.send_sms import UYUSendSMS
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

    def _post_handler_errfunc(self, msg):
        return error(UAURET.PARAMERR, respmsg=msg)

    @with_validator_self
    def _post_handler(self, *args):
        params = self.validator.data
        mobile = params['mobile']
        vcode = params['vcode']
        password = params["password"]

        uop = UUser()
        uop.load_user_by_mobile(mobile)
        if len(uop.udata) == 0:
            log.debug('change pass handler mobile=%s not exists', mobile)
            return error(UAURET.USERERR)

        user_type = uop.udata.get('user_type')
        if user_type != define.UYU_USER_ROLE_SUPER:
            log.debug('change pass handler mobile=%s user_type=%s not super', mobile, user_type)
            return error(UAURET.ROLEERR)

        respcd = uop.change_password(mobile, vcode, password)
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

    def _post_handler_errfunc(self, msg):
        return error(UAURET.PARAMERR, respmsg=msg)

    @uyu_set_cookie(g_rt.redis_pool, cookie_conf, UYU_USER_ROLE_SUPER)
    @with_validator_self
    def _post_handler(self, *args):
        params = self.validator.data
        mobile = params['mobile']
        password = params["password"]

        u_op = UUser()
        ret = u_op.call("check_userlogin", mobile, password, UYU_SYS_ROLE_OP)
        if not u_op.login or ret == UYU_OP_ERR:
            log.warn("mobile: %s login forbidden", mobile)
            return error(UAURET.USERERR)

        log.debug("get user data: %s", u_op.udata)
        log.debug("userid: %d login succ", u_op.udata["id"])
        return success({"userid": u_op.udata["id"]})

    def POST(self, *args):
        ret = self._post_handler(args)
        return ret

class SmsHandler(core.Handler):
    _post_handler_fields = [
        Field('mobile', T_REG, False, match=r'^(1\d{10})$'),
    ]

    _get_handler_fields = [
        Field('mobile', T_REG, False, match=r'^(1\d{10})$'),
        Field('vcode', T_REG, False, match=r'^([0-9]{4})$'),
    ]

    def _post_handler_errfunc(self, msg):
        return error(UAURET.PARAMERR, respmsg=msg)

    def _get_handler_errfunc(self, msg):
        return error(UAURET.PARAMERR, respmsg=msg)

    @with_validator_self
    def _post_handler(self, *args):
        params = self.validator.data
        mobile = params['mobile']

        uop = UUser()
        uop.load_user_by_mobile(mobile)
        if len(uop.udata) == 0:
            log.debug('sms handler mobile=%s not exists', mobile)
            return error(UAURET.USERERR)

        user_type = uop.udata.get('user_type')
        if user_type != define.UYU_USER_ROLE_SUPER:
            log.debug('sms handler mobile=%s user_type=%s not super', mobile, user_type)
            return error(UAURET.ROLEERR)

        vop = VCode()
        vcode = vop.gen_vcode(mobile)
        log.debug("get vcode: %s", vcode)
        if not vcode:
            return error(UAURET.VCODEERR)
        sms_op = UYUSendSMS()
        ret = sms_op.send_sms(mobile, [vcode, 1], define.RONG_YUN_SMS_UYU_TEMPID_VERIFY_CODE)
        if not ret:
            log.debug('send_sms mobile=%s, vcode=%s except', mobile, vcode)
        else:
            status_code = ret.get('statusCode')
            if status_code == '000000':
                log.debug('send_sms mobile=%s, vcode=%s ok', mobile, vcode)
            else:
                log.debug('send_sms mobile=%s, vcode=%s fail', mobile, vcode)

        return success({})

    def POST(self, *args):
        ret = self._post_handler(args)
        self.write(ret)

    def GET(self, *args):
        pass

