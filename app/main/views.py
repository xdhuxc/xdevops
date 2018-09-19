#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from flask import render_template
from flask import request

from . import main
from kubernetes import client

from ..utils import Utils
from .. import kclient

CHARSET = os.environ.get('CHARSET') or 'utf-8'
reload(sys)
sys.setdefaultencoding(CHARSET)


@main.route('/')
def index():

    return render_template('index.html')


@main.route('/main')
def get_main():
    return render_template('main.html')


@main.route('/nodes/<node_name>', methods=['GET'])
def get_node(node_name):
    kclient = client.CoreV1Api()
    result = kclient.read_node(node_name)
    node_dict = {}
    node_dict['node_id'] = result.metadata.uid
    node_dict['node_name'] = result.metadata.name
    conditions = result.status.conditions
    for pressure in conditions:
        if pressure.type == 'Ready':
            node_dict['node_status'] = pressure.status
    node_dict['node_cpu_capacity'] = result.status.capacity['cpu']
    node_dict['node_memory_capacity'] = result.status.capacity['memory'][:-2]
    node_dict['node_cpu_allocatable'] = result.status.allocatable['cpu']
    node_dict['node_memory_allocatable'] = result.status.allocatable['memory'][:-2]
    node_dict['node_age'] = result.metadata.creation_timestamp

    return render_template('node_base.html', node_name=node_name, node=node_dict)


@main.route('/nodes', methods=['GET'])
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
        node_dict['node_memory_capacity'] = item.status.capacity['memory'][:-2]
        node_dict['node_cpu_allocatable'] = item.status.allocatable['cpu']
        node_dict['node_memory_allocatable'] = item.status.allocatable['memory'][:-2]
        node_dict['node_age'] = item.metadata.creation_timestamp

        node_list.append(node_dict)
        node_dict = {}

    return render_template('nodes.html', node_list=node_list)


@main.route('/nodes/<node_name>/pods/')
def get_node_pods(node_name):
    """
    获取指定 node 中的 pod 信息
    :param node_name:
    :return:
    """
    kclient = client.CoreV1Api()
    result = kclient.list_node()
    return render_template('node_pods.html', node_name=node_name)


@main.route('/nodes/<node_name>/specifications')
def get_node_specifications(node_name):
    """
    获取指定 node 的信息
    :param node_name:
    :return:
    """
    node_info = {}
    kclient = client.CoreV1Api()
    result = kclient.read_node_status(node_name)
    system_info = result.status.node_info
    node_info['architecture'] = system_info.architecture
    node_info['boot_id'] = system_info.boot_id
    node_info['container_runtime_version'] = system_info.container_runtime_version
    node_info['kernel_version'] = system_info.kernel_version
    node_info['kube_proxy_version'] = system_info.kube_proxy_version
    node_info['kubelet_version'] = system_info.kubelet_version
    node_info['machine_id'] = system_info.machine_id
    node_info['operating_system'] = system_info.operating_system
    node_info['os_image'] = system_info.os_image
    node_info['system_uuid'] = system_info.system_uuid
    node_info['creation_timestamp'] = result.metadata.creation_timestamp
    node_info['capacity_cpu'] = result.status.capacity['cpu']
    node_info['capacity_memory'] = result.status.capacity['memory'][:-2]
    node_info['capacity_pods'] = result.status.capacity['pods']

    addresses = result.status.addresses

    conditions = result.status.conditions

    return render_template('node_specifications.html', node_name=node_name,
                           node_info=node_info, conditions=conditions, addresses=addresses)


@main.route('/nodes/<node_name>/yaml/', methods=['GET'])
def get_node_yaml(node_name):
    """
    获取指定 node 的 YAML文件。
    :param node_name:
    :return:
    """
    kclient = client.CoreV1Api()
    result = kclient.read_node_status(node_name)
    return render_template('node_yaml.html', node=result, node_name=node_name)


@main.route('/nodes/<node_name>/labels/')
def get_node_labels(node_name):
    """
    获取指定 node 的标签和注解。
    :param node_name:
    :return:
    """
    kclient = client.CoreV1Api()
    result = kclient.read_node_status(node_name)
    labels_dict = result.metadata.labels
    annotations = result.metadata.annotations
    return render_template('node_labels.html', labels=labels_dict, annotations=annotations, node_name=node_name)


@main.route('/nodes/<node_name>/images/')
def get_node_images(node_name):
    """
    从Node的yaml文件中解析出所有镜像，以字典的方式组织，镜像大小直接表现为MB，GB等。
    :param node_name:
    :return:
    """
    images_dict = {}
    kclient = client.CoreV1Api()
    result = kclient.read_node_status(node_name)
    for image in result.status.images:
        for image_name in image.names:
            # 此处用工具函数将字节转换为MB，GB等易读形式。
            images_dict[image_name] = Utils.readable(image.size_bytes)
    return render_template('node_images.html', images=images_dict, node_name=node_name)


@main.route('/pods', methods=['GET'])
def get_pods():
    pod_list = []
    pod_dict = {}
    kclient = client.CoreV1Api()

    result = kclient.list_pod_for_all_namespaces(watch=False)
    for item in result.items:
        pod_dict['pod_name'] = item.metadata.name
        pod_dict['pod_namespace'] = item.metadata.namespace
        pod_dict['pod_phase'] = item.status.phase
        pod_dict['start_time'] = item.status.start_time
        pod_list.append(pod_dict)
        pod_dict = {}
    return render_template('pods.html', pod_list=pod_list)


@main.route('/pod/<pod_namespace>/<pod_name>', methods=['GET'])
def get_pod(pod_namespace, pod_name):
    """
    获取 Pod 基本信息。
    :param pod_namespace:
    :param pod_name:
    :return:
    """
    result = kclient.read_namespaced_pod(pod_name, pod_namespace)
    pod_dict = {}
    pod_dict['pod_name'] = result.metadata.name
    pod_dict['pod_namespace'] = result.metadata.namespace
    pod_dict['pod_phase'] = result.status.phase
    pod_dict['pod_creation_timestamp'] = result.metadata.creation_timestamp
    conditions = result.status.conditions
    for condition in conditions:
        if condition.type == 'Ready':
            pod_dict['pod_status'] = bool(condition.status)
    return render_template('pod_base.html', pod=pod_dict, pod_namespace=pod_namespace, pod_name=pod_name)


@main.route('/pod/<pod_namespace>/<pod_name>/specifications', methods=['GET'])
def get_pod_specifications(pod_namespace, pod_name):
    pod = kclient.read_namespaced_pod_status(pod_name, pod_namespace)
    pod_info = {}
    pod_info['start_time'] = pod.status.start_time
    pod_info['creation_timestamp'] = pod.metadata.creation_timestamp
    pod_info['phase'] = pod.status.phase
    pod_info['namespace'] = pod.metadata.namespace
    pod_info['dns_policy'] = pod.spec.dns_policy
    pod_info['pod_ip'] = pod.status.pod_ip
    pod_info['restart_policy'] = pod.spec.restart_policy
    pod_info['node'] = pod.spec.node_name
    pod_info['service_account'] = pod.spec.service_account
    pod_info['service_account_name'] = pod.spec.service_account_name
    pod_info['host_ip'] = pod.status.host_ip
    pod_info['qos_class'] = pod.status.qos_class
    pod_info['termination_grace_period_seconds'] = pod.spec.termination_grace_period_seconds
    images = []
    for item in pod.spec.containers:
        images.append(item.image)
    pod_info['images'] = images

    conditions = pod.status.conditions

    return render_template('pod_specifications.html', pod_namespace=pod_namespace, pod_name=pod_name, pod_info=pod_info, conditions=conditions)


@main.route('/pod/<pod_namespace>/<pod_name>/yaml', methods=['GET'])
def get_pod_yaml(pod_namespace, pod_name):
    pod = kclient.read_namespaced_pod(pod_name, pod_namespace)
    return render_template('pod_yaml.html',  pod_namespace=pod_namespace, pod_name=pod_name, pod=pod)


@main.route('/pod/<pod_namespace>/<pod_name>/labels', methods=['GET'])
def get_pod_labels(pod_namespace, pod_name):
    """
    获取指定命名空间下的 Pod 的标签和注解。
    :param pod_namespace:
    :param pod_name:
    :return:
    """
    pod = kclient.read_namespaced_pod(pod_name, pod_namespace)
    labels = pod.metadata.labels
    annotations = pod.metadata.annotations
    return render_template('pod_labels.html', pod_namespace=pod_namespace, pod_name=pod_name, labels=labels, annotations=annotations)


@main.route('/pod/<namespace>/<name>/logs', methods=['GET'])
def get_pod_logs(namespace, name, **kwargs):
    containers = Utils.get_pod_containers(namespace, name)

    print request.args
    if 'container' in request.args:
        container = request.args['container']
    else:
        # 默认显示第一个容器的日志。
        container = containers[0]

    if 'tail_lines' in request.args:
        tail_lines = request.args['tail_lines']
    else:
        # 默认显示50行日志信息。
        tail_lines = 50
    # 获取 pod 内容器的日志信息
    print container
    pod_log = kclient.read_namespaced_pod_log(name, namespace, container=container, tail_lines=tail_lines)
    print pod_log

    return render_template('pod_logs.html', pod_namespace=namespace, pod_name=name,
                           containers=containers, container=container, tail_lines=tail_lines, logs=pod_log)


@main.route('/namespaces', methods=['GET'])
def get_namespaces():
    namespace_list = []
    namespace = {}
    namespaces = kclient.list_namespace()
    for item in namespaces.items:
        namespace['name'] = item.metadata.name
        namespace['creation_timestamp'] = item.metadata.creation_timestamp
        namespace['phase'] = item.status.phase
        namespace_list.append(namespace)
        namespace = {}
    return render_template('namespaces.html', namespaces=namespace_list)


@main.route('/pod/<namespace>/<name>/command', methods=['GET'])
def get_command_result(namespace, name):

    command_result = kclient.connect_get_namespaced_pod_exec(name, namespace, command='pwd', stderr=True, stdin=True, stdout=True, tty=True)

    stderr = True
    stdin = True
    stdout = True
    tty = True

    return render_template('command.html', result=command_result)
