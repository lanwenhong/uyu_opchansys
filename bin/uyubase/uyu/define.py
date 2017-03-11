#coding:utf-8

import os, sys

UYU_OP_OK = 0
UYU_OP_ERR = -1

#订单状态
UYU_ORDER_STATUS_SUCC = 0
UYU_ORDER_STATUS_NEED_CONFIRM = 1
UYU_ORDER_STATUS_CANCEL = 2

#基础用户角色
#渠道用户
UYU_USER_ROLE_CHAN     = 2
#门店用户
UYU_USER_ROLE_STORE    = 3
#医院用户
UYU_USER_ROLE_HOSPITAL = 4
#视光师用户
UYU_USER_ROLE_EYESIGHT = 5
#公司超级管理员
UYU_USER_ROLE_SUPER    = 6

#用户状态
#正常
UYU_USER_STATE_OK = 1
#封禁
UYU_USER_STATE_FORBIDDEN = 2
#注销
UYU_USER_STATE_CANCEL = 3

#用户profile状态
#未审核
UYU_USER_PROFILE_STATE_UNAUDITED = 1
#已经审核
UYU_USER_PROFILE_STATE_AUDITED = 2


#渠道信息状态
#启用
UYU_CHAN_STATUS_OPEN = 0
#关闭
UYU_CHAN_STATUS_CLOSE = 1
UYU_CHAN_MAP = {
    UYU_CHAN_STATUS_OPEN : '启用',
    UYU_CHAN_STATUS_CLOSE : '关闭'
}

#门店状态
#启用
UYU_STORE_STATUS_OPEN = 0
#关闭
UYU_STROE_STATUS_CLOSE = 1
UYU_STORE_STATUS_MAP = {
    UYU_STORE_STATUS_OPEN : '启用',
    UYU_STROE_STATUS_CLOSE : '关闭'
}
#门店角色
#门店
UYU_STORE_ROLE_STORE = 0
#医院
UYU_STORE_ROLE_HOSPITAL = 1
#0 门店, 1 医院

UYU_STORE_ROLE_MAP = {
    UYU_STORE_ROLE_STORE: '门店',
    UYU_STORE_ROLE_HOSPITAL: '医院'
}

#系统角色
UYU_SYS_ROLE_OP = 0
UYU_SYS_ROLE_CHAN = 1
UYU_SYS_ROLE_STORE = 2


#使用权限定义
PERMISSION_CHECK = {
    UYU_SYS_ROLE_OP: (UYU_USER_ROLE_SUPER, ),
    UYU_SYS_ROLE_CHAN: (UYU_USER_ROLE_STORE, UYU_USER_ROLE_HOSPITAL),
    UYU_SYS_ROLE_STORE: (UYU_USER_ROLE_STORE,),
}


#业务操作类型busicd
#公司送训练点数给渠道
BUSICD_ORG_ALLOT_TO_CHAN = "000000"
#渠道向公司购买训练点数业务CD
BUSICD_CHAN_BUY_TRAING_TIMES = "000010"
#渠道分配训练点数给门店
BUSICD_CHAN_ALLOT_TO_STORE = "000020"
#门店分配训练点数给消费者
BUSICD_CHAN_ALLOT_TO_COSUMER = "000030"

#订单类型
#分配
UYU_ORDER_TYPE_ALLOT = 0
#购买
UYU_ORDER_TYPE_BUY = 1

UYU_ORDER_TYPE_MAP = {
    UYU_ORDER_TYPE_BUY: '购买',
    UYU_ORDER_TYPE_ALLOT: '分配',
}

#订单支付方式
#支付宝
UYU_ORDER_PAY_TYPE_ALIPAY  = 0
#微信
UYU_ORDER_PAY_TYPE_WCHART  = 1
#线下
UYU_ORDER_PAY_TYPE_OFFLINE = 2

UYU_ORDER_PAY_TYPE_MAP = {
    UYU_ORDER_PAY_TYPE_ALIPAY: '支付宝',
    UYU_ORDER_PAY_TYPE_WCHART: '微信',
    UYU_ORDER_PAY_TYPE_OFFLINE: '支付宝'
}

