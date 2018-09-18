#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wanghuan
# date: 2018-09-09
# description:

import sys
from kubernetes import config
from kubernetes import client

reload(sys)
sys.setdefaultencoding('utf-8')

config.load_kube_config()

kclient = client.CoreV1Api()


result = kclient.read_namespaced_pod_status('kube-dns-v8-9wxkw', 'kube-system')
print result