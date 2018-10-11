#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask import Flask
from config import config
from kubernetes import config as kubernetes_config
from kubernetes import client as kubernetes_client
import logging

bootstrap = Bootstrap()
db = SQLAlchemy()
moment = Moment()

# 加载 kubernetes 配置文件
kubernetes_config.load_kube_config()
# 创建 kubernetes 客户端对象
kclient = kubernetes_client.CoreV1Api()
original_client = kubernetes_client


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)
    moment.init_app(app)

    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    return app


def create_logger():
    """
    创建一个日志记录器并返回
    :return:
    """
    # 创建一个 logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # 创建一个 FileHandler 对象，用于写入日志文件
    file_handler = logging.FileHandler('xdevops.log')
    file_handler.setLevel(logging.DEBUG)

    # 创建一个 StreamHandler 对象，用于输出到控制台
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)

    # 定义 handler 的输出格式
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    # 给 logger 添加处理器
    logger.addHandler(file_handler)
    # logger.addHandler(stream_handler)

    return logger

# 日志记录器
logger = create_logger()

