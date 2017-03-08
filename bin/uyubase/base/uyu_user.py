#coding: utf-8

import os, sys
from zbase.base.dbpool import with_database
import logging, time, random
import traceback

from uyubase.base.response import success, error, UAURET 
from uyubase.uyu import define

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
        pass
    
    def user_register(self, *args, **kwargs):
        pass

    def create_profile(self, *args, **kwargs):
        pass
    
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

