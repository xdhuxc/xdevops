#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wanghuan
# date: 2018-09-09
# description: 工具方法

import os
import yaml

from . import kclient
from kubernetes.client.models.v1_namespace import V1Namespace
from kubernetes.client.models.v1_object_meta import V1ObjectMeta
from kubernetes.client.models.v1_namespace_spec import V1NamespaceSpec
from kubernetes.client.models.v1_namespace_status import V1NamespaceStatus
from kubernetes.client.apis.apiextensions_v1beta1_api import ApiextensionsV1beta1Api

base_dir = os.path.dirname(__file__)


class Utils(object):

    @staticmethod
    def readable(size):
        size = float(size)
        """
        以可视化的形式显示大小。
        :param size:
        :return:
        """
        k, m, g, t, p = float(1024), float(1024**2), float(1024**3), float(1024**4), float(1024**5)
        if size < k:
            return format(size, '.2f') + 'B'
        elif size < m:
            return format((size / k), '.2f') + 'KB'
        elif size < g:
            return format((size / m), '.2f') + 'MB'
        elif size < t:
            return format((size / g), '.2f') + 'GB'
        elif size < p:
            return format((size / t), '.2f') + 'TB'
        else:
            return format((size / p), '.2f') + 'PB'

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
        spec = V1NamespaceSpec()

        body = ''
        kclient.create_namespace(body)

    @staticmethod
    def create_pod_by_yaml(yaml_name, namespace):

        with open(os.path.join(base_dir, yaml_name)) as f:
            deployment = yaml.load(f)
            k8s_beta = kclient.ApiextensionsV1beta1Api()
            resp = k8s_beta.create_namespaced_deployment(body=deployment, namespace=namespace)
            if resp.status == 200:
                print('OK')
            else:
                print('Failed')

    @staticmethod
    def create_deployment(name, image, port, labels, replicas, api_version, deployment_name):
        """
        创建 Deployment 对象并返回
        :param name:
        :param image:
        :param port:
        :param labels:
        :param replicas:
        :param api_version:
        :param deployment_name:
        :return:
        """
        # 配置 Pod 容器模板
        container = kclient.V1Container(
            name=name,
            image=image,
            ports=[kclient.V1ContainerPort(container_port=port)]
        )
        #
        template = kclient.V1PodTemplateSpec(
            metadata=kclient.V1ObjectMeta(labels=labels),
            spec=kclient.V1PodSpec(containers=[container])
        )

        spec = kclient.ExtensionsV1Beta1DeploymentSpec(
            replicas=replicas,
            template=template
        )
        # 实例化 Deployment 对象
        deployment = kclient.ExtensionsV1beta1Deployment(
            api_version=api_version,
            kind='Deployment',
            metadata=kclient.V1ObjectMeta(name=deployment_name),
            spec=spec
        )

        return deployment

    @staticmethod
    def create_namespace(api_version, kind):

        if api_version is None:
            api_version = 'v1'
        if kind is None:
            kind = 'Namespace'

        metadata = ''
        spec = ''
        status = ''

        namespace = kclient.V1Namespace(
            api_version=api_version,
            kind=kind,
            metadata=metadata,
            spec=spec
        )

        return namespace

