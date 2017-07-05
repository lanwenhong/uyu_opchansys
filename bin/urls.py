# -*- coding: utf-8 -*-
from handler import ping
from handler import login
from handler import index
from handler import overview
from handler import channel
from handler import store
from handler import device
from handler import train
from handler import settle
from handler import eyesight
from handler import rules
from handler import user
from handler import vcode
urls = (
    ('/ping', ping.Ping),
    # 登录页面
    ('^/channel_op/v1/page/login.html$', login.Login),
    ('^/channel_op/v1/page/index.html$', index.Index),
    # 总览页面
    ('^/channel_op/v1/page/overview.html$', overview.OverView),
    # 渠道页面
    ('^/channel_op/v1/page/channel.html$', channel.ChannelManage),
    # 门店页面
    ('^/channel_op/v1/page/store.html$', store.StoreManage),
    # 设备页面
    ('^/channel_op/v1/page/device.html$', device.DeviceManage),
    # 训练管理页面
    ('^/channel_op/v1/page/train/buyer.html$', train.TrainBuyerManage),
    # 训练使用页面
    ('^/channel_op/v1/page/train/use.html$', train.TrainUseManage),
    # 清算信息页面
    ('^/channel_op/v1/page/settle.html$', settle.SettleManage),
    # 用户管理页面
    ('^/channel_op/v1/page/users.html$', user.UserManage),
    # 验证码信息页面
    ('^/channel_op/v1/page/vcode.html$', vcode.VerifyCodeManage),
    # 套餐管理页面
    ('^/channel_op/v1/page/rule.html$', rules.RuleManage),

    # 登录接口
    ('^/channel_op/v1/api/login$', login.LoginHandler),
    # 发送验证码接口
    ('^/channel_op/v1/api/sms_send$', login.SmsHandler),
    # 修改密码接口
    ('^/channel_op/v1/api/passwd_change$', login.ChangePassHandler),

    # 渠道API
    # 新建渠道接口
    ('^/channel_op/v1/api/channel_create$', channel.CreateChanHandler),
    # 获取渠道信息和修改渠道信息接口
    ('^/channel_op/v1/api/channel$', channel.ChanHandler),
    # 设置渠道状态接口
    ('^/channel_op/v1/api/channel_set_state', channel.ChanStateSetHandler),
    # 获取渠道数据列表接口
    ('^/channel_op/v1/api/chninfo_pagelist$', channel.ChannelInfoHandler),
    # 获取有效渠道名称列表接口
    ('^/channel_op/v1/api/chan_name_list$', channel.ChanNameList),
    # 获取渠道和对应门店名称列表接口
    ('^/channel_op/v1/api/chan_store_list$', channel.ChanStoreMap),
    # 获取渠道对应绑定套餐的数据
    ('^/channel_op/v1/api/chan_rule_info$', channel.ChanRuleInfoHandler),

    # 门店API
    # 设置门店状态接口
    ('^/channel_op/v1/api/store_set_state', store.StoreStateSetHandler),
    # 新建门店接口
    ('^/channel_op/v1/api/store_create$', store.CreateStoreHandler),
    # 获取门店信息和修改门店信息接口
    ('^/channel_op/v1/api/store$', store.StoreHandler),
    # 获取门店数据接口
    ('^/channel_op/v1/api/storeinfo_pagelist$', store.StoreInfoHandler),
    # 门店绑定视光师接口
    ('^/channel_op/v1/api/store_eye$', store.StoreEyeHandler),
    # 获取有效门店名称接口
    ('^/channel_op/v1/api/store_name_list$', store.StoreNameListHandler),
    # 获取渠道和门店数量统计接口
    ('^/channel_op/v1/api/chan_store_total$', overview.OverViewInfoHandler),

    # 获取设备数量接口
    ('^/channel_op/v1/api/devinfo_pagelist$', device.DeviceInfoHandler),
    # 获取训练操作记录接口
    ('^/channel_op/v1/api/training_op_list$', train.TrainBuyInfoHandler),
    # 获取训练使用记录接口
    ('^/channel_op/v1/api/training_use_list$', train.TrainUseInfoHandler),

    # 视光师
    # 获取视光师信息接口
    ('^/channel_op/v1/api/eyesight_info$', eyesight.EyeSightInfoHandler),
    # 注册视光师接口
    ('^/channel_op/v1/api/register_eye$', eyesight.EyeRegisterHandler),

    # 训练订单
    # 公司分配点数给渠道接口
    ('^/channel_op/v1/api/org_allot_to_chan_order$', train.OrgAllotToChanOrderHandler),
    # 渠道分配点数给门店接口
    ('^/channel_op/v1/api/org_allot_to_store_order$', train.OrgAllotToStoreOrderHandler),
    # 订单撤销接口
    ('^/channel_op/v1/api/order_cancel$', train.OrderCancelHandler),
    # 订单确认接口
    ('^/channel_op/v1/api/order_confirm$', train.OrderConfirmHandler),
    # 平台分配点数给消费者或者视光师
    ('^/channel_op/v1/api/platform_allocate_user$', train.OrgAllocateToUserHandler),

    # 设备
    # 新建设备接口
    ('^/channel_op/v1/api/create_device$', device.DeviceCreateHandler),
    # 分配设备接口
    ('^/channel_op/v1/api/allocate_device$', device.DeviceAllocateHandler),
    # 修改设备信息接口
    ('^/channel_op/v1/api/edit_device$', device.DeviceEditHandler),

    # 结算数据接口
    ('^/channel_op/v1/api/settle_list$', settle.SettleInfoHandler),

    # 套餐规则
    ('^/channel_op/v1/api/rules_list$', rules.RulesInfoHandler),
    # 套餐页面数据
    ('^/channel_op/v1/api/ruleinfo_pagelist$', rules.RulePageHandler),
    # 新建套餐
    ('^/channel_op/v1/api/rule_create$', rules.RuleCreateHandler),
    # 单个套餐数据
    ('^/channel_op/v1/api/rule$', rules.RuleSingleHandler),
    # 修改套餐
    ('^/channel_op/v1/api/rule_edit$', rules.RuleEditHandler),

    # 用户数据
    ('^/channel_op/v1/api/user_list$', user.UserInfoListHandler),
    # 验证码数据
    ('^/channel_op/v1/api/verify_codes_list$', vcode.VerifyCodeInfoListHandler),
    # 用户管理页面修改密码
    ('^/channel_op/v1/api/user_change_password$', user.UserChangePasswordHandler),
)
