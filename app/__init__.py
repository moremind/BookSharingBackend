from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_cors import CORS
from sqlalchemy import create_engine

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    # app.metadata_engine = create_engine(app.config["METADATA_DATABASE_URI"])  # 绑定元数据库引擎
    from .api_v1 import api_blueprint as api_v1_bp  # 加载api的蓝图
    app.register_blueprint(api_v1_bp, url_prefix="/api/v1")  # 注册蓝图

    # 添加路由和自定义的错误页面

    return app