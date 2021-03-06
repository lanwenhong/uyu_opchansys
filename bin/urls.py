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
    ('/channel_op/v1/page/login.html', login.Login),
    ('/channel_op/v1/page/index.html', index.Index),
    ('/channel_op/v1/page/overview.html', overview.OverView),
    ('/channel_op/v1/page/channel.html', channel.ChannelManage),
    ('/channel_op/v1/page/store.html', store.StoreManage),
    ('/channel_op/v1/page/device.html', device.DeviceManage),
    ('/channel_op/v1/page/train/buyer.html', train.TrainBuyerManage),
    ('/channel_op/v1/page/train/use.html', train.TrainUseManage),
    ('/channel_op/v1/page/settle.html', settle.SettleManage),
)
