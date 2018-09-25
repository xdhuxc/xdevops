#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wanghuan
# date: 2018-09-09
# description: 工具方法

from . import kclient
from kubernetes.client.models.v1_namespace import V1Namespace
from kubernetes.client.models.v1_object_meta import V1ObjectMeta
from kubernetes.client.models.v1_namespace_spec import V1NamespaceSpec
from kubernetes.client.models.v1_namespace_status import V1NamespaceStatus


class Utils(object):

    @staticmethod
    def readable(size):
        file_size = float(size)
        """
        以可视化的形式显示大小。
        :param size:
        :return:
        """
        k, m, g, t, p = float(1024), float(1024**2), float(1024**3), float(1024**4), float(1024**5)
        if file_size < k:
            return format(file_size, '.2f') + 'B'
        elif file_size < m:
            return format((file_size / k), '.2f') + 'KB'
        elif file_size < g:
            return format((file_size / m), '.2f') + 'MB'
        elif file_size < t:
            return format((file_size / g), '.2f') + 'GB'
        elif file_size < p:
            return format((file_size / t), '.2f') + 'TB'
        else:
            return format((file_size / p), '.2f') + 'PB'

    @staticmethod
    def get_pod_containers(namespace, name):
        """
        获取指定命名空间中的 pod 中的所有容器。
        :param namespace:
        :param name:
        :return:
        """
        containers = []
        pod = kclient.read_namespaced_pod(name, namespace)
        for container in pod.spec.containers:
            containers.append(container.name)
        return containers

    @staticmethod
    def create_namespace(api_version, kind, namespace):
        """
        创建命令空间
        :param name:
        :return:
        """
        namespace = V1Namespace()
        namespace.api_version = api_version
        namespace.kind = kind or 'Namespace'
        metadata = V1ObjectMeta()
        body = ''
        kclient.create_namespace(body)
