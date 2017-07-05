# -*- coding: utf-8 -*-
import logging
import datetime
from zbase.base.dbpool import get_connection_exception
from uyubase.uyu import define
log = logging.getLogger()

def gen_ret_range(page, maxnum):
    start = maxnum * page - maxnum
    end = start + maxnum
    return start, end

def gen_offset(page, maxnum):
     limit = maxnum
     offset = (page -1) * maxnum
     return offset, limit

def channel_name_to_id(name):
    data = []
    with get_connection_exception('uyu_core') as conn:
        ret = conn.select(table='channel', fields='id', where={'channel_name': name});
        if not ret:
            return data
        for item in ret:
            data.append(item['id'])

        return data

def store_name_to_id(name):
    data = []
    with get_connection_exception('uyu_core') as conn:
        ret = conn.select(table='stores', fields='id', where={'store_name': name});
        if not ret:
            return data
        for item in ret:
            data.append(item['id'])

        return data

def mobile_to_id(phone_num):
    data = []
    with get_connection_exception('uyu_core') as conn:
        ret = conn.select(table='auth_user', fields='id', where={'phone_num': phone_num});
        if not ret:
            return data
        for item in ret:
            data.append(item['id'])

        return data


def nickname_to_id(name):
    data = []
    with get_connection_exception('uyu_core') as conn:
        ret = conn.select(table='auth_user', fields='id', where={'nick_name': name})
        if not ret:
            return data
        for item in ret:
            data.append(item['id'])

        return data


def channel_id_to_name(channel_id):
    with get_connection_exception('uyu_core') as conn:
        ret = conn.select_one(table='channel', fields='channel_name', where={'id': channel_id})
        return ret


def store_id_to_name(store_id):
    with get_connection_exception('uyu_core') as conn:
        ret = conn.select_one(table='stores', fields='store_name', where={'id': store_id})
        return ret


def create_rule(data):
    f_name ='create_rule'
    log.debug('func=%s|in=%s', f_name, data)
    with get_connection_exception('uyu_core') as conn:
        name = data.get('name')
        total_amt = data.get('total_amt')
        training_times = data.get('training_times')
        description = data.get('description')
        now = datetime.datetime.now()
        values = {
            'name': name,
            'total_amt': total_amt,
            'training_times': training_times,
            'ctime': now,
            'utime': now,
            'is_valid': define.UYU_RULES_STATUS_OPEN
        }
        if description not in ['', None]:
            values['description'] = description
        ret = conn.insert(table='rules', values=values)
        log.debug('func=%s|insert|ret=%s', f_name, ret)
        return ret


def single_rule(rule_id):
    f_name = 'single_rule'
    log.debug('func=%s|rule_id=%s', f_name, rule_id)
    with get_connection_exception('uyu_core') as conn:
        where = {'id': rule_id}
        keep_fields = [
            'name', 'total_amt', 'training_times',
            'description', 'is_valid'
        ]
        ret = conn.select_one(table='rules', fields=keep_fields, where=where)
        if ret and ret['total_amt']:
            ret['total_amt'] = ret['total_amt'] / 100.0
        log.debug('func=%s|ret=%s', f_name, ret)
        return ret


def edit_rule(rule_id, name, total_amt, training_times, description=None):
    f_name = 'edit_rule'
    info = {
        'name': name,
        'total_amt': total_amt,
        'training_times': training_times,
    }
    if description not in ['', None]:
        info['description'] = description

    log.debug('func=%s|in=%s|rule_id=%s', f_name, info, rule_id)
    with get_connection_exception('uyu_core') as conn:
        where = {'id': rule_id}
        now = datetime.datetime.now()
        info['utime'] = now
        values = info
        ret = conn.update(table='rules', values=values, where=where)
        log.debug('func=%s|db ret=%s', f_name, ret)
        return ret


def get_rule_name():
    f_name = 'get_rule_name'
    log.debug('func=%s', f_name)
    with get_connection_exception('uyu_core') as conn:
        ret = conn.select(table='rules', fieles=['name'])
        log.debug('func=%s|db ret=%s', f_name, ret)
        return ret
