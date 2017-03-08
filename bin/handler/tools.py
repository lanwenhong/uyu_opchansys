# -*- coding: utf-8 -*-
from zbase.web import template
import logging
log = logging.getLogger()

def gen_ret_range(page, maxnum):
    start = maxnum * page - maxnum
    end = start + maxnum
    return start, end

def check_login(func):
    def _(self, *args, **kwargs):
        try:
            if not self.user.sauth:
                return self.write(template.render("login.html"))

            ret = func(self, *args, **kwargs)
            return ret
        except:
            log.warn('check_login error: %s' % traceback.format_exc())
            return self.write(template.render("login.html"))
    return _
