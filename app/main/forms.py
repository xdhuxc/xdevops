#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm

from wtforms import StringField
from wtforms import IntegerField
from wtforms import SubmitField

from wtforms.validators import DataRequired
from wtforms.validators import Length


class Deployment(FlaskForm):
    image_name = StringField('镜像名称', validators=[DataRequired()])
    replicas = IntegerField('副本数量', validators=[DataRequired()])
    submit = SubmitField('创建')

