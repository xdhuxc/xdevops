#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm

from wtforms import StringField
from wtforms import IntegerField
from wtforms import SubmitField
from wtforms import SelectField

from wtforms.validators import DataRequired
from wtforms.validators import Length

from ..utils import Utils


class DeploymentForm(FlaskForm):
    pod_name = StringField('服务名称', validators=[DataRequired()])
    pod_image_name = StringField('镜像名称', validators=[DataRequired()])
    pod_replicas = IntegerField('副本数量', validators=[DataRequired()])
    namespaces = Utils.get_all_namespaces()
    pod_namespace = SelectField('命名空间', validators=[DataRequired()])
    container_port = IntegerField('容器端口', validators=[DataRequired()])
    submit = SubmitField('创建')

