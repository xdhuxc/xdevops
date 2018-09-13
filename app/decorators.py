#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wanghuan
# date: 2018-09-09
# description:

from functools import wraps
import os
import requests

# 多个装饰器执行的顺序就是从最后一个装饰器开始，执行到第一个装饰器，再执行函数本身。

basedir = os.path.abspath(os.path.dirname(__file__))


def cert_required():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            with requests.Session() as s:
                s.cert = (os.path.join(basedir, 'main/certificate/apiserver-kubelet-client.crt'),
                           os.path.join(basedir, 'main/certificate/apiserver-kubelet-client.key'))
                s.verify = os.path.join(basedir, 'main/certificate/ca.crt')
            return f(s, *args, **kwargs)
        return decorated_function
    return decorator

