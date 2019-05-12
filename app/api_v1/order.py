from flask import Flask, request, json, jsonify
from flask_restful import Resource, Api, reqparse, fields, marshal_with
from . import api_blueprint as api_bp
from ..models.order import GoodsShopCar
from ..models.book import Book
from ..models.user import User
from app import db

api = Api(api_bp)

class OrderGoodsShopCar(Resource):
    def post(self):
        """
        将商品加入购物车
        :return:
        """
        # 定义验证返回的信息
        _response = dict()
        # 通过前端返回的数据进行验证
        req_data = request.data
        data = json.loads(req_data)
        user_id = data['user_id']
        book_id = data['book_id']
        goods = GoodsShopCar()
        goods.user_id = user_id
        goods.status = 1  # 表示用户已经加入购物车
        goods.book_id = book_id
        try:
            db.session.add(goods)
            db.session.commit()
            _response['msg'] = 'commit successfully'
            _response['status'] = '200'
        except:
            db.session.rollback()
            raise
        finally:
            db.session.close()
        return _response, 200
api.add_resource(OrderGoodsShopCar, '/order/addgoods')

class getGoodsCar(Resource):
    def get(self):
        """
        获取用户购物车信息
        :return:
        """
        user_id = request.args.get('user_id')
        own_goods = db.session.query(Book).join(GoodsShopCar, GoodsShopCar.book_id==Book.id).filter(GoodsShopCar.user_id == user_id).all()
        # .filter(GoodsShopCar.user_id == user_id, Book.id == GoodsShopCar.book_id)
        # own_goods = db.session.query(Book).filter(Book.user_id == user_id, GoodsShopCar.book_id == Book.id).all()
        # .join(GoodsShopCar, Book.id == GoodsShopCar.book_id).all()
        # own_goods = db.session.query(GoodsShopCar).filter(GoodsShopCar.user_id == user_id).all()
        print(own_goods)
        book = Book.to_json(own_goods)
        return book, 200
api.add_resource(getGoodsCar, '/order/getgoodscar')