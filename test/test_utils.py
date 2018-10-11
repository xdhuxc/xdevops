#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wanghuan
# date: 2018-09-09
# description:

import sys
import unittest

from app.utils import Utils
from app import kclient
from app import original_client
from kubernetes.client.rest import ApiException

from app import logger

reload(sys)
sys.setdefaultencoding('utf-8')


class UtilsTest(unittest.TestCase):

    def setUp(self):
        # 创建命名空间
        self.namespace = Utils.get_namespace(name='yztc')
        # 创建 Deployment 的标签
        self.deployment_labels = {'xdhuxc-app': 'nginx-xdhuxc'}
        # 创建 Deployment 的选择器
        self.deployment_selector = {'xdhuxc-app': 'nginx-xdhuxc'}
        # 获取 Deployment 实例
        self.deployment = Utils.get_deployment('nginx-xdhuxc', 1, self.deployment_labels, self.deployment_selector,
                    'nginx-xdhuxc', 'yonyoucloud-kubernetes/nginx:test', 80, namespace=self.namespace.metadata.name)
        # 获取 Service 实例
        self.service = Utils.get_service('xdhuxc-nginx-service',
                                         self.deployment_selector, 80, namespace=self.namespace.metadata.name)
        # 获取 Ingress 实例
        self.ingress = Utils.get_ingress('xdhuxc-ingress', 'yztc.com', '/', self.service.metadata.name, 80,
                                         namespace=self.namespace.metadata.name)

    def test_create_namespace(self):
        try:
            result = kclient.create_namespace(body=self.namespace, pretty=True)
        except ApiException as e:
            logger.info(e)

    def test_create_deployment(self):
        try:
            result = original_client.ExtensionsV1beta1Api().create_namespaced_deployment(
                namespace=self.namespace.metadata.name, body=self.deployment)

        except ApiException as e:
            logger.info(e)

    def test_create_service(self):
        try:
            result = kclient.create_namespaced_service(namespace=self.namespace.metadata.name, body=self.service)

        except ApiException as e:
            logger.info(e)

    def test_create_ingress(self):
        try:
            result = original_client.ExtensionsV1beta1Api().create_namespaced_ingress(
                namespace=self.namespace.metadata.name, body=self.ingress)

        except ApiException as e:
            logger.info(e)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main(verbosity=2)

