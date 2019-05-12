from app import db
from datetime import datetime

class GoodsShopCar(db.Model):
    """
    用户购物车表
    """
    __tablename__ = 'order_goods_shopcar'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    book_id = db.Column(db.Integer)
    status = db.Column(db.Integer) # 1表示已经加入购物车，0表示从购物车删除
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