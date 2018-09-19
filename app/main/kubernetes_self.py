#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wanghuan
# date: 2018-09-09
# description:


from ..decorators import cert_required

from flask import current_app


class Kubernetes(object):

    @staticmethod
    @cert_required()
    def get_all_pods(rs):
        """

        :param rs:
        :return:
        """
        url = current_app.config['KUBERNETES_URL'] + '/api/v1/pods?watch=False'
        try:
            resp = rs.get(url, timeout=current_app.config['HTTP_TIMEOUT'])
            if resp.status_code == 200:
                return resp.json()
            else:
                return resp.content
        except Exception, e:
            print(Exception, e)

    @staticmethod
    @cert_required()
    def get_command_result(rs, namespace, name):
        """
        /api/v1/namespaces/{namespace}/pods/{name}/exec
        :return:
        """
        url = current_app.config['KUBERNETES_URL'] + '/api/v1/namespaces/%s/pods/%s/exec' % (namespace, name)
        try:
            resp = rs.get(url, timeout=current_app.config['HTTP_TIMEOUT'])
            if resp.status_code == 200:
                return resp.json()
            else:
                return resp.content
        except Exception, e:
            print(Exception, e)

