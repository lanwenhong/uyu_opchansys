# -*- coding: utf-8 -*-
import traceback
from zbase.web import core
from zbase.web import template
from zbase.web.validator import with_validator_self, Field, T_REG, T_INT, T_STR, T_FLOAT
from zbase.base.dbpool import with_database
from uyubase.base.response import success, error, UAURET
from uyubase.base.usession import uyu_check_session, uyu_check_session_for_page
from uyubase.uyu.define import UYU_USER_ROLE_SUPER, UYU_USER_STATE_OK, UYU_SYS_ROLE_OP, UYU_OP_ERR, UYU_OP_OK
from uyubase.base.training_op import TrainingOP
from uyubase.uyu.define import UYU_OP_CATEGORY_MAP, UYU_ORDER_TYPE_MAP, UYU_ORDER_STATUS_MAP, UYU_BUSICD_MAP, UYU_TRAIN_USE_MAP
from uyubase.uyu import define

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
        Field('mobile', T_STR, True),
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
            channel_name = params.get('channel_name', None)
            store_name = params.get('store_name', None)
            phone_num = params.get('phone_num', None)

            start, end = tools.gen_ret_range(curr_page, max_page_num)
            info_data = self._query_handler(channel_name, store_name, phone_num)

            data['info'] = self._trans_record(info_data[start:end])
            data['num'] = len(info_data)
            return success(data)
        except Exception as e:
            log.warn(e)
            log.warn(traceback.format_exc())
            return error(UAURET.DATAERR)


    @with_database('uyu_core')
    def _query_handler(self, channel_name=None, store_name=None, phone_num=None):
        where = {}

        if channel_name:
            channel_list = tools.channel_name_to_id(channel_name)
            if channel_list:
                where.update({'channel_id': ('in', channel_list)})
            else:
                return []

        if store_name:
            store_list = tools.store_name_to_id(store_name)
            if store_list:
                where.update({'store_id': ('in', store_list)})
            else:
                return []

        if phone_num:
            consumer_list = tools.mobile_to_id(phone_num)
            if consumer_list:
                where.update({'consumer_id': ('in', consumer_list)})
            else:
                return []

        other = ' order by create_time desc'

        keep_fields = [
            'id', 'channel_id', 'store_id',
            'consumer_id', 'category', 'op_type',
            'training_times', 'training_amt', 'op_name',
            'status', 'create_time', 'busicd', 'orderno'
        ]
        ret = self.db.select(table='training_operator_record', fields=keep_fields, where=where, other=other)

        return ret


    @with_database('uyu_core')
    def _trans_record(self, data):
        if not data:
            return []

        for item in data:
            channel_ret = self.db.select_one(table='channel', fields='channel_name', where={'id': item['channel_id']})
            store_ret = self.db.select_one(table='stores', fields='store_name', where={'id': item['store_id']})
            item['channel_name'] = channel_ret.get('channel_name', '') if channel_ret else ''
            item['store_name'] = store_ret.get('store_name', '') if store_ret else ''
            item['create_time'] = item['create_time'].strftime('%Y-%m-%d %H:%M:%S')
            item['category'] = UYU_OP_CATEGORY_MAP.get(item['category'], '')
            item['op_type'] = UYU_ORDER_TYPE_MAP.get(item['op_type'], '')
            item['training_amt'] = item['training_amt'] / 100.0
            item['is_valid'] = item['status']
            item['status'] = UYU_ORDER_STATUS_MAP.get(item['status'], '')
            item['busicd_name'] = item['busicd']

        return data


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
            # data['info'] = info_data[start:end]
            data['info'] = self._trans_record(info_data[start:end])
            data['num'] = len(info_data)
            return success(data)
        except Exception as e:
            log.warn(e)
            log.warn(traceback.format_exc())
            return error(UAURET.DATAERR)

    @with_database('uyu_core')
    def _query_handler(self, channel_name=None, store_name=None, consumer_mobile=None, eyesight=None, create_time=None):
        where = {}
        if channel_name:
            channel_list = tools.channel_name_to_id(channel_name)
            if channel_list:
                where.update({'channel_id': ('in', channel_list)})
            else:
                return []

        if store_name:
            store_list = tools.store_name_to_id(store_name)
            if store_list:
                where.update({'store_id': ('in', store_list)})
            else:
                return []

        if consumer_mobile:
            consumer_list = tools.mobile_to_id(consumer_mobile)
            if consumer_list:
                where.update({'consumer_id': ('in', consumer_list)})
            else:
                return []

        if eyesight:
            eyesight_list = tools.mobile_to_id(eyesight)
            if eyesight_list:
                where.update({'eyesight_id': ('in', eyesight_list)})
            else:
                return []

        if create_time:
            create_time = datetime.datetime.strptime(create_time, '%Y-%m-%d')
            start_time = create_time.replace(hour=0, minute=0, second=0)
            end_time = create_time.replace(hour=23, minute=59, second=59)
            where.update({'ctime': ('between', (start_time, end_time))})

        other = ' order by ctime desc'

        keep_fields = ['id', 'channel_id', 'store_id', 'device_id', 'consumer_id', 'eyesight_id', 'comsumer_nums', 'status', 'ctime']

        ret = self.db.select(table='training_use_record', fields=keep_fields, where=where, other=other)

        return ret

    @with_database('uyu_core')
    def _trans_record(self, data):
        if not data:
            return []

        for item in data:
            channel_ret = self.db.select_one(table='channel', fields='channel_name', where={'id': item['channel_id']})
            store_ret = self.db.select_one(table='stores', fields='store_name', where={'id': item['store_id']})
            device_name = self.db.select_one(table='device', fields='device_name', where={'id': item['device_id']})
            eyesight_name = self.db.select_one(table='auth_user', fields='username', where={'id': item['eyesight_id']})
            item['channel_name'] = channel_ret.get('channel_name') if channel_ret else ''
            item['store_name'] = store_ret.get('store_name') if store_ret else ''
            item['device_name'] = device_name.get('device_name') if device_name else ''
            item['eyesight_name'] = eyesight_name.get('username') if eyesight_name else ''
            item['create_time'] = item['ctime'].strftime('%Y-%m-%d %H:%M:%S')
            item['status'] = UYU_TRAIN_USE_MAP.get(item['status'], '')

        return data


    def GET(self):
        try:
            data = self._get_handler()
            return data
        except Exception as e:
            log.warn(e)
            log.warn(traceback.format_exc())
            return error(UAURET.SERVERERR)

#渠道系统用
#class ChanBuyTrainingsOrderHandler(core.Handler):
#    _post_handler_fields = [
#        Field("busicd", T_STR, False, match=r'^([0-9]{6})$'),
#        Field('channel_id', T_STR, False),
#        Field('training_times', T_INT, False),
#        Field('training_amt', T_INT, False),
#        Field('ch_training_amt_per', T_INT, False),
#    ]
#
#    @with_validator_self
#    def _post_handler(self):
#        params = self.validator.data
#        log.debug("client data: %s", params)
#        top = TrainingOP(params)
#        ret = top.create_chan_buy_trainings_order()
#        if ret == UYU_OP_ERR:
#            return error(UAURET.ORDERERR)
#        return success({})
#
#    def POST(self):
#        return self._post_handler()

class OrgAllotToChanOrderHandler(core.Handler):
    _post_handler_fields = [
        Field("busicd", T_STR, False, match=r'^([0-9]{6})$'),
        Field('channel_id', T_INT, False),
        Field('training_times', T_INT, False),
        Field('training_amt', T_INT, False),
        Field('ch_training_amt_per', T_INT, False),
    ]

    @with_database('uyu_core')
    def _check_permission(self, params):
        channel_id = params["channel_id"]
        channel_reocord = self.db.select_one("channel", {"id": channel_id})
        training_amt = params["training_amt"]
        training_times = params["training_times"]
        ch_training_amt_per = params["training_amt_per"]

        is_valid = channel_reocord["is_valid"]

        if is_valid == define.UYU_CHAN_STATUS_CLOSE:
            return UYU_OP_ERR

        if ch_training_amt_per != channel_reocord["training_amt_per"] or training_amt != training_times * ch_training_amt_per:
            return UYU_OP_ERR

        return UYU_OP_OK

    @uyu_check_session(g_rt.redis_pool, cookie_conf, UYU_SYS_ROLE_OP)
    @with_validator_self
    def _post_handler(self):
        params = self.validator.data
        log.debug("client data: %s", params)
        if params["busicd"] != define.BUSICD_ORG_ALLOT_TO_CHAN:
            log.warn('client busicd: %s real busicd: %s', params['busicd'], define.BUSICD_ORG_ALLOT_TO_CHAN)
            return error(UAURET.BUSICEERR)

        self.user.load_user()
        top = TrainingOP(params, self.user.udata)

        ret = top.create_org_allot_to_chan_order()
        if ret == UYU_OP_ERR:
            return error(UAURET.ORDERERR)
        return success({})

    def POST(self):
        return self._post_handler()

#FIMME
#是否是公司帮渠道分配
class OrgAllotToStoreOrderHandler(core.Handler):
    _post_handler_fields = [
        Field("busicd", T_STR, False, match=r'^([0-9]{6})$'),
        Field('channel_id', T_INT, False),
        Field('store_id', T_INT, False),
        Field('training_times', T_INT, False),
        # Field('training_amt', T_INT, False),
        Field('training_amt', T_FLOAT, False),
        Field('store_training_amt_per', T_INT, False),
    ]

    @with_database('uyu_core')
    def _check_permission(self, params):
        store_id = params["store_id"]
        chan_id = params["channel_id"]
        store_record = self.db.select_one("stores", {"id": store_id})
        chan_record = self.db.select_one("channel", {"id": chan_id})

        training_amt = params["training_amt"]
        training_times = params["training_times"]
        store_training_amt_per = params["store_training_amt_per"]
        s_is_valid = store_record["is_valid"]
        c_is_valid = chan_record["is_valid"]

        if c_is_valid == define.UYU_CHAN_STATUS_CLOSE or s_is_valid == define.UYU_STROE_STATUS_CLOSE:
            log.warn("s_is_valid: %d c_is_valid: %d", s_is_valid, c_is_valid)
            return UYU_OP_ERR

        if store_training_amt_per != store_record["training_amt_per"] or training_amt != training_times * store_training_amt_per:
            log.warn("store_training_amt_per: %d in db: %d", store_training_amt_per, store_record["training_amt_per"])
            return UYU_OP_ERR

        return UYU_OP_OK


    @uyu_check_session(g_rt.redis_pool, cookie_conf, UYU_SYS_ROLE_OP)
    @with_validator_self
    def _post_handler(self):
        params = self.validator.data
        log.debug("client data: %s", params)
        if params["busicd"] != define.BUSICD_CHAN_ALLOT_TO_STORE:
            return error(UAURET.BUSICEERR)

        if self._check_permission(params) == UYU_OP_ERR:
            return error(UAURET.ORDERERR)

        self.user.load_user()
        top = TrainingOP(params, self.user.udata)

        ret = top.create_chan_allot_to_store_order()

        if top.respcd:
            return error(top.respcd)

        if ret == UYU_OP_ERR:
            return error(UAURET.ORDERERR)
        return success({})

    def POST(self):
        return self._post_handler()


class OrderCancelHandler(core.Handler):
    _post_handler_fields = [
        Field("order_no", T_STR, False, match=r'^([0-9]{33})$'),
    ]

    @uyu_check_session(g_rt.redis_pool, cookie_conf, UYU_SYS_ROLE_OP)
    @with_validator_self
    def _post_handler(self):
        params = self.validator.data
        order_no = params["order_no"]
        log.debug("order_no: %s", order_no)
        top = TrainingOP(params, order_no=order_no)
        ret = top.order_cancel()

        if ret == UYU_OP_OK:
            return success({})

        return error(UAURET.ORDERERR)

    def POST(self):
        return self._post_handler()
