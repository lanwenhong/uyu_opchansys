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
from uyubase.uyu.define import UYU_SYS_ROLE_OP, UYU_OP_OK, UYU_OP_ERR, UYU_CHAN_MAP
from uyubase.base.uyu_user import UUser
from uyubase.uyu import define

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
        # Field('login_name', T_REG, False, match=r'^(1\d{10})$'),
        Field('channel_name',  T_STR, False),
        Field('phone_num', T_REG, False, match=r'^(1\d{10})$'),
        Field('email', T_STR, True, match=r'^[a-zA-Z0-9_\-\'\.]+@[a-zA-Z0-9_]+(\.[a-z]+){1,2}$'),
        Field('org_code',  T_STR, True),
        Field('license_id',  T_STR, True),
        Field('legal_person',  T_STR, True),
        Field('business',  T_STR, True),
        Field('front_business',  T_STR, True),
        Field('account_name',  T_STR, True),
        Field('bank_name',  T_STR, True),
        Field('bank_account',  T_STR, True),
        Field('contact_name',  T_STR, False),
        Field('contact_phone',  T_STR, False),
        Field('contact_email',  T_STR, True),
        Field('address',  T_STR, False),
        Field('training_amt_per', T_FLOAT, False),
        Field('divide_percent', T_FLOAT, True),
        Field('is_prepayment', T_INT, False),
    ]

    @uyu_check_session(g_rt.redis_pool, cookie_conf, UYU_SYS_ROLE_OP)
    @with_validator_self
    def _get_handler(self):
        if not self.user.sauth:
            return error(UAURET.SESSIONERR)
        params = self.validator.data
        uop = UUser()
        ret = uop.call("load_info_by_userid", params["userid"])
        if ret ==  UYU_OP_ERR:
            return error(UAURET.USERERR)

        data = {}
        data["profile"] = uop.pdata
        data["chn_data"] = uop.cdata

        log.debug("get data: %s", uop.udata)
        udata = {}
        #ret_filed = ["login_name", "nick_name", "phone_num", "user_type", "email", "sex", "state"]
        ret_filed = ["login_name", "phone_num", "user_type", "email", "sex", "state"]
        for key in ret_filed:
            udata[key] = uop.udata[key]
        udata["userid"] =uop.udata["id"]
        data["u_data"] = udata
        return success(data)

    def GET(self, *args):
        ret = self._get_handler()
        log.debug("ret: %s", ret)
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
        Field('channel_name', T_STR, True),
        Field('phone_num', T_STR, True),
        Field('is_prepayment', T_INT, True),
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
            channel_name = params.get('channel_name', None)
            phone_num = params.get('phone_num', None)
            is_prepayment = params.get('is_prepayment', None)
            log.debug('is_prepayment: %s', is_prepayment)

            start, end = tools.gen_ret_range(curr_page, max_page_num)
            info_data = self._query_handler(channel_name, phone_num, is_prepayment)

            data['info'] = self._trans_record(info_data[start:end])
            data['num'] = len(info_data)
            return success(data)
        except Exception as e:
            log.warn(e)
            log.warn(traceback.format_exc())
            return error(UAURET.DATAERR)

    @with_database('uyu_core')
    def _query_handler(self, channel_name=None, phone_num=None, is_prepayment=None):
        keep_fields = [
            'channel.id', 'channel.remain_times', 'channel.training_amt_per',
            'channel.divide_percent', 'channel.is_valid', 'channel.ctime',
            'channel.userid', 'auth_user.phone_num', 'channel.channel_name',
            'channel.is_prepayment',
        ]

        where = {'channel.channel_name': channel_name} if channel_name else {}

        if phone_num:
            where.update({'auth_user.phone_num': phone_num})

        if is_prepayment in (0, 1):
            where.update({'channel.is_prepayment': is_prepayment})

        other = ' order by ctime desc'
        log.debug('where: %s', where)

        ret = self.db.select_join(table1='channel', table2='auth_user', on={'channel.userid': 'auth_user.id'}, fields=keep_fields, where=where, other=other)

        return ret

    @with_database('uyu_core')
    def _trans_record(self, data):
        if not data:
            return []

        profile_fields = ['contact_name', 'contact_phone']
        for item in data:
            userid = item['userid']
            profile_ret = self.db.select_one(table='profile', fields=profile_fields, where={'userid': userid})
            item['contact_name'] = profile_ret.get('contact_name', '') if profile_ret else ''
            item['ctime'] = item['ctime'].strftime('%Y-%m-%d %H:%M:%S') if item['ctime'] else ''
            item['status'] = item['is_valid']
            item['is_valid'] = UYU_CHAN_MAP.get(item['is_valid'], '')
            item['training_amt_per'] = item['training_amt_per'] / 100.0 if item['training_amt_per'] else 0.00
            if item['is_prepayment'] == 0:
                item['divide_percent'] = '无'

        return data


    def GET(self):
        try:
            data = self._get_handler()
            return data
        except Exception as e:
            log.warn(e)
            log.warn(traceback.format_exc())
            return error(UAURET.SERVERERR)


class CreateChanHandler(core.Handler):
    _post_handler_fields = [
        Field('login_name', T_REG, False, match=r'^(1\d{10})$'),
        Field('phone_num', T_REG, False, match=r'^(1\d{10})$'),
        Field('email', T_STR, True, match=r'^[a-zA-Z0-9_\-\'\.]+@[a-zA-Z0-9_]+(\.[a-z]+){1,2}$'),
        Field('org_code',  T_STR, True),
        Field('license_id',  T_STR, True),
        Field('legal_person',  T_STR, True),
        Field('business',  T_STR, True),
        Field('front_business',  T_STR, True),
        Field('account_name',  T_STR, True),
        Field('bank_name',  T_STR, True),
        Field('bank_account',  T_STR, True),
        Field('contact_name',  T_STR, False),
        Field('contact_phone',  T_STR, False),
        Field('contact_email',  T_STR, True),
        Field('address',  T_STR, False),
        Field('training_amt_per', T_INT, False),
        Field('divide_percent', T_FLOAT, True),
        Field('is_prepayment', T_INT, True),
        Field('channel_name', T_STR, False),
    ]

    @uyu_check_session(g_rt.redis_pool, cookie_conf, UYU_SYS_ROLE_OP)
    @with_validator_self
    def _post_handler(self, *args):
        if not self.user.sauth:
            return error(UAURET.SESSIONERR)
        params = self.validator.data

        log.debug('params: %s', params)
        if params.get("is_prepayment") == define.UYU_CHAN_DIV_TYPE and not params.get("divide_percent", None):
            return error(UAURET.REGISTERERR)

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


class ChanNameList(core.Handler):

    @uyu_check_session(g_rt.redis_pool, cookie_conf, UYU_SYS_ROLE_OP)
    @with_database('uyu_core')
    def GET(self):
        sql = "select id, channel_name, training_amt_per, is_prepayment from channel where is_valid=0"
        db_ret = self.db.query(sql)

        ret_list = []
        for item in db_ret:
            tmp = {}
            tmp['channel_name'] = item.get('channel_name', '')
            tmp['channel_id'] = item.get('id', None)
            tmp['training_amt_per'] = item.get('training_amt_per', None)
            tmp['is_prepayment'] = item.get('is_prepayment', None)
            ret_list.append(tmp)

        self.write(success(ret_list))


class ChanStoreMap(core.Handler):

    _get_handler_fields = [
        Field('channel_id', T_INT, False),
    ]

    def _get_handler_errfunc(self, msg):
        return error(UAURET.PARAMERR, respmsg=msg)


    @with_validator_self
    def _get_handler(self, *args):
        try:
            params = self.validator.data
            channel_id = params.get('channel_id')
            data = self._query_handler(channel_id)
            return success(data)
        except Exception as e:
            log.warn(e)
            log.warn(traceback.format_exc())
            return error(UAURET.DATAERR)

    @with_database('uyu_core')
    def _query_handler(self, channel_id):
        ret = self.db.select(table='stores', fields=['id', 'store_name', 'training_amt_per'], where={'channel_id': channel_id, 'is_valid': 0})
        return ret

    @uyu_check_session(g_rt.redis_pool, cookie_conf, UYU_SYS_ROLE_OP)
    def GET(self):
        try:
            data = self._get_handler()
            return data
        except Exception as e:
            log.warn(e)
            log.warn(traceback.format_exc())
            return error(UAURET.SERVERERR)
