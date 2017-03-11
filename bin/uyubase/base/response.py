#coding:utf-8
import datetime
import logging
try:
    import simplejson as json
except ImportError:
    import json


class UAURET:
    OK                  = "0000"
    DBERR               = "2000"
    THIRDERR            = "2001"
    SESSIONERR          = "2002"
    DATAERR             = "2003"
    IOERR               = "2004"
    LOGINERR            = "2100"
    PARAMERR            = "2101"
    USERERR             = "2102"
    ROLEERR             = "2103"
    PWDERR              = "2104"
    REQERR              = "2200"
    IPERR               = "2201"
    NODATA              = "2300"
    DATAEXIST           = "2301"
    UNKOWNERR           = "2400"
    SERVERERR           = "2600"
    METHODERR           = "2601"
    VCODEERR            = "1000"
    REGISTERERR         = "1001"
    CHANGECHANERR       = "1002"
    CHANGESTOREERR      = "1003"
    USERROLEERR         = "1004"
    ORDERERR            = "1005"

error_map = {
    UAURET.OK                    : u"成功",
    UAURET.DBERR                 : u"数据库查询错误",
    UAURET.THIRDERR              : u"第三方系统错误",
    UAURET.SESSIONERR            : u"用户未登录",
    UAURET.DATAERR               : u"数据错误",
    UAURET.IOERR                 : u"文件读写错误",
    UAURET.LOGINERR              : u"用户登录失败",
    UAURET.PARAMERR              : u"参数错误",
    UAURET.USERERR               : u"用户不存在或未激活",
    UAURET.ROLEERR               : u"用户身份错误",
    UAURET.PWDERR                : u"密码错误",
    UAURET.REQERR                : u"非法请求或请求次数受限",
    UAURET.IPERR                 : u"IP受限",
    UAURET.NODATA                : u"无数据",
    UAURET.DATAEXIST             : u"数据已存在",
    UAURET.UNKOWNERR             : u"未知错误",
    UAURET.SERVERERR             : u"内部错误",
    UAURET.METHODERR             : u"函数未实现",
    UAURET.VCODEERR              : u"验证码错误",
    UAURET.REGISTERERR           : u"用户注册失败",
    UAURET.CHANGECHANERR         : u"更新渠道信息失败",
    UAURET.CHANGESTOREERR        : u"更新门店信息失败",
    UAURET.USERROLEERR           : u"用户身份出错",
    UAURET.ORDERERR              : u"订单操作失败",
}

def json_default_trans(obj):
    '''json对处理不了的格式的处理方法'''
    if isinstance(obj, datetime.datetime):
        return obj.strftime('%Y-%m-%d %H:%M:%S')
    if isinstance(obj, datetime.date):
        return obj.strftime('%Y-%m-%d')
    raise TypeError('%r is not JSON serializable' % obj)


def error(errcode, resperr='', respmsg='', data=None, debug=False, escape=True, encoder=None):
    global error_map
    if not resperr:
        resperr = respmsg if respmsg else error_map[errcode]
    if not data:
        data = {}
    ret = {"respcd": errcode, "respmsg": respmsg, "resperr": resperr, "data": data}
    if debug:
        log.debug('error:%s', ret)
    return json.dumps(ret, ensure_ascii=escape, cls=encoder, separators=(',', ':'), default = json_default_trans)

def success(data, resperr='', debug=False, escape=True, encoder=None):
    ret = {"respcd": "0000", "resperr": resperr, "respmsg": "", "data": data}
    if debug:
        log.debug('success:%s', ret)
    return json.dumps(ret, ensure_ascii=escape, cls=encoder, separators=(',', ':'), default = json_default_trans)
