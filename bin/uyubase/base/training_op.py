#coding: utf-8
import os, sys
from zbase.utils import createid
from zbase.base.dbpool import with_database
from zbase.base import dbpool
import traceback
from uyubase.uyu.define import UYU_OP_OK, UYU_OP_ERR, UYU_ORDER_STATUS_NEED_CONFIRM

class TrainingOP:
    def __init__(self, cdata=None):
        self.data_key = (
            "busicd",  "channel_id", "store_id", "consumer_id",
            "category", "op_type", "pay_type", "training_times",
            "training_amt", "status", "op_name", "orderno",
            "create_time", "update_time",
        )
        self.db_data = {}
        self.cdata = cdata 

    def create_orderno(self):
        with dbpool.get_connection('uyu_core') as conn:
            myid = new_id64(conn=conn)
            return datetime.datetime.now().strftime("%Y%m%d%H%M%S") + str(myid)
    
    def __gen_vsql(self, cdata):
        sql_value = {}
        order_no = self.create_orderno()
        log.debug("order_no: %s", order_no)

        for key in cdata:
            if self.cdata.get(key, None):
                sql_value[key] = self.cdata[key]

        sql_value["orderno"] = order_no
        sql_value["status"] = UYU_ORDER_STATUS_NEED_CONFIRM 
        create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql_value["create_time"] = create_time

        return sql_value

    #@with_database('uyu_core')
    #def create(self, cdata):
    #    sql_value = self.__gen_vsql(cdata) 
    #    try:
    #        self.db.insert("training_operator_record", sql_value)
    #        return UYU_OP_OK
    #    except:
    #        log.warn(traceback.format_exc())
    #        return UYU_OP_ERR
    
    #公司分配给渠道训练次数的订单
    @with_database('uyu_core')
    def create_org_allot_to_chan_order(self, chan_id, cdata):
        sql_value = self.__gen_vsql(cdata)
        try:
            self.db.start()
            self.db.insert("training_operator_record", sql_value)
            training_times = self.cdata["training_times"]
            sql = "update channel set remain_times=remain_times+%d where id=%d" % (training_times, chan_id)
            ret = self.db.execute(sql)
            if ret == 0:
                self.db.rollback()
                return UYU_OP_ERR
            else:
                self.db.commit()
                return UYU_OP_OK
        except:
            log.warn(traceback.format_exc())
            self.db.rollback()
            return UYU_OP_ERR

    @with_database('uyu_core') 
    def create_chan_allot_to_store(self, chan_id, store_id):
        sql_value = self.__gen_sql()
        try:
            self.db.start()
            self.db.insert("training_operator_record", sql_value)
            training_times = self.cdata["training_times"]
            sql = "update channel set remain_times=remain_times-%d where id=%d and remain_times>=%d" % (training_times, chan_id, training_times)
            ret = self.db.execute(sql)
            if ret == 0:
                self.db.rollback()
                return UYU_OP_ERR
            sql = "update stores set remain_times=remain_times+%d where id=%d" % (training_times, store_id)
            ret = self.db.execute(sql)
            if ret == 0:
                self.db.rollback()
                return UYU_OP_ERR
            self.db.commit()
            return UYU_OP_OK
        except:
            log.warn(traceback.format_exc())
            self.db.rollback()
            return UYU_OP_ERR

    def get_order_by_no(self, order_no):
        pass

    def set_order_status(self, status):
        pass
