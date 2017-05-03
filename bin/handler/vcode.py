# -*- coding: utf-8 -*-
import traceback
from zbase.web import core
from zbase.web import template
from zbase.web.validator import with_validator_self, Field, T_REG, T_INT, T_STR, T_FLOAT
from zbase.base.dbpool import with_database
from uyubase.base.response import success, error, UAURET
from uyubase.base.usession import uyu_check_session, uyu_check_session_for_page
from uyubase.uyu.define import UYU_USER_ROLE_SUPER, UYU_USER_STATE_OK, UYU_SYS_ROLE_OP, UYU_OP_ERR, UYU_OP_OK

from runtime import g_rt
from config import cookie_conf
import logging, datetime, time
import tools
log = logging.getLogger()


class VerifyCodeManage(core.Handler):
    @uyu_check_session_for_page(g_rt.redis_pool, cookie_conf, UYU_SYS_ROLE_OP)
    def GET(self):
        self.write(template.render('vcode.html'))


class VerifyCodeInfoListHandler(core.Handler):

    _get_handler_fields = [
        Field('page', T_INT, False),
        Field('maxnum', T_INT, False),
        Field('phone_num', T_STR, True),
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
            phone_num = params.get('phone_num', None)
            curr_page = params.get('page')
            max_page_num = params.get('maxnum')
            start, end = tools.gen_ret_range(curr_page, max_page_num)
            info_data = self._query_handler(phone_num)
            data['info'] = self._trans_record(info_data[start:end])
            data['num'] = len(info_data)
            return success(data)
        except Exception as e:
            log.warn(e)
            log.warn(traceback.format_exc())
            return error(UAURET.DATAERR)



    @with_database('uyu_core')
    def _query_handler(self, phone_num=None):
        keep_fields = [
            'id', 'mobile', 'code', 'stime', 'etime'
        ]

        where = {}

        if phone_num:
            where.update({'mobile': phone_num})

        other = ' order by stime desc'
        log.debug('where: %s', where)

        ret = self.db.select(table='verify_code', fields=keep_fields, where=where, other=other)
        return ret


    @with_database('uyu_core')
    def _trans_record(self, data):
        if not data:
            return []

        for item in data:
            mobile = item['mobile']
            stime = item['stime']
            etime = item['etime']
            item['phone_num'] = mobile
            item['stime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(stime))
            item['etime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(etime))


        return data



    def GET(self):
        try:
            self.set_headers({'Content-Type': 'application/json; charset=UTF-8'})
            data = self._get_handler()
            return data
        except Exception as e:
            log.warn(e)
            log.warn(traceback.format_exc())
            return error(UAURET.SERVERERR)