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
from kubernetes.client.models.extensions_v1beta1_deployment import ExtensionsV1beta1Deployment
from kubernetes.client.models.v1_container import V1Container
from kubernetes.client.models.v1_container_port import V1ContainerPort
from kubernetes.client.models.extensions_v1beta1_deployment_spec import ExtensionsV1beta1DeploymentSpec
from kubernetes.client.models.v1_pod_template_spec import V1PodTemplateSpec
from kubernetes.client.models.v1_pod_spec import V1PodSpec
from kubernetes.client.models.v1_service import V1Service
from kubernetes.client.models.v1_service_port import V1ServicePort
from kubernetes.client.models.v1_service_spec import V1ServiceSpec
from kubernetes.client.models.v1beta1_http_ingress_path import V1beta1HTTPIngressPath
from kubernetes.client.models.v1beta1_http_ingress_rule_value import V1beta1HTTPIngressRuleValue
from kubernetes.client.models.v1beta1_ingress import V1beta1Ingress
from kubernetes.client.models.v1beta1_ingress_backend import V1beta1IngressBackend
from kubernetes.client.models.v1beta1_ingress_rule import V1beta1IngressRule
from kubernetes.client.models.v1beta1_ingress_spec import V1beta1IngressSpec
from kubernetes.client.models.v1_label_selector import V1LabelSelector


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
    def get_all_namespaces():
        """
        获取所有的命名空间。
        :return:
        """
        namespace_list = []
        namespaces = kclient.list_namespace()
        for item in namespaces.items:
            namespace_list.append(item.metadata.name)
        return namespace_list

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
    def get_deployment(name, replicas, labels, selector, container_name, image, container_port,
                       api_version=None, kind=None, namespace=None):
        """
        创建单容器的 Deployment 实例并返回。
        :param api_version:
        :param name:
        :param namespace:
        :param kind:
        :param replicas:
        :param labels:
        :param selector:
        :param container_name:
        :param image:
        :param container_port:
        :return:
        """
        if api_version is None:
            api_version = 'extensions/v1beta1'
        if kind is None:
            kind = 'Deployment'
        if namespace is None:
            namespace = 'default'
        print api_version
        # 配置 Pod 容器模板
        container = V1Container(name=container_name, image=image,
                                ports=[V1ContainerPort(container_port=container_port)])
        #
        template = V1PodTemplateSpec(metadata=V1ObjectMeta(labels=labels), spec=V1PodSpec(containers=[container]))

        metadata = V1ObjectMeta(name=name, namespace=namespace, labels=labels)
        selector = V1LabelSelector(match_labels=selector)
        spec = ExtensionsV1beta1DeploymentSpec(replicas=replicas, selector=selector, template=template)
        # 实例化 Deployment 并返回。
        return ExtensionsV1beta1Deployment(api_version=api_version, kind=kind, metadata=metadata, spec=spec)

    @staticmethod
    def get_namespace(name, api_version=None, kind=None):
        """
        创建命名空间实例并返回。
        :param api_version:
        :param kind:
        :param name:
        :return:
        """
        if api_version is None:
            api_version = 'v1'
        if kind is None:
            kind = 'Namespace'
        # 为每一个命名空间添加默认的标签 name:${name}
        labels = {'name': name}
        metadata = V1ObjectMeta(name=name, labels=labels)
        spec = V1NamespaceSpec()
        return V1Namespace(api_version=api_version, kind=kind, metadata=metadata, spec=spec)

    @staticmethod
    def get_service(name, selector, port, api_version=None, kind=None, namespace=None, service_type=None):
        """
        创建 Service 实例并返回。
        :param selector:
        :param port:
        :param api_version:
        :param kind:
        :param namespace:
        :param service_type:
        :return:
        """
        if kind is None:
            kind = 'Service'
        if api_version is None:
            api_version = 'v1'
        if service_type is None:
            service_type = 'ClusterIP'
        if namespace is None:
            namespace = 'default'

        # 为每一个 Service 指定一个默认的标签：namespace-app: name
        labels = {namespace + 'app': name}
        metadata = V1ObjectMeta(name=name, namespace=namespace, labels=labels)

        port = V1ServicePort(port=port)

        spec = V1ServiceSpec(selector=selector, type=service_type, ports=[port, ])
        return V1Service(api_version=api_version, kind=kind, metadata=metadata, spec=spec)

    @staticmethod
    def get_ingress(name, host, path, service_name, service_port, api_version=None, kind=None, namespace=None):
        """
        创建 Ingress 实例并返回。
        :param name:
        :param host:
        :param path:
        :param service_name:
        :param service_port:
        :param api_version:
        :param kind:
        :param namespace:
        :return:
        """
        if api_version is None:
            api_version = 'extensions/v1beta1'
        if kind is None:
            kind = 'Ingress'
        if namespace is None:
            namespace = 'default'
        metadata = V1ObjectMeta(name=name, namespace=namespace)
        v1beta1_ingress_backend = V1beta1IngressBackend(service_name=service_name, service_port=service_port)
        v1beta1_http_ingress_path = V1beta1HTTPIngressPath(backend=v1beta1_ingress_backend, path=path)
        v1beta1_http_ingress_rule_value = V1beta1HTTPIngressRuleValue([v1beta1_http_ingress_path, ])
        v1beta1_ingress_rule = V1beta1IngressRule(host=host, http=v1beta1_http_ingress_rule_value)

        rules = [v1beta1_ingress_rule, ]
        spec = V1beta1IngressSpec(rules=rules)
        return V1beta1Ingress(api_version=api_version, kind=kind, metadata=metadata, spec=spec)




