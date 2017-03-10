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
urls = (
    ('/ping', ping.Ping),
    #页面
    ('^/channel_op/v1/page/login.html$', login.Login),
    ('^/channel_op/v1/page/index.html$', index.Index),
    ('^/channel_op/v1/page/overview.html$', overview.OverView),
    ('^/channel_op/v1/page/channel.html$', channel.ChannelManage),
    ('^/channel_op/v1/page/store.html$', store.StoreManage),
    ('^/channel_op/v1/page/device.html$', device.DeviceManage),
    ('^/channel_op/v1/page/train/buyer.html$', train.TrainBuyerManage),
    ('^/channel_op/v1/page/train/use.html$', train.TrainUseManage),
    ('^/channel_op/v1/page/settle.html$', settle.SettleManage),
    #api
    ('^/channel_op/v1/api/login$', login.LoginHandler),
    ('^/channel_op/v1/api/sms_send$', login.SmsHandler),
    ('^/channel_op/v1/api/passwd_change$', login.ChangePassHandler),

    #渠道API
    ('^/channel_op/v1/api/channel_create$', channel.CreateChanHandler),
    ('^/channel_op/v1/api/channel$', channel.ChanHandler),
    ('^/channel_op/v1/api/channel_set_state', channel.ChanStateSetHandler),
    ('^/channel_op/v1/api/chninfo_pagelist$', channel.ChannelInfoHandler),
    
    #门店API
    ('^/channel_op/v1/api/store_set_state', store.StoreStateSetHandler),
    ('^/channel_op/v1/api/store_create$', store.CreateStoreHandler),
    ('^/channel_op/v1/api/store$', store.StoreHandler),
    ('^/channel_op/v1/api/storeinfo_pagelist$', store.StoreInfoHandler),


    ('^/channel_op/v1/api/devinfo_pagelist$', device.DeviceInfoHandler),
    ('^/channel_op/v1/api/training_op_list$', train.TrainBuyInfoHandler),
    ('^/channel_op/v1/api/training_use_list$', train.TrainUseInfoHandler),
    #('^/channel_op/v1/api/channel$', channel.ChannelHandler),
    ('^/channel_op/v1/api/chan_store_total$', overview.OverViewInfoHandler),
)
