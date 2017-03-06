# coding=utf-8
from zbase.web import core
from zbase.web import template


class Index(core.Handler):
    def GET(self):
        self.write(template.render('index.html'))
