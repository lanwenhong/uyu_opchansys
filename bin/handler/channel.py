# -*- coding: utf-8 -*-
from zbase.web import core
from zbase.web import template
from uyubase.base.usession import uyu_check_session 
from response.response import success, error, UAURET, UYU_USER_ROLE_SUPER, UYU_USER_STATE_OK

from runtime import g_rt
from config import cookie_conf

class ChannelManage(core.Handler):
    def GET(self):
        self.write(template.render('channel.html'))



class ChannelHandler(core.Handler):
    
    @uyu_check_session(g_rt, cookie_conf, UYU_USER_ROLE_SUPER)
    def _post_handler(self, *args):
        if not self.user.sauth:
            return error(UAURET.SESSIONERR)
        params = self.req.input()
        return success({})

    def POST(self, *args):
        return self._post_handler()


