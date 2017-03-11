# -*- coding: utf-8 -*-
import traceback
from zbase.web import core
from zbase.web import template
from zbase.web.validator import with_validator_self, Field, T_REG, T_INT, T_STR, T_FLOAT
from zbase.base.dbpool import with_database
from uyubase.base.response import success, error, UAURET
from uyubase.base.usession import uyu_check_session, uyu_check_session_for_page
from uyubase.base.uyu_user import UUser


from uyubase.uyu.define import UYU_USER_ROLE_SUPER, UYU_USER_STATE_OK
from uyubase.uyu.define import UYU_SYS_ROLE_OP, UYU_OP_ERR, UYU_STORE_ROLE_MAP, UYU_STORE_STATUS_MAP

from runtime import g_rt
from config import cookie_conf
import logging, datetime, time
import tools
log = logging.getLogger()

class StoreManage(core.Handler):
    @uyu_check_session_for_page(g_rt.redis_pool, cookie_conf, UYU_SYS_ROLE_OP)
    def GET(self):
        self.write(template.render('store.html'))

class StoreStateSetHandler(core.Handler):
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
        ret = uop.call("set_store_state", params["userid"], params["state"])
        if ret == UYU_OP_ERR:
            return error(UAURET.REQERR)
        log.debug("set userid: %d state: %d succ", params["userid"], params["state"])
        return success({})

    def POST(self, *args):
        ret = self._post_handler()
        self.write(ret)

class StoreInfoHandler(core.Handler):


    _get_handler_fields = [
        Field('page', T_INT, False),
        Field('maxnum', T_INT, False),
        Field('channel_name', T_STR, True),
        Field('store_name', T_STR, True),
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
            channel_name = params.get('channel_name')
            store_name = params.get('store_name')
            start, end = tools.gen_ret_range(curr_page, max_page_num)
            info_data = self._query_handler(channel_name, store_name)
            data['info'] = info_data[start:end]
            data['num'] = len(info_data)
            return success(data)
        except Exception as e:
            log.warn(e)
            log.warn(traceback.format_exc())
            return error(UAURET.DATAERR)

    @with_database('uyu_core')
    def _query_handler(self, channel_name=None, store_name=None):
        where = {}
        if channel_name:
            where.update({'channel_name': channel_name})
        if store_name:
            where.update({'store_name': store_name})

        keep_fields = ['stores.id', 'stores.userid', 'stores.channel_id', 'stores.store_type', 'stores.store_contacter',
                       'stores.store_mobile', 'stores.store_addr', 'stores.training_amt_per', 'stores.divide_percent',
                       'stores.remain_times', 'stores.is_valid', 'stores.ctime', 'stores.store_name']
        ret = self.db.select_join(table1='stores', table2='channel', on={'channel.id': 'stores.channel_id'}, fields=keep_fields, where=where)
        # ret = self.db.select(table='stores', fields=keep_fields, where=st_where)
        for item in ret:
            ch_ret = self.db.select_one(table='channel', fields='channel_name', where={'id': item['channel_id']})
            item['channel_name'] = ch_ret.get('channel_name', '') if ch_ret else ''
            user_ret = self.db.select_one(table='auth_user', fields='nick_name', where={'id': item['userid']})
            item['nick_name'] = user_ret.get('nick_name') if user_ret else ''
            profile_ret = self.db.select_one(table='profile', fields='contact_name', where={'userid': item['userid']})
            item['contact_name'] = profile_ret.get('contact_name') if profile_ret else ''
            item['create_time'] = item['ctime'].strftime('%Y-%m-%d %H:%M:%S')
            item['store_type'] = UYU_STORE_ROLE_MAP.get(item['store_type'], '')
            item['status'] = item['is_valid']
            item['is_valid'] = UYU_STORE_STATUS_MAP.get(item['is_valid'], '')

        return ret

    def GET(self):
        try:
            data = self._get_handler()
            return data
        except Exception as e:
            log.warn(e)
            log.warn(traceback.format_exc())
            return error(UAURET.SERVERERR)


class StoreHandler(core.Handler):
    _get_handler_fields = [
         Field('userid', T_INT, False)
    ]

    _post_handler_fields = [
        Field("se_userid", T_INT, False),
        Field('userid', T_INT, False),
        Field('login_name', T_REG, False, match=r'^(1\d{10})$'),
        Field('phone_num', T_REG, False, match=r'^(1\d{10})$'),
        Field('email', T_STR, False, match=r'^[a-zA-Z0-9_\-\'\.]+@[a-zA-Z0-9_]+(\.[a-z]+){1,2}$'),
        #profile信息
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

        #门店信息
        Field('training_amt_per', T_INT, False),
        Field('divide_percent', T_FLOAT, False),
        # Field('is_prepayment', T_INT, False),
        # Field('channel_id', T_INT, False),
        Field('store_contacter', T_STR, False),
        Field('store_mobile', T_REG, False, match=r'^(1\d{10})$'),
        Field('store_addr', T_STR, False),
        Field('store_name', T_STR, False),
        # Field("store_type", T_INT, False, match=r'^([0-1]{1})$'),
    ]

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

        # log.debug("store_type: %d", params["store_type"])
        sdata = {}
        for key in uop.skey:
            if params.get(key, None) != None:
                log.debug("key: %s v: %s", key, params[key])
                sdata[key] = params[key]

        log.debug("udata: %s pdata: %s sdata: %s", udata, pdata, sdata)
        uop = UUser()
        ret = uop.call("store_info_change", params["userid"], udata, pdata, sdata)
        if ret == UYU_OP_ERR:
            return error(UAURET.CHANGESTOREERR)
        return success({"userid": params["userid"]})

    def POST(self):
        return self._post_handler()

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
        data["chn_data"] = uop.sdata

        udata = {}

        ret_filed = ["nick_name", "phone_num", "user_type", "email", "sex", "state"]
        for key in ret_filed:
            if uop.udata.get(key, None):
                udata[key] = uop.udata[key]

        udata["userid"] =uop.udata["id"]
        data["u_data"] = udata
        return success(data)

    def GET(self, *args):
        return self._get_handler()

class StoreEyeHandler(core.Handler):
    _get_handler_fields = [
        Field('phone_num', T_REG, False, match=r'^(1\d{10})$'),
    ]

    _post_handler_fields = [
        Field('userid', T_INT, False, match=r'^([0-9]{0,10})$'),
        Field('store_id', T_INT, False, match=r'^([0-9]{0,10})$'),
        Field('channel_id', T_INT, False, match=r'^([0-9]{0,10})$'),
    ]

    @uyu_check_session(g_rt.redis_pool, cookie_conf, UYU_SYS_ROLE_OP)
    @with_validator_self
    def _get_handler(self):
        params = self.validator.data
        uop = UUser()
        uop.call("load_user_by_mobile", params["mobile"])
        if len(uop.udata) == 0 or uop.user.get("user_type", -1) != define.UYU_USER_ROLE_EYESIGHT:
            return error(UAURET.USERROLEERR)

        ret = {}
        ret["mobile"] = uop.udata["phone_num"]
        ret["nick_name"] = uop.udata["nick_name"]

        return success(ret)

    def GET(self, *args):
        return self._get_handler()

    def _post_handler(self):
        params = self.validator.data
        uop = UUser()
        uop.store_bind_eyesight(params["userid"], params["store_id"], params["channel_id"])

    def POST(self, *arg):
        return self._post_handler()

class CreateStoreHandler(core.Handler):
    _post_handler_fields = [
        #用户基本信息
        Field('login_name', T_REG, False, match=r'^(1\d{10})$'),
        Field('phone_num', T_REG, False, match=r'^(1\d{10})$'),
        Field('email', T_STR, False, match=r'^[a-zA-Z0-9_\-\'\.]+@[a-zA-Z0-9_]+(\.[a-z]+){1,2}$'),
        #profile信息
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
        #门店信息
        Field('training_amt_per', T_INT, False),
        Field('divide_percent', T_FLOAT, False),
        # Field('is_prepayment', T_INT, False),
        Field('channel_id', T_INT, False),
        Field('store_contacter', T_STR, False),
        Field('store_mobile', T_REG, False, match=r'^(1\d{10})$'),
        Field('store_addr', T_STR, False),
        Field('store_name', T_STR, False),
    ]

    @uyu_check_session(g_rt.redis_pool, cookie_conf, UYU_SYS_ROLE_OP)
    @with_validator_self
    def _post_handler(self):
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

        sdata = {}
        for key in uop.skey:
            if params.get(key, None):
                sdata[key] = params[key]

        log.debug("udata: %s pdata: %s sdata: %s", udata, pdata, sdata)
        ret = uop.call("create_store_transaction", udata, pdata, sdata)
        if ret == UYU_OP_ERR:
            return error(UAURET.REGISTERERR)
        return success({"userid": uop.userid, "chnid": uop.chnid, "store_id": uop.store_id})

    def POST(self, *args):
        ret = self._post_handler()
        self.write(ret)


class StoreNameListHandler(core.Handler):
    
    @with_database('uyu_core')
    @uyu_check_session(g_rt.redis_pool, cookie_conf, UYU_SYS_ROLE_OP)
    def GET(self):
        sql = "select store_name from stores" 
        db_ret = self.db.query(sql)

        ret_list = []
        for item in db_ret:
            ret_list.append(item.get("store_name", ""))
        self.write(success(ret_list))
