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
from uyubase.uyu.define import UYU_USER_ROLE_SUPER, UYU_USER_STATE_OK
from uyubase.uyu.define import UYU_STORE_EYESIGHT_BIND, UYU_STORE_EYESIGHT_BIND_MAP
from uyubase.uyu.define import UYU_SYS_ROLE_OP, UYU_OP_ERR

from runtime import g_rt
from config import cookie_conf
import logging, datetime, time
import tools
log = logging.getLogger()


class EyeSightInfoHandler(core.Handler):

    _get_handler_fields = [
        Field('userid', T_INT, False),
        Field('store_id', T_STR, False),
        Field('channel_id', T_STR, False),
    ]

    _post_handler_fields = [
        Field('userid', T_INT, False, match=r'^([0-9]{0,10})$'),
        Field('store_id', T_INT, False, match=r'^([0-9]{0,10})$'),
        Field('channel_id', T_INT, False, match=r'^([0-9]{0,10})$'),
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
            store_id = params.get('store_id')
            channel_id = params.get('channel_id')
            info_data = self._query_handler(store_id=store_id, channel_id=channel_id)
            data['info'] = info_data
            print 'info data', data
            return success(data)
        except Exception as e:
            log.warn(e)
            log.warn(traceback.format_exc())
            return error(UAURET.DATAERR)

    @with_database('uyu_core')
    def _query_handler(self, store_id=None, channel_id=None):
        where = {'is_valid': UYU_STORE_EYESIGHT_BIND}
        if store_id:
            where.update({'store_id': store_id})
        if channel_id:
            where.update({'channel_id': channel_id})

        user_fields = ['id', 'nick_name', 'phone_num']
        keep_fields = ['eyesight_id', 'store_id', 'ctime', 'id', 'is_valid']
        ret = self.db.select(table='store_eyesight_bind', fields=keep_fields, where=where)
        for item in ret:
            user_ret = self.db.select_one(table='auth_user', fields=user_fields, where={'id': item['eyesight_id']})
            item['nick_name'] = user_ret.get('nick_name') if user_ret else ''
            item['phone_num'] = user_ret.get('phone_num') if user_ret else ''
            item['ctime'] = item['ctime'].strftime('%Y-%m-%d %H:%M:%S')
            item['status'] = item['is_valid']
            item['is_valid'] = UYU_STORE_EYESIGHT_BIND_MAP.get(item['is_valid'], '')

        return ret

    def GET(self):
        try:
            data = self._get_handler()
            return data
        except Exception as e:
            log.warn(e)
            log.warn(traceback.format_exc())
            return error(UAURET.SERVERERR)

    @uyu_check_session(g_rt.redis_pool, cookie_conf, UYU_SYS_ROLE_OP)
    @with_validator_self
    def _post_handler(self):
        if not self.user.sauth:
            return error(UAURET.SESSIONERR)
        try:
            params = self.validator.data
            uop = UUser()
            uop.unbind_eyesight(params["userid"], params["store_id"], params["channel_id"])
            return success({})
        except Exception as e:
            log.warn(e)
            log.warn(traceback.format_exc())
            return error(UAURET.SERVERERR)

    def POST(self, *arg):
        return self._post_handler()


class EyeRegisterHandler(core.Handler):

    _post_handler_fields = [
        Field('mobile', T_REG, False, match=r'^(1\d{10})$'),
        Field('nick_name', T_STR, False),
        Field('username', T_STR, False),
        Field('email', T_STR, True, match=r'^[a-zA-Z0-9_\-\'\.]+@[a-zA-Z0-9_]+(\.[a-z]+){1,2}$'),
    ]


    @uyu_check_session(g_rt.redis_pool, cookie_conf, UYU_SYS_ROLE_OP)
    @with_validator_self
    def _post_handler(self):
        if not self.user.sauth:
            return error(UAURET.SESSIONERR)
        try:
            params = self.validator.data
            mobile = params['mobile']
            params['user_type'] = define.UYU_USER_ROLE_EYESIGHT
            params['password'] = mobile[-6:]
            uop = UUser()
            flag, userid = uop.internal_user_register(params)
            if flag:
                return success({'userid': userid})
            else:
                return error(UAURET.DATAEXIST)
        except Exception as e:
            log.warn(e)
            log.warn(traceback.format_exc())
            return error(UAURET.SERVERERR)


    def POST(self, *arg):
        return self._post_handler()
