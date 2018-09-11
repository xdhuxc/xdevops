#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: zengyumeng
# datetime: 2018/9/11 9:54
# description:

from flask import render_template
from flask import request
from flask import jsonify
from . import main


@main.app_errorhandler(404)
def page_not_found(e):
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response = jsonify({'error': '找不到请求的页面。'})
        response.status_code = 404
        return response
    return render_template('404.html'), 404
