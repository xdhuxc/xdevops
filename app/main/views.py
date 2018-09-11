#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template
from ..main import main


@main.route('/', methods=['GET'])
def index():
    return render_template('index.html')