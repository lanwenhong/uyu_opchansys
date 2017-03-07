# -*- coding: utf-8 -*-

def gen_ret_range(page, maxnum):
    start = maxnum * page - maxnum
    end = start + maxnum
    return start, end

