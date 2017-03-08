# -*- coding: utf-8 -*-
from zbase.web import core
from zbase.web import template
from uyubase.base.usession import uyu_check_session 
from uyubase.base.response import success, error, UAURET 
from uyubase.uyu.define import UYU_SYS_ROLE_OP, UYU_OP_OK, UYU_OP_ERR
from zbase.web.validator import with_validator_self, Field, T_REG, T_INT, T_STR, T_FLOAT
from uyubase.base.uyu_user import UUser


from runtime import g_rt
from config import cookie_conf
import logging

log = logging.getLogger()

class ChannelManage(core.Handler):
    def GET(self):
        self.write(template.render('channel.html'))

class CreateChanHandler(core.Handler):
    _post_handler_fields = [
        Field('login_name', T_REG, False, match=r'^(1\d{10})$'),
        Field('nick_name',  T_STR, False),
        Field('phone_num', T_REG, False, match=r'^(1\d{10})$'),
        Field('user_type', T_INT, False),
        Field('email', T_STR, False, match=r'^[a-zA-Z0-9_\-\'\.]+@[a-zA-Z0-9_]+(\.[a-z]+){1,2}$'),
        Field('org_code',  T_STR, False),
        Field('license_id',  T_STR, False),
        Field('legal_person',  T_STR, False),
        Field('business',  T_STR, False),
        Field('front_business',  T_STR, False),
        Field('account_name',  T_STR, False),
        Field('bank_name',  T_STR, False),
        Field('bank_account',  T_STR, False),
        Field('contact_name',  T_STR, False),
        Field('contact_phone',  T_STR, False),
        Field('contact_email',  T_STR, False),
        Field('address',  T_STR, False),
        Field('training_amt_per', T_INT, False),
        Field('divide_percent', T_FLOAT, False),
        Field('is_prepayment', T_INT, False),
    ]

    @uyu_check_session(g_rt.redis_pool, cookie_conf, UYU_SYS_ROLE_OP)
    @with_validator_self
    def _post_handler(self, *args):
        if not self.user.sauth:
            return error(UAURET.SESSIONERR)
        params = self.validator.data
        uop = UUser()

        udata = {}
        for key in uop.ukey:
            if params.get(key, None):
                udata[key] = params[key]

        pdata = {}
        for key in uop.pkey:
            if params.get(key, None):
                pdata[key] = params[key]

        chndata = {}
        for key in uop.chan_key:
            if params.get(key, None):
                chndata[key] = params[key]

        log.debug("udata: %s pdata: %s chandata: %s", udata, pdata, chndata)         
        ret = uop.create_chan_transaction(udata, pdata, chndata)
        if ret == UYU_OP_ERR:
            return error(UAURET.REGISTERERR)

        return success({"userid": uop.userid, "chnid": uop.chnid})

    def POST(self, *args):
        return self._post_handler()

