#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint

main = Blueprint('main', __name__)


def inject_permissions():
    """
    为了避免每次调用render_template()时都多添加一个模板参数，可以使用上下文处理器。
    上下文处理器能让变量在所有模板中全局可访问。
    :return:
    """
    return dict()


from . import views
from . import errors
