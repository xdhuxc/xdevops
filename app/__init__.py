#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from config import config
from kubernetes import config as kubernetes_config


bootstrap = Bootstrap()
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)

    # 加载 kubernetes 配置文件
    kubernetes_config.load_kube_config()

    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    return app

