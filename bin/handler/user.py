# -*- coding: utf-8 -*-
import traceback
from zbase.web import core
from zbase.web import template
from zbase.web.validator import with_validator_self, Field, T_REG, T_INT, T_STR, T_FLOAT
from zbase.base.dbpool import with_database
from uyubase.base.response import success, error, UAURET
from uyubase.base.usession import uyu_check_session, uyu_check_session_for_page
from uyubase.uyu.define import UYU_USER_ROLE_SUPER, UYU_USER_STATE_OK, UYU_SYS_ROLE_OP, UYU_OP_ERR, UYU_OP_OK
from uyubase.base.training_op import TrainingOP
from uyubase.uyu.define import UYU_OP_CATEGORY_MAP, UYU_ORDER_TYPE_MAP, UYU_ORDER_STATUS_MAP, UYU_BUSICD_MAP, UYU_TRAIN_USE_MAP
from uyubase.uyu import define
from uyubase.base.uyu_user import UUser

from runtime import g_rt
from config import cookie_conf
import logging, datetime, time
import tools
log = logging.getLogger()


class UserManage(core.Handler):
    @uyu_check_session_for_page(g_rt.redis_pool, cookie_conf, UYU_SYS_ROLE_OP)
    def GET(self):
        self.write(template.render('users.html'))


class UserInfoListHandler(core.Handler):

    _get_handler_fields = [
        Field('page', T_INT, False),
        Field('maxnum', T_INT, False),
        Field('phone_num', T_STR, True),
        Field('login_name', T_STR, True),
        Field('nick_name', T_STR, True),
    ]

    def _get_handler_errfunc(self, msg):
        return error(UAURET.PARAMERR, respmsg=msg)

    @uyu_check_session(g_rt.redis_pool, cookie_conf, UYU_SYS_ROLE_OP)
    @with_validator_self
    def _get_handler(self, *args):
        if not self.user.sauth:
            return error(UAURET.SESSIONERR)
        try:
            data = {}
            params = self.validator.data
            phone_num = params.get('phone_num', None)
            login_name = params.get('login_name', None)
            nick_name = params.get('nick_name', None)
            curr_page = params.get('page')
            max_page_num = params.get('maxnum')

            offset, limit = tools.gen_offset(curr_page, max_page_num)
            info_data = self._query_handler(offset, limit, phone_num, login_name, nick_name)

            data['info'] = self._trans_record(info_data)
            data['num'] = self._total_stat()
            return success(data)
        except Exception as e:
            log.warn(e)
            log.warn(traceback.format_exc())
            return error(UAURET.DATAERR)

    @with_database('uyu_core')
    def _total_stat(self):
        sql = 'select count(*) as total from auth_user where ctime>0'
        ret = self.db.get(sql)
        return int(ret['total']) if ret['total'] else 0

    @with_database('uyu_core')
    def _query_handler(self, offset, limit, phone_num=None, login_name=None, nick_name=None):
        keep_fields = [
            'id', 'phone_num', 'username', 'nick_name', 'state', 'user_type', 'ctime', 'login_name'
        ]

        where = {}
        # where = {'user_type': ('in', (define.UYU_USER_ROLE_EYESIGHT, define.UYU_USER_ROLE_COMSUMER))}

        if phone_num:
            where.update({'phone_num': phone_num})

        if login_name:
            where.update({'login_name': login_name})

        if nick_name:
            where.update({'nick_name': nick_name})

        other = ' order by ctime desc limit %d offset %d' % (limit, offset)
        log.debug('where: %s', where)

        ret = self.db.select(table='auth_user', fields=keep_fields, where=where, other=other)
        return ret


    @with_database('uyu_core')
    def _trans_record(self, data):
        if not data:
            return []

        for item in data:
            user_type = item['user_type']
            item['state'] = define.UYU_USER_STATE_MAP.get(item['state'])
            item['user_type'] = define.UYU_USER_ROLE_MAP.get(user_type)
            item['ctime'] = datetime.datetime.strftime(item['ctime'], '%Y-%m-%d %H:%M:%S')
            item['remain_times'] = self._collect_remain_times(self.db, item['id'], user_type)
            item['user_role'] = user_type

        return data


    def _collect_remain_times(self, conn, userid, user_type):
        if user_type in (define.UYU_USER_ROLE_EYESIGHT, define.UYU_USER_ROLE_COMSUMER):
            keep_fields = [
                'sum(remain_times) as remain_times'
            ]
            where = {'userid': userid}
            ret = conn.select_one(
                table='consumer', fields=keep_fields, where=where
            )
            remain_times = int(ret['remain_times']) if ret['remain_times'] else 0

        elif user_type in (define.UYU_USER_ROLE_STORE, define.UYU_USER_ROLE_HOSPITAL):
            where = {'userid': userid}
            keep_fields = ['remain_times']
            ret = conn.select_one(table='stores', fields=keep_fields, where=where)
            remain_times = int(ret['remain_times']) if ret['remain_times'] else 0

        elif user_type == define.UYU_USER_ROLE_CHAN:
            where = {'userid': userid}
            keep_fields = ['remain_times']
            ret = conn.select_one(table='channel', fields=keep_fields, where=where)
            remain_times = int(ret['remain_times']) if ret['remain_times'] else 0

        else:
            remain_times = '无'

        return remain_times


    def GET(self):
        try:
            self.set_headers({'Content-Type': 'application/json; charset=UTF-8'})
            data = self._get_handler()
            return data
        except Exception as e:
            log.warn(e)
            log.warn(traceback.format_exc())
            return error(UAURET.SERVERERR)


class UserChangePasswordHandler(core.Handler):
    _post_handler_fields = [
        Field('userid', T_INT, False),
        Field('password', T_STR, False),
        Field('echo_password', T_STR, False),
    ]

    def _post_handler_errfunc(self, msg):
        return error(UAURET.PARAMERR, respmsg=msg)

    @uyu_check_session(g_rt.redis_pool, cookie_conf, UYU_SYS_ROLE_OP)
    @with_validator_self
    def _post_handler(self, *args):
        if not self.user.sauth:
            return error(UAURET.SESSIONERR)
        params = self.validator.data
        userid = params['userid']
        password = params["password"]
        echo_password = params["echo_password"]

        ret = self._check_user(userid)
        if not ret:
            return error(UAURET.USERERR)
        user_type = ret['user_type']
        login_name = ret['login_name']
        u_op = UUser()
        ret = u_op.call("change_password_all", userid, password, echo_password, user_type, login_name)
        if ret != UYU_OP_OK:
            return error(ret)
        return success({})


    @with_database('uyu_core')
    def _check_user(self, userid):
        ret = self.db.select_one(table='auth_user', where={'id': userid})
        return ret


    def POST(self, *args):
        self.set_headers({'Content-Type': 'application/json; charset=UTF-8'})
        ret = self._post_handler(self, args)
        self.write(ret)
