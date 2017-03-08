# -*- coding: utf-8 -*-
from zbase.web import core
from zbase.web import template

from uyubase.base.response import success, error, UAURET
from uyubase.base.usession import uyu_check_session, USession
from uyubase.base.uyu_user import UUser
from uyubase.uyu.define import UYU_USER_ROLE_SUPER, UYU_USER_STATE_OK

from runtime import g_rt
from config import cookie_conf

import logging, datetime, time

log = logging.getLogger()

class OverView(core.Handler):
    @uyu_check_session(g_rt.redis_pool, cookie_conf, UYU_USER_ROLE_SUPER)
    def GET(self):
        self.write(template.render('overview.html'))


