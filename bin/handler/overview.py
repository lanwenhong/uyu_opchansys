# -*- coding: utf-8 -*-
import traceback
from zbase.web import core
from zbase.web import template

from uyubase.base.response import success, error, UAURET
from uyubase.base.usession import uyu_check_session, USession, uyu_check_session_for_page
from uyubase.base.uyu_user import UUser
from uyubase.uyu.define import UYU_USER_ROLE_SUPER, UYU_USER_STATE_OK, UYU_SYS_ROLE_OP
from zbase.web.validator import with_validator_self, Field, T_REG, T_INT, T_STR
from zbase.base.dbpool import with_database

from runtime import g_rt
from config import cookie_conf
import logging, datetime, time

log = logging.getLogger()


class OverView(core.Handler):
    @uyu_check_session_for_page(g_rt.redis_pool, cookie_conf, UYU_SYS_ROLE_OP)
    def GET(self):
        self.write(template.render('overview.html'))


class OverViewInfoHandler(core.Handler):
    _get_handler_fields = [
        Field('se_userid', T_INT, False),
    ]

    def _get_handler_errfunc(self, msg):
        return error(UAURET.PARAMERR, respmsg=msg)

    @with_validator_self
    def _get_handler(self, *args):
        try:
            data = {}
            params = self.validator.data
            # userid = params.get('se_userid')
            channel_total, store_total = self._query_handler()
            data['channel_total'] = channel_total
            data['store_total'] = store_total
            return success(data)
        except Exception as e:
            log.warn(e)
            log.warn(traceback.format_exc())
            return error(UAURET.DATAERR)

    @with_database('uyu_core')
    def _query_handler(self):
        channel_ret = self.db.select_one(table='channel', fields='count(id) as total')
        store_ret = self.db.select_one(table='stores', fields='count(id) as total')
        channel_len = int(channel_ret['total']) if channel_ret['total'] else 0
        store_len = int(store_ret['total']) if store_ret['total'] else 0
        return channel_len, store_len

    def GET(self):
        try:
            data = self._get_handler()
            return data
        except Exception as e:
            log.warn(e)
            log.warn(traceback.format_exc())
            return error(UAURET.SERVERERR)
