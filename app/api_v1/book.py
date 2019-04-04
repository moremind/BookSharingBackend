from flask import Flask, request, json, jsonify
from flask_restful import Resource, Api, reqparse, fields, marshal_with
from . import api_blueprint as api_bp
from ..models.book import Book
from app import db
from sqlalchemy.orm import class_mapper


api = Api(api_bp)


class PublishSingleBook(Resource):
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
        book = Book()
        all_books = db.session.query(Book).all()
        # books = marshal_with(all_books)
        # json.dumps(book, cls=AlchemyEncoder)
        # print(all_books)
        # print(books)
        result = []
        # for book in all_books:
        #     result.append(book)
        # print(result)
        # return json.dumps(result), 200
api.add_resource(getAllBooks, '/get/all_books')