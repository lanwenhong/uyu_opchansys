# -*- coding: utf-8 -*-
from zbase.web import template
from uyubase.base.usession import USession
from uyubase.uyu import define
import logging
log = logging.getLogger()

def gen_ret_range(page, maxnum):
    start = maxnum * page - maxnum
    end = start + maxnum
    return start, end

def check_login(func):
    """sessionid userid all"""
    def _(self, *args, **kwargs):
        try:
            if not self.user.sauth:
                print 'before redirect sauth:', self.user.sauth
                self.redirect('/channel_op/v1/page/login.html')
            print 'sauth:', self.user.sauth
            ret = func(self, *args, **kwargs)
            return ret
        except Exception as e:
            log.warn(e)
            print 'except redirect'
            self.redirect('/channel_op/v1/page/login.html')
    return _


def check_session(redis_pool, cookie_conf, sys_role):
    def f(func):
        def _(self, *args, **kwargs):
            try:
                flag = True
                sk = self.get_cookie("sessionid")
                log.debug("sk: %s", sk)
                self.session = USession(redis_pool, cookie_conf, sk)
                v = self.session.get_session()
                if not v:
                    flag = False

                plist = define.PERMISSION_CHECK.get(sys_role, None)
                if not plist:
                    print 'tool permission error'
                    flag = False

                log.debug("tool get plist: %s", plist)
                user_type = v.get("user_type")
                if user_type not in plist:
                    print 'tool user type error'
                    flag = False

                if not flag:
                    self.redirect('/channel_op/v1/page/login.html')

                ret = func(self, *args, **kwargs)
                return ret
            except Exception as e:
                log.warn(e)
                print 'tool except redirect'
                self.redirect('/channel_op/v1/page/login.html')
        return _
    return f
