# coding=utf-8
from zbase.web import core
from zbase.web import template


class Login(core.Handler):
    def GET(self):
        self.write(template.render('login.html'))
