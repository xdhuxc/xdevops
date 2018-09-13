#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

# 获取当前文件所在的目录
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'xdhuxc'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    KUBERNETES_URL = os.environ.get('KUBERNETES_URL') or 'https://172.20.26.150:6443'
    HTTP_TIMEOUT = 10

    def __init__(self):
        pass

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'dev-data.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('PROD_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'prod-data.sqlite')


class TestingConfig(Config):
    TESTING = True
    # 在测试配置中禁用CSRF保护

    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'test-data.sql')


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,

    'default': DevelopmentConfig
}


