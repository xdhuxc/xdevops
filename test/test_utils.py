#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wanghuan
# date: 2018-09-09
# description:

import sys

from app.utils import Utils
from app import kclient
from app import oclient
from kubernetes.client.rest import ApiException

from app import logger

reload(sys)
sys.setdefaultencoding('utf-8')

# 创建命名空间
namespace = Utils.get_namespace(name='yztc')
print namespace

try:
    print
    # result = kclient.create_namespace(body=namespace, pretty=True)
    # pprint(result)
except ApiException as e:
    print("Create Namespace: \n%s\n" % e)

deployment_labels = {'xdhuxc-app': 'nginx-xdhuxc'}
deployment_selector = {'xdhuxc-app': 'nginx-xdhuxc'}
deployment = Utils.get_deployment('nginx-xdhuxc', 1, deployment_labels, deployment_selector, 'nginx-xdhuxc',
                                  'yonyoucloud-kubernetes/nginx:test', '80', namespace=namespace.metadata.name)
print deployment
try:
    result = oclient.ExtensionsV1beta1Api().create_namespaced_deployment(namespace=namespace.metadata.name,
                                                                         body=deployment)
except ApiException as e:
    logger.info(e)
    # print("Create Deployment：\n%s" % e)


service = Utils.get_service('xdhuxc-nginx-service', deployment_selector, namespace=namespace.metadata.name)
try:
    result = kclient.create_namespaced_service(namespace=namespace.metadata.name, body=service)
except ApiException as e:
    logger.info(e)
    # print("Create Service：\n%s" % e)


ingress = Utils.get_ingress('xdhuxc-ingress', 'yztc.com', '/', service.metadata.name, 80, namespace=namespace.metadata.name)
try:
    result = oclient.ExtensionsV1beta1Api().create_namespaced_ingress(namespace=namespace.metadata.name, body=ingress)
except ApiException as e:
    print("Create Ingress：\n%s" % e)