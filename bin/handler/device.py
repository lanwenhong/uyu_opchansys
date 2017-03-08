# -*- coding: utf-8 -*-
import traceback
from zbase.web import core
from zbase.web import template
from zbase.web.validator import with_validator_self, Field, T_REG, T_INT, T_STR
from zbase.base.dbpool import with_database
from uyubase.base.response import success, error, UAURET
from uyubase.uyu.define import UYU_USER_ROLE_SUPER, UYU_USER_STATE_OK

import logging, datetime, time
import tools
log = logging.getLogger()

class DeviceManage(core.Handler):
    def GET(self):
        self.write(template.render('device.html'))


class DeviceInfoHandler(core.Handler):

    _get_handler_fields = [
        Field('page', T_INT, False),
        Field('maxnum', T_INT, False),
        Field('device_name', T_STR, True),
        Field('serial_number', T_STR, True),
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
            device_name = params.get('device_name')
            serial_number = params.get('serial_number')
            start, end = tools.gen_ret_range(curr_page, max_page_num)
            info_data = self._query_handler(device_name, serial_number)
            data['info'] = info_data[start:end]
            data['num'] = len(info_data)
            return success(data)
        except Exception as e:
            log.warn(e)
            log.warn(traceback.format_exc())
            return error(UAURET.DATAERR)

    @with_database('uyu_core')
    def _query_handler(self, device_name=None, serial_number=None):
        keep_fields = ['id', 'device_name', 'serial_number',
                       'hd_version', 'blooth_tag', 'scm_tag',
                       'status', 'channel_id', 'store_id',
                       'training_nums', 'create_time'
                       ]
        where = {}
        if device_name:
            where.update({'device_name': device_name})
        if serial_number:
            where.update({'serial_number': serial_number})
        ret = self.db.select(table='device', fields=keep_fields, where=where)
        for item in ret:
            channel_ret = self.db.select_one(table='channel', fields='userid', where={'id': item['channel_id']})
            store_ret = self.db.select_one(table='stores', fields='userid', where={'id': item['store_id']})
            channel_name = self.db.select_one(table='auth_user', fields='nick_name', where={'id': channel_ret['userid']})
            store_name = self.db.select_one(table='auth_user', fields='nick_name', where={'id': store_ret['userid']})
            item['channel_name'] = channel_name['nick_name']
            item['store_name'] = store_name['nick_name']
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
