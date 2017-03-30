# -*- coding: utf-8 -*-
import traceback
import calendar
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
        Field('channel_name', T_STR, True),
        Field('store_name', T_STR, True),
        Field('start_time', T_STR, True),
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
            channel_name = params.get('channel_name', None)
            store_name = params.get('store_name', None)
            start_time = params.get('start_time', None)

            start, end = tools.gen_ret_range(curr_page, max_page_num)
            info_data = self._query_handler(channel_name, store_name, start_time)

            data['info'] = self._trans_record(info_data[start:end])
            data['num'] = len(info_data)
            return success(data)
        except Exception as e:
            log.warn(traceback.format_exc())
            return error(UAURET.DATAERR)

    @with_database('uyu_core')
    def _query_handler(self, channel_name=None, store_name=None, start_time=None):
        where = {}
        keep_fields = '*'
        other = ' order by settle_cycle desc '

        if channel_name:
            channel_list = tools.channel_name_to_id(channel_name)
            if channel_list:
                where.update({'channel_id': ('in', channel_list)})
            else:
                return []

        if store_name:
            store_list = tools.store_name_to_id(store_name)
            log.debug('#store_list=%s', store_list)
            if store_list:
                where.update({'store_id': ('in', store_list)})
            else:
                return []

        if start_time:
            year_month = start_time.split('-')
            year = int(year_month[0])
            month = int(year_month[1])
            last_day = calendar.monthrange(year, month)[1]
            stime = datetime.datetime.strptime(start_time, '%Y-%m')
            etime = datetime.datetime(year=year, month=month, day=last_day)
            where.update({'settle_cycle': ('between', [stime, etime])})

        ret = self.db.select(table='settlement_record', fields=keep_fields, where=where, other=other)
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
            item['settle_cycle'] = item['settle_cycle'].strftime('%Y-%m')
            item['settle_time'] = item['settle_time'].strftime('%Y-%m-%d')
            item['channel_divide_amt'] = '%0.2f' % (item['channel_divide_amt'] / 100.0)
            item['store_divide_amt'] = '%0.2f' % (item['store_divide_amt'] / 100.0)
            item['company_divide_amt'] = '%0.2f' % (item['company_divide_amt'] / 100.0)
            item['settle_amt'] = '%0.2f' % (item['settle_amt'] / 100.0)
            item['buyer_type'] = define.UYU_BUYER_TYPE_MAP.get(item['buyer_type'], '')

        return data


    def GET(self):
        try:
            data = self._get_handler()
            return data
        except Exception as e:
            log.warn(e)
            log.warn(traceback.format_exc())
            return error(UAURET.SERVERERR)
