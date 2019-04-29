
from app import db
from datetime import datetime
from flask_rest_jsonapi import  Api, ResourceDetail, ResourceList
from flask_sqlalchemy import SQLAlchemy
from marshmallow_jsonapi.flask import Schema
from marshmallow_jsonapi import fields

class Book(db.Model):
    """
    :发布书籍模型
    """
    __tablename__ = 'books'
    # 用户发表数据的信息
    id = db.Column(db.Integer, primary_key=True, index=True)
    book_name = db.Column(db.String(255), index=True)
    book_desc = db.Column(db.String(255))
    book_price = db.Column(db.FLOAT)
    book_number = db.Column(db.Integer)
    book_img_url = db.Column(db.String(255))
    user_id = db.Column(db.Integer) # 来源于user表
    real_name = db.Column(db.String(64))
    user_phone = db.Column(db.String(20))
    user_province = db.Column(db.String(64))
    user_city = db.Column(db.String(64))
    user_region = db.Column(db.String(64))
    user_address = db.Column(db.String(255))
    is_publish = db.Column(db.Boolean, default=True)
    is_sold = db.Column(db.Boolean, default=False)
    wish_num = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime, default=datetime.now())
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now())


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
