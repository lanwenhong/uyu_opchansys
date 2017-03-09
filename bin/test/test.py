#coding: utf-8

from zbase.base import logger
from zbase.base.http_client import RequestsClient
from zbase.server.client import HttpClient

log = logger.install('stdout')


def test_login():
    SERVER   = [{'addr':('127.0.0.1', 8083), 'timeout':20},]
    client = HttpClient(SERVER, client_class = RequestsClient)
    send = {"mobile": "15882895784", "password": "123456"}
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
    send = {"userid": 1100, "se_userid": 1000}
    headers = {'cookie': 'sessionid=85aeb24b-04ba-47ed-975b-ba763fc1b2a4'}
    ret = client.get('/channel_op/v1/api/channel', send, headers=headers)

    log.debug(ret)




def test_chn_register():
     SERVER   = [{'addr':('127.0.0.1', 8083), 'timeout':20},]
     client = HttpClient(SERVER, client_class = RequestsClient)
     send = {
        "se_userid": 1000,

        "login_name": "15782895987",
        "nick_name": "张三",
        "phone_num": "15782895987",
        #"user_type": 2,
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

def test_chn_change():
     SERVER   = [{'addr':('127.0.0.1', 8083), 'timeout':20},]
     client = HttpClient(SERVER, client_class = RequestsClient)
     send = {
        "se_userid": 1000,
        "userid": 1103,
        "login_name": "13456789090",
        "nick_name": "张三",
        "phone_num": "13456789090",
        #"user_type": 2,
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
        "training_amt_per": 59,
        "divide_percent": 0.75,
        "is_prepayment": 0,
     }
     headers = {'cookie': 'sessionid=85aeb24b-04ba-47ed-975b-ba763fc1b2a4'}
     ret = client.post('/channel_op/v1/api/channel', send, headers=headers)
     log.info(ret)


if __name__ == '__main__':
    #test_login()
    #test_vcode()
    #test_vcode_verify()
    #test_create_chan()
    #test_chn_register()
    #test_chn_query()
    test_chn_change() 
