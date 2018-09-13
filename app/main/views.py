#!/usr/bin/env python
# -*- coding: utf-8 -*-


import requests
import os


basedir = os.path.abspath(os.path.dirname(__file__))


kubernetes_url = 'https://172.20.26.150:6443/api/v1/pods?watch=False'


cert = (os.path.join(basedir, 'certificate/apiserver-kubelet-client.crt'),
                         os.path.join(basedir, 'certificate/apiserver-kubelet-client.key'))
verify = os.path.join(basedir, 'certificate/ca.crt')

resp = requests.get(kubernetes_url, timeout=10, cert=cert, verify=verify)

print(resp)
