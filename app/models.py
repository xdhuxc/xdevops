#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wanghuan
# date: 2018-09-09
# description:

from . import db
import json


class Deployment(db.Model):
    __tablename__ = 'deployments'
    pod_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pod_name = db.Column(db.String(120), unique=True, comment='Pod 名称')
    pod_image_name = db.Column(db.Text, comment='镜像名称')
    pod_replicas = db.Column(db.Integer, comment='Pod 副本')
    container_port = db.Column(db.Integer, comment='容器端口')

    def __init__(self, **kwargs):
        super(Deployment, self).__init__(**kwargs)

    def __repr__(self):
        """
        输出该对象的 JSON 格式。
        :return:
        """
        deployment_json = {
            'pod_id': self.pod_id,
            'pod_name': self.pod_name,
            'pod_image_name': self.pod_image_name,
            'pod_replicas': self.pod_replicas,
            'container_port': self.container_port
        }
        return json.dumps(deployment_json)


