#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from flask import render_template

from . import main
from kubernetes import client

CHARSET = os.environ.get('CHARSET') or 'utf-8'
reload(sys)
sys.setdefaultencoding(CHARSET)


@main.route('/')
def index():

    return render_template('index.html')


@main.route('/get_main')
def get_main():
    return render_template('main.html')


@main.route('/get_pods', methods=['GET'])
def get_pods():
    pod_list = []
    pod_dict = {}
    kclient = client.CoreV1Api()

    result = kclient.list_pod_for_all_namespaces(watch=False)
    for item in result.items:
        pod_dict['pod_name'] = item.metadata.name
        pod_dict['pod_namespace'] = item.metadata.namespace
        pod_dict['pod_phase'] = item.status.phase
        pod_list.append(pod_dict)
        pod_dict = {}
    return render_template('pod.html', pod_list=pod_list)


@main.route('/get_nodes', methods=['GET'])
def get_nodes():
    node_list = []
    node_dict = {}
    kclient = client.CoreV1Api()
    result = kclient.list_node()
    for item in result.items:
        node_dict['node_id'] = item.metadata.uid
        node_dict['node_name'] = item.metadata.name
        conditions = item.status.conditions
        for pressure in conditions:
            if pressure.type == 'Ready':
                node_dict['node_status'] = pressure.status
        node_dict['node_cpu_capacity'] = item.status.capacity['cpu']
        node_dict['node_memory_capacity'] = item.status.capacity['memory']
        node_dict['node_cpu_allocatable'] = item.status.allocatable['cpu']
        node_dict['node_memory_allocatable'] = item.status.allocatable['memory']
        print(item.metadata.creation_timestamp)
        print type(item.metadata.creation_timestamp)



        node_dict['node_age'] = item.metadata.creation_timestamp

        node_list.append(node_dict)
        node_dict = {}

    return render_template('node.html', node_list=node_list)


