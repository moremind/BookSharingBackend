""""
:function: 写入路由、注册蓝图
"""
from flask import Blueprint

api_blueprint = Blueprint("api_v1", __name__)

from . import book, user, test