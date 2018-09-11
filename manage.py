#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from app import create_app
from app import db
from flask_script import Manager
from flask_script import Shell
from flask_migrate import Migrate
from flask_migrate import MigrateCommand
from flask_migrate import upgrade

CHARSET = os.environ.get('CHARSET') or 'utf-8'
reload(sys)
sys.setdefaultencoding(CHARSET)

# 获取当前文件所在目录
basedir = os.path.abspath(os.path.dirname(__file__))

app = create_app(os.environ.get('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
