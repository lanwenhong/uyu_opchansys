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

class ChannelManage(core.Handler):
    def GET(self):
        self.write(template.render('channel.html'))


class ChannelInfoHandler(core.Handler):

    _get_handler_fields = [
        Field('page', T_INT, False),
        Field('maxnum', T_INT, False),
        Field('nick_name', T_STR, True),
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
            nick_name = params.get('nick_name')
            start, end = tools.gen_ret_range(curr_page, max_page_num)
            info_data = self._query_handler(nick_name=nick_name)
            data['info'] = info_data[start:end]
            data['num'] = len(info_data)
            return success(data)
        except Exception as e:
            log.warn(e)
            log.warn(traceback.format_exc())
            return error(UAURET.DATAERR)

    @with_database('uyu_core')
    def _query_handler(self, nick_name=None):
        profile_fields = ['contact_name', 'contact_phone']
        keep_fields = ['channel.id', 'channel.remain_times', 'channel.training_amt_per',
                       'channel.divide_percent', 'channel.status', 'channel.create_time',
                       'channel.userid', 'auth_user.login_name', 'auth_user.nick_name',
                       ]
        where = {'auth_user.nick_name': nick_name} if nick_name else {}
        ret = self.db.select_join(table1='channel', table2='auth_user', on={'channel.userid': 'auth_user.id'}, fields=keep_fields, where=where)
        for item in ret:
            userid = item['userid']
            profile_ret = self.db.select_one(table='profile', fields=profile_fields, where={'userid': userid})
            item['contact_name'] = profile_ret.get('contact_name', '') if profile_ret else ''
            item['contact_phone'] = profile_ret.get('contact_phone', '') if profile_ret else ''
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
