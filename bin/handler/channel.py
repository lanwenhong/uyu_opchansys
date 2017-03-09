# -*- coding: utf-8 -*-
import traceback
from zbase.web import core
from zbase.web import template
from zbase.web.validator import with_validator_self, Field, T_REG, T_INT, T_STR, T_FLOAT
from zbase.base.dbpool import with_database

import logging, datetime, time
import tools
log = logging.getLogger()
from uyubase.base.usession import uyu_check_session, uyu_check_session_for_page
from uyubase.base.response import success, error, UAURET
from uyubase.uyu.define import UYU_SYS_ROLE_OP, UYU_OP_OK, UYU_OP_ERR
from uyubase.base.uyu_user import UUser

from runtime import g_rt
from config import cookie_conf
import logging

log = logging.getLogger()

class ChannelManage(core.Handler):
    @uyu_check_session_for_page(g_rt.redis_pool, cookie_conf, UYU_SYS_ROLE_OP)
    def GET(self):
        self.write(template.render('channel.html'))


class ChanStateSetHandler(core.Handler):
    _post_handler_fields = [
        Field('userid', T_INT, False),
        Field('state', T_INT, False),
    ]

    @uyu_check_session(g_rt.redis_pool, cookie_conf, UYU_SYS_ROLE_OP)
    @with_validator_self
    def _post_handler(self):
        if not self.user.sauth:
            return error(UAURET.SESSIONERR)
        uop = UUser()
        params = self.validator.data
        ret = uop.call("set_chan_state", params["userid"], params["state"])
        if ret == UYU_OP_ERR:
            return error(UAURET.REQERR)
        log.debug("set userid: %d state: %d succ", params["userid"], params["state"])
        return success({})

    def POST(self, *args):
        ret = self._post_handler()
        self.write(ret)

class ChanHandler(core.Handler):

    _get_handler_fields = [
        Field('userid', T_INT, False)
    ]

    _post_handler_fields = [
        Field("se_userid", T_INT, False),
        Field("userid", T_INT, False),
        Field('login_name', T_REG, False, match=r'^(1\d{10})$'),
        Field('channel_name',  T_STR, False),
        Field('phone_num', T_REG, False, match=r'^(1\d{10})$'),
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
    def _get_handler(self):
        if not self.user.sauth:
            return error(UAURET.SESSIONERR)
        params = self.validator.data
        uop = UUser()
        ret = uop.call("load_chan_by_userid", params["userid"])
        if ret ==  UYU_OP_ERR:
            return error(UAURET.USERERR)

        data = {}
        data["profile"] = uop.pdata
        data["chn_data"] = uop.cdata
        data["u_dasta"] = uop.udata
        return success(data)

    def GET(self, *args):
        ret = self._get_handler()
        self.write(ret)

    @uyu_check_session(g_rt.redis_pool, cookie_conf, UYU_SYS_ROLE_OP)
    @with_validator_self
    def _post_handler(self):
        if not self.user.sauth:
            return error(UAURET.SESSIONERR)
        uop = UUser()
        params = self.validator.data

        udata = {}
        for key in ["login_name", "nick_name", "phone_num"]:
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
        uop = UUser()
        ret = uop.call("chan_info_change", params["userid"], udata, pdata, chndata)
        if ret == UYU_OP_ERR:
            return error(UAURET.CHANGECHANERR)
        return success({"userid": params["userid"]})

    def POST(self, *args):
        ret = self._post_handler()
        self.write(ret)

class ChannelInfoHandler(core.Handler):

    _get_handler_fields = [
        Field('page', T_INT, False),
        Field('maxnum', T_INT, False),
        Field('nick_name', T_STR, True),
    ]

    def _get_handler_errfunc(self, msg):
        return error(UAURET.PARAMERR, respmsg=msg)

    @with_validator_self
    def _get_handler(self, *args):
        try:
            data = {}
            params = self.validator.data
            curr_page = params.get('page')
            max_page_num = params.get('maxnum')
            nick_name = params.get('nick_name')
            start, end = tools.gen_ret_range(curr_page, max_page_num)
            info_data = self._query_handler(nick_name=nick_name)
            data['info'] = info_data[start:end]
            data['num'] = len(info_data)
            return success(data)
        except Exception as e:
            log.warn(e)
            log.warn(traceback.format_exc())
            return error(UAURET.DATAERR)

    @with_database('uyu_core')
    def _query_handler(self, nick_name=None):
        profile_fields = ['contact_name', 'contact_phone']
        keep_fields = ['channel.id', 'channel.remain_times', 'channel.training_amt_per',
                       'channel.divide_percent', 'channel.is_valid', 'channel.ctime',
                       'channel.userid', 'auth_user.login_name', 'auth_user.nick_name',
                       ]
        where = {'auth_user.nick_name': nick_name} if nick_name else {}
        ret = self.db.select_join(table1='channel', table2='auth_user', on={'channel.userid': 'auth_user.id'}, fields=keep_fields, where=where)
        for item in ret:
            userid = item['userid']
            profile_ret = self.db.select_one(table='profile', fields=profile_fields, where={'userid': userid})
            item['contact_name'] = profile_ret.get('contact_name', '') if profile_ret else ''
            item['contact_phone'] = profile_ret.get('contact_phone', '') if profile_ret else ''
            item['ctime'] = item['ctime'].strftime('%Y-%m-%d %H:%M:%S') if item['ctime'] else ''

        return ret


    def GET(self):
        try:
            data = self._get_handler()
            return data
        except Exception as e:
            log.warn(e)
            log.warn(traceback.format_exc())
            return error(UAURET.SERVERERR)


#class ChannelHandler(core.Handler):
#    @uyu_check_session(g_rt.redis_pool, cookie_conf, UYU_SYS_ROLE_OP)
#    @with_validator_self
#    def _post_handler(self):
#        if not self.user.sauth:
#            return error(UAURET.SESSIONERR)
#        uop = UUser()
#        params = self.validator.data
#
#        udata = {}
#        for key in ["login_name", "nick_name", "phone_num"]:
#            if params.get(key, None):
#                udata[key] = params[key]
#
#        pdata = {}
#        for key in uop.pkey:
#            if params.get(key, None):
#                pdata[key] = params[key]
#
#        chndata = {}
#        for key in uop.chan_key:
#            if params.get(key, None):
#                chndata[key] = params[key]
#        log.debug("udata: %s pdata: %s chandata: %s", udata, pdata, chndata)
#        uop = UUser()
#        ret = uop.call("chan_info_change", params["userid"], udata, pdata, chndata)
#        if ret == UYU_OP_ERR:
#            return error(UAURET.CHANGECHANERR)
#        return success({"userid": params["userid"]})
#
#    def POST(self, *args):
#        ret = self._post_handler()
#        self.write(ret)

class CreateChanHandler(core.Handler):
    _post_handler_fields = [
        Field('login_name', T_REG, False, match=r'^(1\d{10})$'),
        #Field('nick_name',  T_STR, False),
        Field('phone_num', T_REG, False, match=r'^(1\d{10})$'),
        Field('email', T_STR, False, match=r'^[a-zA-Z0-9_\-\'\.]+@[a-zA-Z0-9_]+(\.[a-z]+){1,2}$'),
        Field('org_code',  T_STR, False),
        Field('license_id',  T_STR, False),
        Field('legal_person',  T_STR, False),
        # Field('business',  T_STR, False),
        # Field('front_business',  T_STR, False),
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
        Field('channel_name', T_STR, False),
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
        ret = uop.call("create_chan_transaction", udata, pdata, chndata)
        if ret == UYU_OP_ERR:
            return error(UAURET.REGISTERERR)

        return success({"userid": uop.userid, "chnid": uop.chnid})

    def POST(self, *args):
        return self._post_handler()
