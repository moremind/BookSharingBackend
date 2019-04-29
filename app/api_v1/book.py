from flask import Flask, request, json, jsonify
from flask_restful import Resource, Api, reqparse, fields, marshal_with
from . import api_blueprint as api_bp
from ..models.book import Book
from app import db
from datetime import datetime
from qcloud_cos_py3.cos_auth import CosAuth
# from qcloud_cos import CosS3Auth
import baseConfig
from time import time
import requests

api = Api(api_bp)

class PublishSingleBook(Resource):
    """
    :实现添加单本书籍
    """
    def post(self):
        # 获取request数据
        _response = dict()
        data = request.data
        data = json.loads(data)
        book_data = data['data']
        new_book = Book()
        # 对model进行赋值
        new_book.book_name = book_data['bookName']
        new_book.book_desc = book_data['bookDesc']
        new_book.book_price = book_data['bookPrice']
        new_book.book_img_url = '22222'
        new_book.real_name = book_data['userName']
        new_book.user_phone = book_data['phone']
        new_book.user_province = book_data['province']
        new_book.user_city = book_data['city']
        new_book.user_region = book_data['region']
        new_book.user_address = book_data['address']
        new_book.book_number = 1
        # 进行数据库事物
        try:
            db.session.add(new_book)
            db.session.commit()
        except:
            db.session.rollback()
            raise
        finally:
            db.session.close()
        return _response, 200

api.add_resource(PublishSingleBook, '/publish/single')

class PublishManyBook(Resource):
    """
    :function: 实现添加多本书籍
    :return: response:200：表示添加成功，401：表示添加失败
    """
    def post(self):
        _response = dict()
        # 解析数据
        data = request.data
        data = json.loads(data)
        book_data = data['data']
        new_book = Book()
        # 对model进行赋值
        new_book.book_number = book_data['bookNum']
        new_book.book_name = book_data['bookName']
        new_book.book_desc = book_data['bookDesc']
        new_book.book_price = book_data['bookPrice']
        new_book.book_img_url = '22222'
        new_book.real_name = book_data['userName']
        new_book.user_phone = book_data['phone']
        new_book.user_province = book_data['province']
        new_book.user_city = book_data['city']
        new_book.user_region = book_data['region']
        new_book.user_address = book_data['address']

        # 进行数据库事物
        try:
            db.session.add(new_book)
            db.session.commit()
        except:
            db.session.rollback()
            raise
        finally:
            db.session.close()
        return _response, 200

api.add_resource(PublishManyBook, '/publish/many')

class getAllBooks(Resource):

    def get(self):
        """
        :向服务器取得所有数据数据
        :return:
        """
        all_books = db.session.query(Book).all()
        book = Book.to_json(all_books)
        return book, 200
api.add_resource(getAllBooks, '/get/all_books')

class getCosAuth(Resource):
    def get(self):
        auth = CosAuth(appid=baseConfig.QCOS_APPID,
                       secret_id=baseConfig.QCOS_SECRET_ID,
                       secret_key=baseConfig.QCOS_SECRET_KEY)
        expired = time() + 3600  # 签名有效时间 3600 秒
        # 上传到 cos bucket 的目录
        dir_name = requests.get('cos_path', '/xrzeti')
        # dir_name = request.raw_args.get('cos_path', '/xrzeti')
        # 生成签名
        sign = auth.sign_more(baseConfig['QCOS_BUCKET_NAME'],
                              cos_path=dir_name,
                              expired=expired)
        return {"sign": sign}, 200
api.add_resource(getCosAuth, '/get/upload_auth')