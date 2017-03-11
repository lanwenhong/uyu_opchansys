# -*- coding: utf-8 -*-
import traceback
from zbase.web import core
from zbase.web import template
from zbase.web.validator import with_validator_self, Field, T_REG, T_INT, T_STR
from zbase.base.dbpool import with_database
from uyubase.base.response import success, error, UAURET
from uyubase.base.usession import uyu_check_session, uyu_check_session_for_page
from uyubase.uyu.define import UYU_USER_ROLE_SUPER, UYU_USER_STATE_OK, UYU_SYS_ROLE_OP, UYU_OP_ERR, UYU_OP_OK
from uyubase.base.training_op import TrainingOP

from runtime import g_rt
from config import cookie_conf
import logging, datetime, time
import tools
log = logging.getLogger()


class TrainBuyerManage(core.Handler):
    @uyu_check_session_for_page(g_rt.redis_pool, cookie_conf, UYU_SYS_ROLE_OP)
    def GET(self):
        self.write(template.render('buyer.html'))

class TrainUseManage(core.Handler):
    @uyu_check_session_for_page(g_rt.redis_pool, cookie_conf, UYU_SYS_ROLE_OP)
    def GET(self):
        self.write(template.render('use.html'))


class TrainBuyInfoHandler(core.Handler):

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
            info_data = self._query_handler(channel_name, store_name)
            data['info'] = info_data[start:end]
            data['num'] = len(info_data)
            return success(data)
        except Exception as e:
            log.warn(e)
            log.warn(traceback.format_exc())
            return error(UAURET.DATAERR)

    @with_database('uyu_core')
    def _query_handler(self, channel_name=None, store_name=None):
        where = {}
        keep_fields = ['id', 'channel_id', 'store_id', 'consumer_id', 'category', 'op_type', 'training_times', 'training_amt', 'op_name', 'status', 'create_time']
        ret = self.db.select(table='training_operator_record', fields=keep_fields, where=where)
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


class TrainUseInfoHandler(core.Handler):

    _get_handler_fields = [
        Field('page', T_INT, False),
        Field('maxnum', T_INT, False),
        Field('channel_name', T_STR, True),
        Field('store_name', T_STR, True),
        Field('consumer_mobile', T_STR, True),
        Field('eyesight', T_STR, True),
        Field('create_time', T_STR, True),
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
            consumer_mobile = params.get('consumer_mobile')
            eyesight = params.get('eyesight')
            create_time = params.get('create_time')
            start, end = tools.gen_ret_range(curr_page, max_page_num)
            info_data = self._query_handler(channel_name, store_name, consumer_mobile, eyesight, create_time)
            data['info'] = info_data[start:end]
            data['num'] = len(info_data)
            return success(data)
        except Exception as e:
            log.warn(e)
            log.warn(traceback.format_exc())
            return error(UAURET.DATAERR)

    @with_database('uyu_core')
    def _query_handler(self, channel_name=None, store_name=None, consumer_mobile=None, eyesight=None, create_time=None):
        where = {}
        keep_fields = ['id', 'channel_id', 'store_id', 'device_id', 'consumer_id', 'eyesight_id', 'comsumer_nums', 'status', 'create_time']
        ret = self.db.select(table='training_use_record', fields=keep_fields, where=where)
        for item in ret:
            channel_ret = self.db.select_one(table='channel', fields='userid', where={'id': item['channel_id']})
            store_ret = self.db.select_one(table='stores', fields='userid', where={'id': item['store_id']})
            device_name = self.db.select_one(table='device', fields='device_name', where={'id': item['device_id']})
            channel_name = self.db.select_one(table='auth_user', fields='nick_name', where={'id': channel_ret['userid']})
            store_name = self.db.select_one(table='auth_user', fields='nick_name', where={'id': store_ret['userid']})
            eyesight_name = self.db.select_one(table='auth_user', fields='nick_name', where={'id': item['eyesight_id']})
            item['channel_name'] = channel_name['nick_name']
            item['store_name'] = store_name['nick_name']
            item['device_name'] = device_name['device_name']
            item['eyesight_name'] = eyesight_name['nick_name']
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


class ChanBuyTrainingsOrderHandler(core.Handler):
    _post_handler_fields = [
        Field("busicd", T_STR, False, match=r'^([0-9]{6})$'),
        Field('channel_id', T_STR, False),
        Field('training_times', T_INT, False),
        Field('training_amt', T_INT, False),
        Field('ch_training_amt_per', T_INT, False),
    ]
    
    @with_validator_self
    def _post_handler(self):
        params = self.validator.data
        top = TrainingOP(params)
        ret = top.create_chan_buy_trainings_order()
        if ret == UYU_OP_ERR:
            return error(UAURET.ORDERERR)
        return success({})

    def POST(self):
        return self._post_handler()
