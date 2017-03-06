# -*- coding: utf-8 -*-
from zbase.web import core
from zbase.web import template


class TrainBuyerManage(core.Handler):
    def GET(self):
        self.write(template.render('buyer.html'))

class TrainUseManage(core.Handler):
    def GET(self):
        self.write(template.render('use.html'))

