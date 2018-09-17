#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from flask import render_template

from . import main
from kubernetes import client

from ..utils import Utils

CHARSET = os.environ.get('CHARSET') or 'utf-8'
reload(sys)
sys.setdefaultencoding(CHARSET)


@main.route('/')
def index():

    return render_template('index.html')


@main.route('/main')
def get_main():
    return render_template('main.html')


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
        pod_list.append(pod_dict)
        pod_dict = {}
    return render_template('pods.html', pod_list=pod_list)


@main.route('/nodes/<node_name>', methods=['GET'])
def get_node(node_name):
    kclient = client.CoreV1Api()
    result = kclient.read_node(node_name)
    return render_template('node_base.html', node_name=node_name, node=result)


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


    pass


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
    node_info['architecture'] = system_info.system_info
    node_info['boot_id'] = system_info.boot_id
    node_info['container_runtime_version'] = system_info.container_runtime_version
    node_info['kernel_version'] = system_info.kernel_version
    node_info['kube_proxy_version'] = system_info.kube_proxy_version
    node_info['kubelet_version'] = system_info.kubelet_version
    node_info['machine_id'] = system_info.machine_id
    node_info['operating_system'] = system_info.operating_system
    node_info['os_image'] = system_info.os_image
    node_info['system_uuid'] = system_info.system_uuid

    return render_template('node_specifications.html', node_name=node_name)


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
