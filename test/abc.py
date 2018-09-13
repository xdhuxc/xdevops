#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wanghuan
# date: 2018-09-09
# description:

import os
import requests


@main.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@main.route('/pod')
def manage_pod():
    return render_template('pod.html')