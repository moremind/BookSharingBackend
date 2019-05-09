from app import db
import app
from flask import current_app
from config import config
from datetime import datetime

class User(db.Model):
    __tablename__ = 'user'
    # 微信相关信息
    user_id = db.Column(db.Integer, primary_key=True, index=True)
    open_id = db.Column(db.String(255), unique=True) # 用户的唯一标识
    user_name = db.Column(db.String(64), index=True)
    user_phone = db.Column(db.String(18))
    user_address = db.Column(db.String(255))
    user_sign = db.Column(db.String(255))
    nick_name = db.Column(db.String(64))
    user_pic = db.Column(db.String(255))
    gender = db.Column(db.Boolean)
    country = db.Column(db.String(255))
    province = db.Column(db.String(255))
    city = db.Column(db.String(255))
    create_time = db.Column(db.DateTime, default=datetime.now())
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now())

    # def to_dict(self):
    #     model_dict = dict(self.__dict__)
    #     del model_dict['_sa_instance_state']
    #     return model_dict
    #
    # Base.to_dict = to_dict  # 注意:这个跟使用flask_sqlalchemy的有区别

    def single_to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def data_to_dict(self):
        result = {}
        for key in self.__mapper__.c.keys():
            if getattr(self, key) is not None:
                result[key] = str(getattr(self, key))
            else:
                result[key] = getattr(self, key)
        return result

    def to_json(all_vendors):
        v = [ven.data_to_dict() for ven in all_vendors]
        return v

# 用户日志表
class UserLog(db.Model):
    __tablename__ = 'user_log'
    log_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    login_time = db.Column(db.DateTime)
    logout_time = db.Column(db.DateTime)
    # login_type = db.Column(db.Strig(255), default=1) # 1表示微信登录，2表示手机登录
