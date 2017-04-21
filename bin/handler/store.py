# -*- coding: utf-8 -*-
import traceback
from zbase.web import core
from zbase.web import template
from zbase.web.validator import with_validator_self, Field, T_REG, T_INT, T_STR, T_FLOAT
from zbase.base.dbpool import with_database
from uyubase.base.response import success, error, UAURET
from uyubase.base.usession import uyu_check_session, uyu_check_session_for_page
from uyubase.base.uyu_user import UUser
from uyubase.uyu import define


from uyubase.uyu.define import UYU_USER_ROLE_SUPER, UYU_USER_STATE_OK, UYU_USER_ROLE_EYESIGHT
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

    def _post_handler_errfunc(self, msg):
        return error(UAURET.PARAMERR, respmsg=msg)

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
        Field('is_valid', T_INT, True),
    ]

    def _get_handler_errfunc(self, msg):
        return error(UAURET.PARAMERR, respmsg=msg)

    @uyu_check_session(g_rt.redis_pool, cookie_conf, UYU_SYS_ROLE_OP)
    @with_validator_self
    def _get_handler(self, *args):
        if not self.user.sauth:
            return error(UAURET.SESSIONERR)
        try:
            data = {}
            params = self.validator.data
            curr_page = params.get('page')
            max_page_num = params.get('maxnum')
            channel_name = params.get('channel_name')
            store_name = params.get('store_name')
            is_valid = params.get('is_valid', None)

            start, end = tools.gen_ret_range(curr_page, max_page_num)
            info_data = self._query_handler(channel_name, store_name, is_valid)

            data['info'] = self._trans_record(info_data[start:end])
            data['num'] = len(info_data)
            return success(data)
        except Exception as e:
            log.warn(e)
            log.warn(traceback.format_exc())
            return error(UAURET.DATAERR)

    @with_database('uyu_core')
    def _query_handler(self, channel_name=None, store_name=None, is_valid=None):
        where = {}

        if channel_name:
            where.update({'channel_name': channel_name})

        if store_name:
            where.update({'store_name': store_name})

        if is_valid in (0, 1):
            where.update({'stores.is_valid': is_valid})

        other = ' order by ctime desc'

        keep_fields = ['stores.id', 'stores.userid', 'stores.channel_id', 'stores.store_type', 'stores.store_contacter',
                       'stores.store_mobile', 'stores.store_addr', 'stores.training_amt_per', 'stores.divide_percent',
                       'stores.remain_times', 'stores.is_valid', 'stores.ctime', 'stores.store_name', 'stores.is_prepayment', 'channel.channel_name']

        ret = self.db.select_join(table1='stores', table2='channel', on={'channel.id': 'stores.channel_id'}, fields=keep_fields, where=where, other=other)

        return ret


    @with_database('uyu_core')
    def _trans_record(self, data):
        if not data:
            return []

        for item in data:
            user_ret = self.db.select_one(table='auth_user', fields='phone_num', where={'id': item['userid']})
            item['phone_num'] = user_ret.get('phone_num') if user_ret else ''
            item['create_time'] = item['ctime'].strftime('%Y-%m-%d %H:%M:%S')
            item['store_type'] = UYU_STORE_ROLE_MAP.get(item['store_type'], '')
            item['status'] = item['is_valid']
            item['is_valid'] = UYU_STORE_STATUS_MAP.get(item['is_valid'], '')
            item['training_amt_per'] = item['training_amt_per'] / 100.0 if item['training_amt_per'] else 0.00
            if item.get('is_prepayment') == 0:
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


class StoreHandler(core.Handler):
    _get_handler_fields = [
         Field('userid', T_INT, False)
    ]

    def _get_handler_errfunc(self, msg):
        return error(UAURET.PARAMERR, respmsg=msg)


    _post_handler_fields = [
        Field("se_userid", T_INT, False),
        Field('userid', T_INT, False),
        # Field('login_name', T_REG, False, match=r'^(1\d{10})$'),
        Field('phone_num', T_REG, False, match=r'^(1\d{10})$'),
        Field('email', T_STR, True, match=r'^[a-zA-Z0-9_\-\'\.]+@[a-zA-Z0-9_]+(\.[a-z]+){1,2}$'),
        #profile信息
        Field('org_code',  T_STR, True),
        Field('license_id',  T_STR, True),
        Field('legal_person',  T_STR, True),
        Field('business',  T_STR, True),
        Field('front_business',  T_STR, True),
        Field('account_name',  T_STR, True),
        Field('bank_name',  T_STR, True),
        Field('bank_account',  T_STR, True),
        Field('contact_name',  T_STR, False),
        Field('contact_phone',  T_STR, False, match=r'^(0\d{2,3}\-\d{7,8})|(1\d{10})$'),
        Field('contact_email',  T_STR, True),
        Field('address',  T_STR, False),

        #门店信息
        Field('training_amt_per', T_INT, False),
        Field('divide_percent', T_FLOAT, True),
        Field('is_prepayment', T_INT, False, match=r'^([0-1]{1})$'),
        Field('channel_id', T_INT, False),
        Field('store_contacter', T_STR, False),
        Field('store_mobile', T_REG, False, match=r'^(0\d{2,3}\-\d{7,8})|(1\d{10})$'),
        Field('store_addr', T_STR, True),
        Field('store_name', T_STR, False),
        Field("store_type", T_INT, False, match=r'^([0-1]{1})$'),
    ]

    def _post_handler_errfunc(self, msg):
        return error(UAURET.PARAMERR, respmsg=msg)

    @with_database('uyu_core')
    def _can_modify(self, channel_id):
        ret = self.db.select_one(table='channel',fields='is_prepayment', where={'id': channel_id})
        is_prepayment = ret.get('is_prepayment')
        return is_prepayment

    @with_database('uyu_core')
    def _update_device_eyesight_channel(self, channel_id, store_userid):
        ret = self.db.select_one(table='stores', fields='id', where={'userid': store_userid})
        store_id = ret.get('id')
        self.db.update(table='device', values={'channel_id': channel_id}, where={'store_id': store_id})
        self.db.update(table='store_eyesight_bind', values={'channel_id': channel_id}, where={'store_id': store_id})

    @uyu_check_session(g_rt.redis_pool, cookie_conf, UYU_SYS_ROLE_OP)
    @with_validator_self
    def _post_handler(self):
        if not self.user.sauth:
            return error(UAURET.SESSIONERR)
        uop = UUser()
        params = self.validator.data
        store_userid = params['userid']
        log.debug('store change store_userid=%s', store_userid)
        uop.load_info_by_userid(store_userid)
        origin_channel_id = uop.sdata['channel_id']
        origin_store_is_prepayment = uop.sdata['is_prepayment']

        remain_times = uop.sdata['remain_times']
        channel_id = params['channel_id']
        store_is_prepayment = params['is_prepayment']
        origin_channel_is_prepayment = self._can_modify(origin_channel_id)
        new_channel_is_prepayment = self._can_modify(channel_id)

        log.debug("channel_id: %d origin_channel_id: %d store_is_prepayment: %d origin_store_is_prepayment: %d", channel_id, origin_channel_id, store_is_prepayment, origin_store_is_prepayment)

        if origin_channel_id == channel_id and store_is_prepayment == origin_store_is_prepayment:
            log.debug("not change channel and store type not change pass!!!")
            pass
        else:
            if new_channel_is_prepayment == define.UYU_CHAN_DIV_TYPE and store_is_prepayment != define.UYU_STORE_DIV_TYPE:
                return error(UAURET.STOREERR1)

            if remain_times < 0 and store_is_prepayment == define.UYU_STORE_PREPAY_TYPE and origin_store_is_prepayment == define.UYU_STORE_DIV_TYPE:
                return error(UAURET.STOREERR1)

        params['login_name'] = params['phone_num']

        udata = {}
        for key in ["login_name", "nick_name", "phone_num"]:
            if params.get(key, None):
                udata[key] = params[key]

        pdata = {}
        for key in uop.pkey:
            if params.get(key, None):
                pdata[key] = params[key]

        sdata = {}
        for key in uop.skey:
            if params.get(key, None) not in [None, '']:
                log.debug("key: %s v: %s", key, params[key])
                sdata[key] = params[key]

        log.debug("udata: %s pdata: %s sdata: %s", udata, pdata, sdata)
        uop = UUser()
        ret = uop.call("store_info_change", params["userid"], udata, pdata, sdata)
        if ret == UYU_OP_ERR:
            return error(UAURET.CHANGESTOREERR)
        if origin_channel_id != channel_id:
            # 更新这个门店下绑定下设备的channel_id
            # 更新这个门店下视光师绑定的channel_id
            self._update_device_eyesight_channel(channel_id, store_userid)

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

    def _get_handler_errfunc(self, msg):
        return error(UAURET.PARAMERR, respmsg=msg)

    _post_handler_fields = [
        Field('userid', T_INT, False, match=r'^([0-9]{0,10})$'),
        Field('store_id', T_INT, False, match=r'^([0-9]{0,10})$'),
        Field('channel_id', T_INT, False, match=r'^([0-9]{0,10})$'),
    ]

    def _post_handler_errfunc(self, msg):
        return error(UAURET.PARAMERR, respmsg=msg)

    @uyu_check_session(g_rt.redis_pool, cookie_conf, UYU_SYS_ROLE_OP)
    @with_validator_self
    def _get_handler(self):
        if not self.user.sauth:
            return error(UAURET.SESSIONERR)
        params = self.validator.data
        uop = UUser()
        uop.call("load_user_by_mobile", params["phone_num"])
        log.debug('udata: %s', uop.udata)
        # if len(uop.udata) == 0 or uop.udata.get("user_type", -1) != UYU_USER_ROLE_EYESIGHT:
        if len(uop.udata) == 0 or uop.udata.get("user_type", -1) not in [define.UYU_USER_ROLE_EYESIGHT, define.UYU_USER_ROLE_COMSUMER]:
            return error(UAURET.USERROLEERR)

        ret = {}
        ret["id"] = uop.udata["id"]
        ret["mobile"] = uop.udata["phone_num"]
        ret["nick_name"] = uop.udata["nick_name"]
        ret["username"] = uop.udata.get("username", '')

        return success(ret)

    def GET(self, *args):
        return self._get_handler()

    @with_validator_self
    def _post_handler(self):
        try:
            params = self.validator.data
            uop = UUser()
            flag, err_code = uop.store_bind_eyesight(params["userid"], params["store_id"], params["channel_id"])
            if flag:
                return success({})
            else:
                return error(err_code)
        except Exception as e:
            log.warn(e)
            log.warn(traceback.format_exc())
            return error(UAURET.DATAEXIST)

    def POST(self, *arg):
        return self._post_handler()


class CreateStoreHandler(core.Handler):
    _post_handler_fields = [
        #用户基本信息
        Field('login_name', T_REG, False, match=r'^(1\d{10})$'),
        Field('phone_num', T_REG, False, match=r'^(1\d{10})$'),
        Field('email', T_STR, True, match=r'^[a-zA-Z0-9_\-\'\.]+@[a-zA-Z0-9_]+(\.[a-z]+){1,2}$'),
        #profile信息
        Field('org_code',  T_STR, True),
        Field('license_id',  T_STR, True),
        Field('legal_person',  T_STR, True),
        Field('business',  T_STR, True),
        Field('front_business',  T_STR, True),
        Field('account_name',  T_STR, True),
        Field('bank_name',  T_STR, True),
        Field('bank_account',  T_STR, True),
        Field('contact_name',  T_STR, False),
        Field('contact_phone',  T_STR, False, match=r'^(0\d{2,3}\-\d{7,8})|(1\d{10})$'),
        Field('contact_email',  T_STR, True),
        Field('address',  T_STR, False),
        #门店信息
        Field('training_amt_per', T_INT, False),
        Field('divide_percent', T_FLOAT, True),
        Field('is_prepayment', T_INT, False, match=r'^([0-1]{1})$'),
        Field('channel_id', T_INT, False),
        Field('store_contacter', T_STR, False),
        Field('store_mobile', T_REG, False, match=r'^(0\d{2,3}\-\d{7,8})|(1\d{10})$'),
        Field('store_addr', T_STR, True),
        Field('store_name', T_STR, False),
        Field("store_type", T_INT, False, match=r'^([0-1]{1})$'),
    ]

    def _post_handler_errfunc(self, msg):
        return error(UAURET.PARAMERR, respmsg=msg)

    @with_database('uyu_core')
    def _can_modify(self, channel_id):
        ret = self.db.select_one(table='channel',fields='is_prepayment', where={'id': channel_id})
        is_prepayment = ret.get('is_prepayment')
        return is_prepayment


    @uyu_check_session(g_rt.redis_pool, cookie_conf, UYU_SYS_ROLE_OP)
    @with_validator_self
    def _post_handler(self):
        if not self.user.sauth:
            return error(UAURET.SESSIONERR)
        params = self.validator.data
        channel_id = params['channel_id']
        store_is_prepayment = params['is_prepayment']
        channel_is_prepayment = self._can_modify(channel_id)
        if channel_is_prepayment != store_is_prepayment and channel_is_prepayment == define.UYU_CHAN_DIV_TYPE:
            return error(UAURET.STOREERR1)
        params['username'] = params['store_name']
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
            if params.get(key, None) not in [None, '']:
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
        if not self.user.sauth:
            return error(UAURET.SESSIONERR)
        sql = "select store_name from stores"
        db_ret = self.db.query(sql)

        ret_list = []
        for item in db_ret:
            ret_list.append(item.get("store_name", ""))
        self.write(success(ret_list))
