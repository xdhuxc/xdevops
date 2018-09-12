#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template
from ..main import main

from kubernetes import client
from kubernetes import config


@main.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@main.route('/pod')
def manage_pod():
    client.Configuration.host = '172.20.26.150'

    v1 = client.CoreV1Api()
    ret = v1.list_pod_for_all_namespaces(watch=False)
    for item in ret.items():
        print(item)
    return render_template('pod.html')
