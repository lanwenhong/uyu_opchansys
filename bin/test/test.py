#coding: utf-8

from zbase.base import logger
from zbase.base.http_client import RequestsClient
from zbase.server.client import HttpClient

log = logger.install('stdout')


def test_login():
    SERVER   = [{'addr':('127.0.0.1', 8083), 'timeout':20},]
    client = HttpClient(SERVER, client_class = RequestsClient)
    send = {"mobile": "15882895784", "password": "123456"}
    #send = {"mobile": "18987867889", "password": "867889"}
    ret = client.post('/channel_op/v1/api/login', send)
    log.info(ret)
    print client.client.headers


def test_vcode():
    SERVER   = [{'addr':('127.0.0.1', 8083), 'timeout':20},]
    client = HttpClient(SERVER, client_class = RequestsClient)
    send = {"mobile": "15882895784"}
    ret = client.post('/channel_op/v1/api/sms_send', send)
    log.info(ret)

def test_vcode_verify():
    SERVER   = [{'addr':('127.0.0.1', 8083), 'timeout':20},]
    client = HttpClient(SERVER, client_class = RequestsClient)
    send = {"mobile": "15882895784", "vcode":"3924", "password":"123456"}
    ret = client.post('/channel_op/v1/api/passwd_change', send)
    log.info(ret)




def test_chn_query():
    SERVER   = [{'addr':('127.0.0.1', 8083), 'timeout':20},]
    client = HttpClient(SERVER, client_class = RequestsClient)
    send = {"userid": 1129, "se_userid": 1000}
    headers = {'cookie': 'sessionid=85aeb24b-04ba-47ed-975b-ba763fc1b2a4'}
    ret = client.get('/channel_op/v1/api/channel', send, headers=headers)

    log.debug(ret)




def test_chn_register():
     SERVER   = [{'addr':('127.0.0.1', 8083), 'timeout':20},]
     client = HttpClient(SERVER, client_class = RequestsClient)
     send = {
        "se_userid": 1000,

        "login_name": "14789897654",
        "nick_name": "张四",
        "phone_num": "14789897654",
        "channel_name": "大中国四川成都牛逼大渠道",
        "email": "lanwenhong@xxx.com",
        "org_code": "xxxxxx1111111111",
        "license_id": "xxxxxx11111111111", 
        "legal_person": "李四",
        "business": "大富豪",
        "front_business": "岁月",
        "account_name": "天天",
        "bank_name": "建设银行",
        "bank_account": "78878878787878787878",
        "contact_name": "天天",
        "contact_phone": "15882895989",
        "contact_email": "lanwenhong@xxxx.com",
        "address": "成都天府新区",
        "training_amt_per": 100,
        "divide_percent": 0.45,
        "is_prepayment": 0,
     }
     headers = {'cookie': 'sessionid=85aeb24b-04ba-47ed-975b-ba763fc1b2a4'}
     ret = client.post('/channel_op/v1/api/channel_create', send, headers=headers)
     log.info(ret)

def test_store_register():
     SERVER   = [{'addr':('127.0.0.1', 8083), 'timeout':20},]
     client = HttpClient(SERVER, client_class = RequestsClient)
     send = {
        "se_userid": 1000,

        "login_name": "13988887779",
        "phone_num": "13988887779",
        "channel_name": "大中国四川成都牛逼大渠道",
        "email": "lanwenhong@xxx.com",
        "org_code": "xxxxxx1111111111",
        "license_id": "xxxxxx11111111111", 
        "legal_person": "李四",
        "business": "大富豪",
        "front_business": "岁月",
        "account_name": "天天",
        "bank_name": "建设银行",
        "bank_account": "78878878787878787878",
        "contact_name": "天天",
        "contact_phone": "15882895989",
        "contact_email": "lanwenhong@xxxx.com",
        "address": "成都天府新区",

        "training_amt_per": 100,
        "divide_percent": 0.45,
        "is_prepayment": 0,
        "channel_id": 76,
        "store_contacter": "王麻子",
        "store_mobile": "13788887779",
        "store_addr": "天府新区",
        "store_name": "武大郎炊饼",
        "store_type": 0,
     }
     headers = {'cookie': 'sessionid=85aeb24b-04ba-47ed-975b-ba763fc1b2a4'}
     ret = client.post('/channel_op/v1/api/store_create', send, headers=headers)
     log.info(ret)


def test_chn_change():
     SERVER   = [{'addr':('127.0.0.1', 8083), 'timeout':20},]
     client = HttpClient(SERVER, client_class = RequestsClient)
     send = {
        "se_userid": 1000,
        "userid": 1129,

        "login_name": "13788889999",
        "nick_name": "张三",
        "phone_num": "13788889999",
        "email": "lanwenhong@xxx.com",
        "org_code": "xxxxxx1111111111",
        "license_id": "xxxxxx11111111111", 
        "legal_person": "李四",
        "business": "大富豪",
        "front_business": "岁月",
        "account_name": "天天",
        "bank_name": "建设银行",
        "bank_account": "78878878787878787878",
        "contact_name": "天天",
        "contact_phone": "15882895989",
        "contact_email": "lanwenhong@xxxx.com",
        "address": "成都天府新区",
        "training_amt_per": 30,
        "divide_percent": 0.65,
        "is_prepayment": 0,
        "channel_name": "牛逼渠道",
     }
     headers = {'cookie': 'sessionid=85aeb24b-04ba-47ed-975b-ba763fc1b2a4'}
     ret = client.post('/channel_op/v1/api/channel', send, headers=headers)
     log.info(ret)

def test_chan_set_state():
    SERVER   = [{'addr':('127.0.0.1', 8083), 'timeout':20},]
    client = HttpClient(SERVER, client_class = RequestsClient)
    send = {"se_userid": 1000, "userid": 1128, "state": 1}

    headers = {'cookie': 'sessionid=85aeb24b-04ba-47ed-975b-ba763fc1b2a4'}
    ret = client.post('/channel_op/v1/api/channel_set_state', send, headers=headers)
    log.debug(ret)

if __name__ == '__main__':
    #test_login()
    #test_vcode()
    #test_vcode_verify()
    #test_chn_register()
    #test_chn_query()
    #test_chn_change() 
    #test_chan_set_state()
    test_store_register()
