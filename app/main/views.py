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
        node_dict['node_name'] = item.metadata.name
        node_dict['node_status'] = item.status.conditions.last_heartbeat_time[-1].type
        node_dict['node_cpu_capacity'] = item.status.capacity.cpu
        node_dict['node_memory_capacity'] = item.status.capacity.memory


