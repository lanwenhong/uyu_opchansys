# -*- coding: utf-8 -*-
import traceback
from zbase.web import core
from zbase.web import template
from uyubase.uyu import define
from uyubase.uyu.define import UYU_USER_ROLE_SUPER, UYU_USER_STATE_OK, UYU_SYS_ROLE_OP
from uyubase.base.usession import uyu_check_session, uyu_check_session_for_page
from zbase.web.validator import with_validator_self, Field, T_REG, T_INT, T_STR, T_FLOAT
from zbase.base.dbpool import with_database
from uyubase.base.uyu_user import UUser
from uyubase.base.response import success, error, UAURET

from runtime import g_rt
from config import cookie_conf
import logging, datetime, time
import tools
log = logging.getLogger()


class SettleManage(core.Handler):
    @uyu_check_session_for_page(g_rt.redis_pool, cookie_conf, UYU_SYS_ROLE_OP)
    def GET(self):
        self.write(template.render('settle.html'))


class SettleInfoHandler(core.Handler):

    _get_handler_fields = [
        Field('page', T_INT, False),
        Field('maxnum', T_INT, False),
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

            start, end = tools.gen_ret_range(curr_page, max_page_num)
            info_data = self._query_handler()

            data['info'] = self._trans_record(info_data[start:end])
            data['num'] = len(info_data)
            return success(data)
        except Exception as e:
            log.warn(traceback.format_exc())
            return error(UAURET.DATAERR)

    @with_database('uyu_core')
    def _query_handler(self):
        where = {}
        keep_fields = '*'
        ret = self.db.select(table='settlement_record', fields=keep_fields, where=where)
        return ret

    @with_database('uyu_core')
    def _trans_record(self, data):
        if not data:
            return []

        for item in data:
            channel_ret = tools.channel_id_to_name(item['channel_id'])
            store_ret = tools.store_id_to_name(item['store_id'])
            item['channel_name'] = channel_ret.get('channel_name') if channel_ret else ''
            item['store_name'] = store_ret.get('store_name') if store_ret else ''
            item['settle_cycle'] = item['settle_cycle'].strftime('%Y-%m-%d')
            item['settle_time'] = item['settle_time'].strftime('%Y-%m-%d')
            item['channel_divide_amt'] = '%0.2f' % (item['channel_divide_amt'] / 100.0)
            item['store_divide_amt'] = '%0.2f' % (item['store_divide_amt'] / 100.0)
            item['company_divide_amt'] = '%0.2f' % (item['company_divide_amt'] / 100.0)
            item['settle_amt'] = '%0.2f' % (item['settle_amt'] / 100.0)

        return data


    def GET(self):
        try:
            data = self._get_handler()
            return data
        except Exception as e:
            log.warn(e)
            log.warn(traceback.format_exc())
            return error(UAURET.SERVERERR)
