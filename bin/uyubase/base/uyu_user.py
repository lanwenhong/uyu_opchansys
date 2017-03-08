#coding: utf-8

import os, sys
from zbase.base.dbpool import with_database
import logging, time, random
import traceback

from uyubase.base.response import success, error, UAURET 
from uyubase.uyu import define
from uyubase.uyu.define import UYU_OP_OK, UYU_OP_ERR

import logging, datetime
log = logging.getLogger()

class VCode:
    def __init__(self):
        pass
    
    @with_database('uyu_core')
    def gen_vcode(self, mobile):
        try:
            now = int(time.time())
            sql = "select * from verify_code where mobile='%s' and stime<%d and etime>%d" % (mobile, now, now)
            dbret = self.db.get(sql)

            if not dbret:
                vcode = ''
                for i in xrange(0, 4):
                    vcode += str(random.randint(0,9))
                sql = "insert into verify_code set mobile='%s', code='%s', stime=%d, etime=%d" % (mobile, vcode, int(time.time()), int(time.time()) + 60)
                self.db.execute(sql)
                return vcode
            else:
                return dbret["code"]
        except:
            log.warn(traceback.format_exc())
            return None

    def sms_vcode(self, vcode):
        pass

class UUser:
    def __init__(self):
        self.userid = None
        self.udata = {}
        self.pdata = {}

        self.ukey = [
            "login_name", "nick_name", "phone_num", "password",
            "ctime", "utime", "user_type", "email",
            "sex", "state",
        ]

        self.pkey = [
            "userid", "org_code", "license_id", "legal_person", 
            "business", "front_business", "account_name", "bank_name",
            "bank_account", "contact_name", "contact_phone", "contact_email", 
            "address", "org_pic", "license_pic", "idcard_no", 
            "idcard_front", "idcard_back", "state", "ctime",
        ]

        self.chan_key = [
            "userid", "remain_times", "training_amt_per", "divide_percent",
            "status", "is_valid", "is_prepayment", "ctime",
        ]
    
    def __gen_vsql(self, klist, cdata):
        sql_value = {}
        for key in cdata:
            if cdata.get(key, None):
                sql_value[key] = cdata[key]
        return sql_value
    
    #用户注册
    @with_database('uyu_core')
    def user_register(self, udata):
        try:
            sql_value = self.__gen_vsql(self.ukey, udata)
            sql_value["ctime"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            mobile = udata["login_name"]
            #默认密码手机号后六位
            sql_value["password"] = mobile[-6:]
            sql_value["state"] = define.UYU_USER_STATE_OK 
            ret = self.db.insert("auth_user", sql_value)
            if ret == 0:
                return UYU_OP_ERR
            self.userid = self.db.last_insert_id()
            return UYU_OP_OK
        except:
            log.debug(traceback.format_exc())
            return UYU_OP_ERR

        
    #修改档案表
    @with_database('uyu_core')
    def profile_update(self, userid, **kwargs):
        try:
            sql_value = self.__gen_vsql(self.pkey, kwargs)
            ret = self.db.update("profile", sql_value, {"userid": userid})
            if ret == 0:
                return UYU_OP_ERR
            return UYU_OP_OK
        except:
            log.debug(traceback.format_exc())
            return UYU_OP_ERR

    #创建渠道事务
    @with_database('uyu_core')
    def create_chan_transaction(self, udata, pdata, cdata):
        try:
            self.db.start()
            sql_value = self.__gen_vsql(self.ukey, udata)
            sql_value["ctime"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            mobile = udata["login_name"]
            sql_value["password"] = mobile[-6:]
            sql_value["state"] = define.UYU_USER_STATE_OK 

            self.db.insert("auth_user", sql_value)
            userid = self.db.last_insert_id()
            sql_value = self.__gen_vsql(self.pkey, pdata)
            sql_value["userid"] = userid
            self.db.insert("profile", sql_value)
            
            sql_value = self.__gen_vsql(self.chan_key, cdata)
            sql_value["userid"] = userid

            self.db.insert("channel", sql_value)
            chnid = self.db.last_insert_id()
            self.db.commit()

            self.userid = userid
            self.chnid = chnid
            return UYU_OP_OK
        except:
            log.debug(traceback.format_exc())
            self.db.rollback()
            return UYU_OP_ERR

    def _check_permission(self, user_type, sys_role):
        log.debug(define.PERMISSION_CHECK)
        plist = define.PERMISSION_CHECK.get(sys_role, None)
        if not plist:
            return False 

        log.debug("plist: %s", plist)
        if user_type not in plist:
            return False
        return True

    @with_database('uyu_core')
    def check_userlogin(self, mobile, password, sys_role):
        sql = "select * from auth_user where phone_num='%s' and password='%s'" % (mobile, password)
        dbret = self.db.get(sql)
        if not dbret:
            return UAURET.USERERR, None 
        if dbret["password"] != password:
            return UAURET.PWDERR, None
        user_type = dbret.get("user_type", -1)
        if not self._check_permission(user_type, sys_role):
            return UAURET.ROLEERR, None
        return UAURET.OK, dbret

    @with_database('uyu_core')
    def change_password(self, mobile, vcode, password):
        try:
            now = int(time.time())
            sql = "select * from verify_code where mobile='%s' and stime<%d and etime>%d" % (mobile, now, now)
            dbret = self.db.get(sql)
            log.debug("dbret: %s", dbret)

            if dbret and vcode == dbret['code']:
                sql = "update auth_user set password='%s' where phone_num='%s'" % (password, mobile)
                self.db.execute(sql)
                return UAURET.OK

            return UAURET.VCODEERR
        except:
            log.warn(traceback.format_exc())
            return UAURET.VCODEERR

