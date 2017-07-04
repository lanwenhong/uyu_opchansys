# -*- coding: utf-8 -*-
import traceback
from zbase.web import core
from zbase.web import template
from zbase.web.validator import with_validator_self, Field, T_REG, T_INT, T_STR
from zbase.base.dbpool import with_database
from uyubase.base.response import success, error, UAURET
from uyubase.uyu.define import UYU_USER_ROLE_SUPER, UYU_USER_STATE_OK, UYU_SYS_ROLE_OP
from uyubase.base.usession import uyu_check_session, uyu_check_session_for_page
from uyubase.uyu.define import UYU_SYS_ROLE_OP, UYU_OP_OK, UYU_OP_ERR, UYU_CHAN_MAP, UYU_DEVICE_MAP, UYU_RULES_STATUS_OPEN, UYU_RULES_STATUS_MAP
from uyubase.base.uyu_user import UUser
from uyubase.uyu import define

from uyubase.base.usession import uyu_check_session, uyu_check_session_for_page

import logging, datetime, time
import tools
from runtime import g_rt
from config import cookie_conf
log = logging.getLogger()

class RulesInfoHandler(core.Handler):

    @uyu_check_session(g_rt.redis_pool, cookie_conf, UYU_SYS_ROLE_OP)
    def _get_handler(self, *args):
        if not self.user.sauth:
            return error(UAURET.SESSIONERR)
        try:
            info_data = self._query_handler()
            data = self._trans_record(info_data)
            return success(data)
        except Exception as e:
            log.warn(e)
            log.warn(traceback.format_exc())
            return error(UAURET.DATAERR)

    @with_database('uyu_core')
    def _query_handler(self):
        where = {'is_valid': UYU_RULES_STATUS_OPEN}
        keep_fields = ['*']
        other = ' order by name desc'
        ret = self.db.select(table='rules', fields=keep_fields, where=where, other=other)
        return ret

    @with_database('uyu_core')
    def _trans_record(self, data):
        if not data:
            return []

        for item in data:
            item['total_amt'] = '%0.2f' % (item['total_amt'] / 100.0)

        return data


    def GET(self):
        try:
            self.set_headers({'Content-Type': 'application/json; charset=UTF-8'})
            data = self._get_handler()
            return data
        except Exception as e:
            log.warn(e)
            log.warn(traceback.format_exc())


class RuleManage(core.Handler):
    @uyu_check_session_for_page(g_rt.redis_pool, cookie_conf, UYU_SYS_ROLE_OP)
    def GET(self):
        self.write(template.render('rule.html'))


class RulePageHandler(core.Handler):

    _get_handler_fields = [
        Field('page', T_INT, False),
        Field('maxnum', T_INT, False),
        Field('name', T_STR, True),
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
            cls_name = 'RulePageHandler'
            params = self.validator.data
            name = params.get('name')
            curr_page = params.get('page')
            max_page_num = params.get('maxnum')
            log.debug('class=%s|method=GET|params=%s', cls_name, params)
            offset, limit = tools.gen_offset(curr_page, max_page_num)
            info_data = self._query_handler(offset, limit, name)
            data['info'] = self._trans_record(info_data)
            data['num'] = self._total_stat()
            return success(data)
        except Exception as e:
            log.warn(e)
            log.warn(traceback.format_exc())
            return error(UAURET.DATAERR)

    @with_database('uyu_core')
    def _query_handler(self, offset, limit, name=None):
        keep_fields = [
            'name', 'total_amt', 'training_times', 'description',
            'ctime', 'is_valid', 'id'
        ]
        where = {}
        if name not in ['', None]:
            where['name'] = name
        
        other = ' order by ctime desc limit %d offset %d' % (limit, offset)
        ret = self.db.select(table='rules', fields=keep_fields, where=where, other=other)
        return ret

    def _trans_record(self, data):
        if not data:
            return []

        for item in data:
            item['ctime'] = datetime.datetime.strftime(item['ctime'], '%Y-%m-%d %H:%M:%S')
            item['state'] = define.UYU_RULES_STATUS_MAP.get(item['is_valid'], '')
            item['total_amt'] = item['total_amt'] / 100.0 if item['total_amt'] else 0.00

        return data

    @with_database('uyu_core')
    def _total_stat(self):
        sql = 'select count(*) as total from rules where ctime>0'
        ret = self.db.get(sql)
        return int(ret['total']) if ret['total'] else 0

    def GET(self):
        try:
            self.set_headers({'Content-Type': 'application/json; charset=UTF-8'})
            data = self._get_handler()
            return data
        except Exception as e:
            log.warn(e)
            log.warn(traceback.format_exc())
            return error(UAURET.SERVERERR)


class RuleCreateHandler(core.Handler):

    _post_handler_fields = [
        Field('name', T_STR, False),
        Field('total_amt', T_INT, False),
        Field('training_times', T_INT, False),
        Field('description', T_STR, True)
    ]

    def _post_handler_errfunc(self, msg):
        return error(UAURET.PARAMERR, respmsg=msg)

    @uyu_check_session(g_rt.redis_pool, cookie_conf, UYU_SYS_ROLE_OP)
    def _post_handler(self):
        params = self.validator.data
        ret = tools.create_rule(params)
        if ret != 1:
            return error(UAURET.DATAERR)
        return success({})

    def POST(self):
        try:
            self.set_headers({'Content-Type': 'application/json; charset=UTF-8'})
            data = self._post_handler()
            return data
        except Exception as e:
            log.warn(e)
            log.warn(traceback.format_exc())
            return error(UAURET.SERVERERR)
