#!/usr/bin/env python
# -*- coding: utf-8 -*-


from flask import render_template

from . import main
from kubernetes import client


@main.route('/')
def index():

    return render_template('index.html')


@main.route('/get_pods', methods=['GET'])
def get_pods():
    pod_list = []
    pod_dict = {}
    v1 = client.CoreV1Api()

    result = v1.list_pod_for_all_namespaces(watch=False)
    for item in result.items:
        pod_dict['pod_name'] = item.metadata.name
        pod_dict['pod_namespace'] = item.metadata.namespace
        pod_dict['pod_phase'] = item.status.phase

        containers = item.status.container_statuses


        if item.metadata.name == 'kube-dns-v8-9wxkw':
            print(item)
        print(item.status.pod_ip)
        print(item.metadata.namespace)
        print(item.metadata.name)
    return render_template('pod.html')


