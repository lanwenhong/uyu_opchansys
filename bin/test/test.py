#coding: utf-8

import json
import hashlib
import unittest
from zbase.base import logger
from zbase.base.http_client import RequestsClient
from zbase.server.client import HttpClient

log = logger.install('stdout')

class TestUyuChannelOp(unittest.TestCase):

    def setUp(self):
        self.url = ''
        self.send = {}
        self.host = '127.0.0.1'
        self.port = 8084
        self.timeout = 2000
        self.server = [{'addr':(self.host, self.port), 'timeout':self.timeout},]
        self.client = HttpClient(self.server, client_class = RequestsClient)
        self.headers = {'cookie': 'sessionid=92b852a9-04fc-4fb1-8fb4-e3901b52557e'}


    @unittest.skip("skipping")
    def test_login(self):
        self.url = '/channel_op/v1/api/login'
        self.send = {
            "mobile": "13802438716",
            "password": hashlib.md5("12345678").hexdigest()
        }
        ret = self.client.post(self.url, self.send)
        log.info(ret)
        print '--headers--'
        print self.client.client.headers
        respcd = json.loads(ret).get('respcd')
        self.assertEqual(respcd, '0000')


    @unittest.skip("skipping")
    def test_vcode(self):
        self.url = '/channel_op/v1/api/sms_send'
        self.send = {"mobile": "18215630018"}
        ret = self.client.post(self.url, self.send)
        log.info(ret)
        respcd = json.loads(ret).get('respcd')
        self.assertEqual(respcd, '0000')


    #@unittest.skip("skipping")
    def test_vcode_verify(self):
        self.url = '/channel_op/v1/api/passwd_change'
        self.send = {
            "mobile": "18215630018",
            "vcode":"1493",
            "password": hashlib.md5("12345678").hexdigest()
        }
        ret = self.client.post(self.url, self.send)
        log.info(ret)
        respcd = json.loads(ret).get('respcd')
        self.assertEqual(respcd, '0000')


    @unittest.skip("skipping")
    def test_chn_query(self):
        self.url = '/channel_op/v1/api/channel'
        self.send = {"userid": 1562, "se_userid": 1262}
        ret = self.client.get(self.url, self.send, headers=self.headers)
        log.debug(ret)
        respcd = json.loads(ret).get('respcd')
        self.assertEqual(respcd, '0000')


    @unittest.skip("skipping")
    def test_chn_register(self):
         self.url = '/channel_op/v1/api/channel_create'
         self.send = {
            "se_userid": 1262,

            "login_name": "14789897655",
            "nick_name": "张四",
            "phone_num": "14789897655",
            "channel_name": "渠道655",
            "email": "wende@xxx.com",
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
            "contact_email": "wende@xxxx.com",
            "address": "成都天府新区",
            "training_amt_per": 100,
            "divide_percent": 0.45,
            "is_prepayment": 0,
         }
         ret = self.client.post(self.url, self.send, headers=self.headers)
         log.info(ret)
         respcd = json.loads(ret).get('respcd')
         self.assertEqual(respcd, '0000')


    @unittest.skip("skipping")
    def test_store_register(self):
         self.url = '/channel_op/v1/api/store_create'
         self.send = {
            "se_userid": 1262,

            "login_name": "13988888880",
            "phone_num": "13988888880",
            "channel_name": "渠道8880",
            "email": "brook@xxx.com",
            "org_code": "xxxxxx1111111111",
            "license_id": "xxxxxx11111111111",
            "legal_person": "李四",
            "business": "大富豪",
            "front_business": "岁月",
            "account_name": "天天",
            "bank_name": "建设银行",
            "bank_account": "78878878787878787878",
            "contact_name": "天天",
            "contact_phone": "15882895990",
            "contact_email": "brook@xxxx.com",
            "address": "成都天府新区",

            "training_amt_per": 100,
            "divide_percent": 0.45,
            "is_prepayment": 0,
            "channel_id": 76,
            "store_contacter": "王麻子",
            "store_mobile": "15882895990",
            "store_addr": "天府新区",
            "store_name": "BrookCook",
            "store_type": 0,
         }
         ret = self.client.post(self.url, self.send, headers=self.headers)
         log.info(ret)
         respcd = json.loads(ret).get('respcd')
         self.assertEqual(respcd, '0000')


    @unittest.skip("skipping")
    def test_chn_change(self):
         self.url = '/channel_op/v1/api/channel'
         self.send = {
            "se_userid": 1262,
            "userid": 51563,

            "login_name": "14789897656",
            "nick_name": "张三",
            "phone_num": "14789897656",
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
         ret = self.client.post(self.url, self.send, headers=self.headers)
         log.info(ret)
         respcd = json.loads(ret).get('respcd')
         self.assertEqual(respcd, '0000')


    @unittest.skip("skipping")
    def test_store_change(self):
         self.url = '/channel_op/v1/api/store'
         self.send = {
            "se_userid": 1262,
            "userid": 51564,

            "login_name": "13988888881",
            "phone_num": "13988888881",
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
            "contact_phone": "15882895990",
            "contact_email": "lanwenhong@xxxx.com",
            "address": "成都天府新区",

            "training_amt_per": 100,
            "divide_percent": 0.95,
            "is_prepayment": 0,
            "channel_id": 104,
            "store_contacter": "王麻子",
            "store_mobile": "13988888880",
            "store_addr": "天府新区",
            "store_name": "BrookCook",
            "store_type": 0,
         }
         ret = self.client.post(self.url, self.send, headers=self.headers)
         log.info(ret)
         respcd = json.loads(ret).get('respcd')
         self.assertEqual(respcd, '0000')


    @unittest.skip("skipping")
    def test_chan_set_state(self):
        self.url = '/channel_op/v1/api/channel_set_state'
        self.send = {"se_userid": 1262, "userid": 51563, "state": 1}
        ret = self.client.post(self.url, self.send, headers=self.headers)
        log.debug(ret)
        respcd = json.loads(ret).get('respcd')
        self.assertEqual(respcd, '0000')


    @unittest.skip("skipping")
    def test_channel_list(self):
        self.url = '/channel_op/v1/api/chninfo_pagelist'
        self.send = {
            "se_userid": 1262,
            "page": 1,
            "maxnum": 10,
            # "channel_name": "",
            # "phone_num": "",
            # "is_prepayment": 0,
            # "is_valid": 0
        }
        ret = self.client.get(self.url, self.send, headers=self.headers)
        log.debug(ret)
        respcd = json.loads(ret).get('respcd')
        self.assertEqual(respcd, '0000')


    @unittest.skip("skipping")
    def test_store_list(self):
        self.url = '/channel_op/v1/api/storeinfo_pagelist'
        self.send = {
            "se_userid": 1262,
            "page": 1,
            "maxnum": 10,
            # "channel_name": "",
            # "store_name": "",
            # "is_valid": 0
        }
        ret = self.client.get(self.url, self.send, headers=self.headers)
        log.debug(ret)
        respcd = json.loads(ret).get('respcd')
        self.assertEqual(respcd, '0000')


    @unittest.skip("skipping")
    def test_device_list(self):
        self.url = '/channel_op/v1/api/devinfo_pagelist'
        self.send = {
            "se_userid": 1262,
            "page": 1,
            "maxnum": 10,
            # "channel_name": "",
            # "store_name": "",
            # "serial_number": "",
            # "status": 0
        }
        ret = self.client.get(self.url, self.send, headers=self.headers)
        log.debug(ret)
        respcd = json.loads(ret).get('respcd')


    @unittest.skip("skipping")
    def test_store_set_state(self):
        self.url = '/channel_op/v1/api/store_set_state'
        self.send = {"se_userid": 1262, "userid": 51564, "state": 1}
        ret = self.client.post(self.url, self.send, headers=self.headers)
        log.debug(ret)
        respcd = json.loads(ret).get('respcd')
        self.assertEqual(respcd, '0000')


    @unittest.skip("skipping")
    def test_store_query(self):
        self.url = '/channel_op/v1/api/store'
        self.send = {"userid": 51564, "se_userid": 1262}
        ret = self.client.get(self.url, self.send, headers=self.headers)
        log.debug(ret)
        respcd = json.loads(ret).get('respcd')
        self.assertEqual(respcd, '0000')


    @unittest.skip("skipping")
    def test_bind_eyesight(self):
        self.url = '/channel_op/v1/api/store_eye'
        self.send = {
            # "userid": 1229, #视光师ok
            # "userid": 1199, #消费者ok
            "userid": 1197, #门店fail
            "store_id": 78,
            "channel_id": 104,
            "se_userid": 1262
        }
        ret = self.client.post(self.url, self.send, headers=self.headers)
        log.debug(ret)
        respcd = json.loads(ret).get('respcd')
        self.assertEqual(respcd, '0000')


    @unittest.skip("skipping")
    def test_query_eyesight_info(self):
        self.url = '/channel_op/v1/api/store_eye'
        self.send = {
            "se_userid": 1262,
            #"phone_num": "13475481267"  #视光师ok
            # "phone_num": "13100000001"  #消费者ok
            "phone_num": "13000000003"  #门店fail
        }
        ret = self.client.get(self.url, self.send, headers=self.headers)
        log.debug(ret)
        respcd = json.loads(ret).get('respcd')
        self.assertEqual(respcd, '0000')


    @unittest.skip("skipping")
    def test_channel_name_list(self):
        self.url = '/channel_op/v1/api/chan_name_list'
        self.send = {"se_userid": 1262}
        ret = self.client.get(self.url, self.send, headers=self.headers)
        log.debug(ret)
        respcd = json.loads(ret).get('respcd')
        self.assertEqual(respcd, '0000')


    @unittest.skip("skipping")
    def test_channel_store_map(self):
        self.url = '/channel_op/v1/api/chan_store_list'
        self.send = {
            "se_userid": 1262,
            "channel_id": 104
        }
        ret = self.client.get(self.url, self.send, headers=self.headers)
        log.debug(ret)
        respcd = json.loads(ret).get('respcd')
        self.assertEqual(respcd, '0000')


    @unittest.skip("skipping")
    def test_store_name_list(self):
        self.url = '/channel_op/v1/api/store_name_list'
        self.send = {"se_userid": 1262}
        ret = self.client.get(self.url, self.send, headers=self.headers)
        log.debug(ret)
        respcd = json.loads(ret).get('respcd')
        self.assertEqual(respcd, '0000')


    #@unittest.skip("skipping")
    #def test_chan_buy_order(self):
    #    self.url = "/channel_op/v1/api/chan_buy_order"
    #    self.send = {
    #        "se_userid": 1000,
    #        "busicd": "000010",
    #        "channel_id": 37,
    #        "training_times": 19,
    #        "training_amt": 19,
    #        'ch_training_amt_per': 1
    #    }
    #    headers = {'cookie': 'sessionid=85aeb24b-04ba-47ed-975b-ba763fc1b2a4'}
    #    ret = self.client.post(self.url, self.send, headers=headers)
    #    respcd = json.loads(ret).get('respcd')
    #    self.assertEqual(respcd, '0000')


    @unittest.skip("skipping")
    def test_org_allot_to_chan_order(self):
        self.url = "/channel_op/v1/api/org_allot_to_chan_order"
        self.send = {
            "se_userid": 1262,
            "busicd": "ORG_ALLOT_TO_CHAN",
            "channel_id": 104,
            "rule_id": 1,
            "training_times": 500,
            "training_amt": 2000000,
            "ch_training_amt_per": 30,
            "remark": "给104渠道分套餐A",
        }
        ret = self.client.post(self.url, self.send, headers=self.headers)
        respcd = json.loads(ret).get('respcd')
        self.assertEqual(respcd, '0000')


    @unittest.skip("skipping")
    def test_org_allot_to_store_order(self):
        self.url = "/channel_op/v1/api/org_allot_to_store_order"
        self.send = {
            "se_userid": 1262,
            "busicd": "CHAN_ALLOT_TO_STORE",
            "channel_id": 104,
            "store_id": 78,
            "training_times": 18,
            "training_amt": 18 * 100,
            'store_training_amt_per': 100
        }
        ret = self.client.post(self.url, self.send, headers=self.headers)
        respcd = json.loads(ret).get('respcd')
        self.assertEqual(respcd, '0000')


    @unittest.skip("skipping")
    def test_order_cancel(self):
        self.url = "/channel_op/v1/api/order_cancel"
        self.send = {
            "se_userid": 1262,
            "order_no": "2017041401586142"
        }
        ret = self.client.post(self.url, self.send, headers=self.headers)
        log.debug(ret)
        respcd = json.loads(ret).get('respcd')
        self.assertEqual(respcd, '0000')


    @unittest.skip("skipping")
    def test_order_confirm(self):
        self.url = "/channel_op/v1/api/order_confirm"
        self.send = {
            "se_userid": 1262,
            "order_no": "2017041501586143"
        }
        ret = self.client.post(self.url, self.send, headers=self.headers)
        log.debug(ret)
        respcd = json.loads(ret).get('respcd')
        self.assertEqual(respcd, '0000')


    @unittest.skip("skipping")
    def test_create_device(self):
        self.url = "/channel_op/v1/api/create_device"
        self.send = {
            "se_userid": 1262,
            "device_name": "设备_0414",
            "hd_version": "hd_v1",
            "blooth_tag": "bt_v1",
            "scm_tag": "sm_v1",
            "status": 0
        }
        ret = self.client.post(self.url, self.send, headers=self.headers)
        log.debug(ret)
        respcd = json.loads(ret).get('respcd')
        self.assertEqual(respcd, '0000')


    @unittest.skip("skipping")
    def test_allocate_device(self):
        self.url = "/channel_op/v1/api/allocate_device"
        self.send = {
            "se_userid": 1262,
            "serial_number": 145,
            "channel_id": 104,
            "store_id": 78
        }
        ret = self.client.post(self.url, self.send, headers=self.headers)
        log.debug(ret)
        respcd = json.loads(ret).get('respcd')
        self.assertEqual(respcd, '0000')


    @unittest.skip("skipping")
    def test_edit_device(self):
        self.url = "/channel_op/v1/api/edit_device"
        self.send = {
            "se_userid": 1262,
            "device_name": "设备_0414",
            "hd_version": "hd_v1.1",
            "blooth_tag": "bt_v1.1",
            "scm_tag": "sm_v1.1",
            "status": 0,
            "serial_number": 145
        }
        ret = self.client.post(self.url, self.send, headers=self.headers)
        log.debug(ret)
        respcd = json.loads(ret).get('respcd')
        self.assertEqual(respcd, '0000')



    @unittest.skip("skipping")
    def test_settle_list(self):
        self.url = "/channel_op/v1/api/settle_list"
        self.send = {
            "se_userid": 1262,
            "page": 1,
            "maxnum": 10,
            "channel_name": "四川渠道",
            # "store_name": "",
            # "start_time": "",
        }
        ret = self.client.get(self.url, self.send, headers=self.headers)
        log.debug(ret)
        respcd = json.loads(ret).get('respcd')
        self.assertEqual(respcd, '0000')


    @unittest.skip("skipping")
    def test_train_op_list(self):
        self.url = "/channel_op/v1/api/training_op_list"
        self.send = {
            "se_userid": 1262,
            "page": 1,
            "maxnum": 10,
            # "channel_name": "四川渠道",
            # "store_name": "",
            # "consumer_id": "",
            # "start_time": "",
            # "end_time": "",
            # "status": "",
        }
        ret = self.client.get(self.url, self.send, headers=self.headers)
        log.debug(ret)
        respcd = json.loads(ret).get('respcd')
        self.assertEqual(respcd, '0000')


    @unittest.skip("skipping")
    def test_train_use_list(self):
        self.url = "/channel_op/v1/api/training_use_list"
        self.send = {
            "se_userid": 1262,
            "page": 1,
            "maxnum": 10,
            # "channel_name": "四川渠道",
            # "store_name": "",
            # "consumer_id": "",
            # "eyesight": "",
            # "create_time": "",
        }
        ret = self.client.get(self.url, self.send, headers=self.headers)
        log.debug(ret)
        respcd = json.loads(ret).get('respcd')
        self.assertEqual(respcd, '0000')



    @unittest.skip("skipping")
    def test_rules_list(self):
        self.url = "/channel_op/v1/api/rules_list"
        self.send = {
            "se_userid": 1262,
        }
        ret = self.client.get(self.url, self.send, headers=self.headers)
        log.debug(ret)
        respcd = json.loads(ret).get('respcd')
        self.assertEqual(respcd, '0000')


    @unittest.skip("skipping")
    def test_channel_store_stat(self):
        self.url = "/channel_op/v1/api/chan_store_total"
        self.send = {
            "se_userid": 1262,
        }
        ret = self.client.get(self.url, self.send, headers=self.headers)
        log.debug(ret)
        respcd = json.loads(ret).get('respcd')
        self.assertEqual(respcd, '0000')


    @unittest.skip("skipping")
    def test_store_bind_eyesight_info_list(self):
        self.url = "/channel_op/v1/api/eyesight_info"
        self.send = {
            "se_userid": 1262,
            "channel_id": 104,
            "store_id": 78,
            "userid": 51564
        }
        ret = self.client.get(self.url, self.send, headers=self.headers)
        log.debug(ret)
        respcd = json.loads(ret).get('respcd')
        self.assertEqual(respcd, '0000')


    @unittest.skip("skipping")
    def test_store_unbind_eyesight(self):
        self.url = "/channel_op/v1/api/eyesight_info"
        self.send = {
            "se_userid": 1262,
            "channel_id": 104,
            "store_id": 78,
            "userid": 1227
        }
        ret = self.client.post(self.url, self.send, headers=self.headers)
        log.debug(ret)
        respcd = json.loads(ret).get('respcd')
        self.assertEqual(respcd, '0000')


    @unittest.skip("skipping")
    def test_register_eyesight(self):
        self.url = "/channel_op/v1/api/register_eye"
        self.send = {
            "se_userid": 1262,
            "mobile": "13928478194",
            "nick_name": "视光师8194",
            "username": "wende8914",
            "email": "wende8914@ccc.com"
        }
        ret = self.client.post(self.url, self.send, headers=self.headers)
        log.debug(ret)
        respcd = json.loads(ret).get('respcd')
        self.assertEqual(respcd, '0000')



suite = unittest.TestLoader().loadTestsFromTestCase(TestUyuChannelOp)
unittest.TextTestRunner(verbosity=2).run(suite)
