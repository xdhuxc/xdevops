#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wanghuan
# date: 2018-09-09
# description: 工具方法


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
