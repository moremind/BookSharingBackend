from flask import Flask, request, json, jsonify
from flask_restful import Resource, Api, reqparse, fields, marshal_with
from . import api_blueprint as api_bp
from ..models.book import Book
from app import db

api = Api(api_bp)

class PublishSingleBook(Resource):
    """
    实现添加单本书籍
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
        new_book.book_img_url = book_data['images']
        new_book.real_name = book_data['userName']
        new_book.user_id = book_data['user_id']
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

api.add_resource(PublishSingleBook, '/books/single')

class PublishManyBook(Resource):
    def post(self):
        """
        function: 实现添加多本书籍
        :return: response:200：表示添加成功，201：表示添加失败
        """
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
        new_book.book_img_url = book_data['images']
        new_book.user_id = book_data['user_id']
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

api.add_resource(PublishManyBook, '/books/many')

class getAllBooks(Resource):

    def get(self):
        """
        向服务器取得所有数据数据
        :return:
        """
        all_books = db.session.query(Book).filter(Book.is_publish == True).all()
        book = Book.to_json(all_books)
        return book, 200
api.add_resource(getAllBooks, '/books/all')

class getOwnPublishBooks(Resource):
    def get(self):
        """
        查询用户发布的数据
        :return: 该用户发布的书籍信息
        """
        userId = request.args.get('user_id')
        own_books = db.session.query(Book).filter(Book.user_id == userId).all()
        book = Book.to_json(own_books)
        return book, 200
api.add_resource(getOwnPublishBooks, '/books/own')

class getSearchBook(Resource):
    def get(self):
        """
        查询用户的书籍信息
        :return: 根据用户关键字返回的信息
        """
        req_data = request.args.get('keyword')
        KeyWord = req_data
        search_book = db.session.query(Book).filter(Book.book_name.like("%"+KeyWord+"%"))
        book = Book.to_json(search_book)
        return book, 200
api.add_resource(getSearchBook, '/books/search')

class getOneBook(Resource):
    def get(self):
        """
        根据书籍id查看书籍详细信息
        :return:某本书的相信信息
        """
        book_id = request.args.get('id')
        own_books = db.session.query(Book).filter(Book.id == book_id).all()
        book = Book.to_json(own_books)
        return book, 200
api.add_resource(getOneBook, '/books/getone')

class deleteBook(Resource):
    def post(selfq):
        """
        根据用户提供的书籍id删除用户发布的书籍
        :return:
        """
        _response = dict()
        req_data = request.data
        data = json.loads(req_data)
        book_id = data['book_id']
        user_id = data['user_id']
        try:
            Book.query.filter_by(id=book_id, user_id=user_id).delete()
            db.session.commit()
            _response['msg'] = 'delete successfully!'
            _response['code'] = '200'
        except:
            db.session.rollback()
            raise
        finally:
            db.session.close()
api.add_resource(deleteBook, '/books/deletebook')

class changeBookStatus(Resource):
    def post(self):
        """
        修改书籍发布状态
        :return:
        """
        _response = dict()
        req_data = request.data
        data = json.loads(req_data)
        book_id = data['book_id']
        user_id = data['user_id']
        is_publish = data['is_publish']
        print(data)
        try:
            # 查询用户id，并且根据用户id进行更新信息
            Book.query.filter_by(id=book_id, user_id=user_id).update({"is_publish": is_publish})
            db.session.commit()
        except:
            db.session.rollback()
            raise
        finally:
            db.session.close()
api.add_resource(changeBookStatus, '/books/updatestatus')