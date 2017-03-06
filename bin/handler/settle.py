# -*- coding: utf-8 -*-
from zbase.web import core
from zbase.web import template


class SettleManage(core.Handler):
    def GET(self):
        self.write(template.render('settle.html'))

