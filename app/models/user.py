from app import db
import app
from flask import current_app
from config import config
from datetime import datetime

class User(db.Model):
    __tablename__ = 'user'
    # 微信相关信息
    user_id = db.Column(db.Integer, primary_key=True)
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
