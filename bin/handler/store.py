# -*- coding: utf-8 -*-
import traceback
from zbase.web import core
from zbase.web import template
from zbase.web.validator import with_validator_self, Field, T_REG, T_INT, T_STR
from zbase.base.dbpool import with_database
from response.response import success, error, UAURET, UYU_USER_ROLE_SUPER, UYU_USER_STATE_OK

import logging, datetime, time
import tools
log = logging.getLogger()

class StoreManage(core.Handler):
    def GET(self):
        self.write(template.render('store.html'))


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
            #channel_name -> channel_id
            #store_name -> store_id
            info_data = self._query_handler(channel_id=None, store_id=None)
            data['info'] = info_data[start:end]
            data['num'] = len(info_data)
            return success(data)
        except Exception as e:
            log.warn(e)
            log.warn(traceback.format_exc())
            return error(UAURET.DATAERR)

    @with_database('uyu_core')
    def _query_handler(self, channel_id, store_id):
        where = {}
        if channel_id:
            where.update({'channel_id': channel_id})
        if store_id:
            where.update({'store_id': store_id})

        keep_fields = ['id', 'userid', 'channel_id', 'store_type', 'store_contacter',
                       'store_mobile', 'store_addr', 'training_amt_per', 'divide_percent',
                       'remain_times', 'is_valid', 'create_time']
        ret = self.db.select(table='stores', fields=keep_fields, where=where)
        for item in ret:
            item['channel_name'] = str(item['channel_id'])
            user_ret = self.db.select_one(table='auth_user', fields='nick_name', where={'id': item['userid']})
            item['nick_name'] = user_ret.get('nick_name') if user_ret else ''
            profile_ret = self.db.select_one(table='profile', fields='contact_name', where={'userid': item['userid']})
            item['contact_name'] = profile_ret.get('contact_name') if profile_ret else ''
            item['create_time'] = item['create_time'].strftime('%Y-%m-%d %H:%M:%S')

        return ret

    def GET(self):
        try:
            data = self._get_handler()
            return data
        except Exception as e:
            log.warn(e)
            log.warn(traceback.format_exc())
            return error(UAURET.SERVERERR)
