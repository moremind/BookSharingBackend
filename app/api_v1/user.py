from flask import Flask, request, json, jsonify
from flask_restful import Resource, Api, reqparse
from . import api_blueprint as api_bp
from ..models.user import User, UserLog
from app import db
import requests
from baseConfig import baseConfig
from datetime import datetime

api = Api(api_bp)

"""
返回码约束：200：表示查询成功的返回码
          201:失败返回码
"""

class UserApi(Resource):
    """
    : 用于测试接口
    """
    def get(self):
        return {'user': '1'}
api.add_resource(UserApi, '/users')
class RegisterSession(Resource):
    def post(self):
        """
        以微信方式的登陆应用
        :return:登陆成功返回session_key以及open_id
        """
        # 以微信登陆方式的参数
        _response = dict()
        login_data = request.data
        login_data = json.loads(login_data)
        app_id = baseConfig['app_id']
        secret = baseConfig['secret']
        js_code = login_data['code']
        grant_type = baseConfig['grant_type']

        # 通过requests发送post请求获得session以及openid
        url = 'https://api.weixin.qq.com/sns/jscode2session?appid='+app_id+'&secret='+secret+'&js_code='+js_code+'&grant_type='+grant_type
        response = requests.get(url)
        if(response.status_code == 200):
            return response.text
        else:
            _response['error_code'] = response.status_code
            _response['error_mgs'] = 'error'
            return _response

api.add_resource(RegisterSession, '/get/params')

individual_register_parser = reqparse.RequestParser()

class UserRegister(Resource):
    def post(self):
        """
        登陆成功后将微信数据注册到数据库中
        :return:
        """
        _response = dict()
        data = request.data
        data = json.loads(data)
        user_data = data['data']
        new_user = User()
        new_user.open_id = user_data['openId']
        new_user.user_name = user_data['nickName']
        new_user.country = user_data['country']
        new_user.province = user_data['province']
        new_user.city = user_data['city']
        new_user.nick_name = user_data['nickName']
        new_user.user_pic = user_data['avatarUrl']
        new_user.gender = user_data['gender'] # 1:表示男,0表示女

        # 数据库事物
        try:
            db.session.add(new_user)
            db.session.flush()
            userId = new_user.user_id
            # # 新插入用户需要返回用户id，用于用户查询
            _response['user_id'] = userId
            db.session.commit()
        except:
            db.session.rollback()
            raise
        finally:
            db.session.close()

        return _response, 201
api.add_resource(UserRegister, '/user/register')

class UserLogin(Resource):
    def post(self):
        """
        用户使用用户信息进行登录，微信用户登录不需要验证，手机用户登录需要验证手机号码
        只需要更新用户登录时间
        """
        # 定义验证返回的信息
        _response = dict()
        # 通过前端返回的数据进行验证
        req_data = request.data
        data = json.loads(req_data)
        user_id = data['user_id']
        user_log = UserLog()
        user_log.login_time = datetime.now()
        user_log.user_id = user_id
        try:
            db.session.add(user_log)
            db.session.commit()
            _response['msg'] = 'login successfully.'
            return _response, 200
        except:
            db.session.rollback()
            raise
            _response['msg'] = 'login failed.'
            return _response, 201
        finally:
            db.session.close()

api.add_resource(UserLogin, '/user/login')

class UserVerify(Resource):
    def post(self):

        """
        验证用户是否登录过
        """
        # 查询是否存在当前用户，使用微信NickName作为username
        # 如果查询微信用户已经注册，则让用户直接登录，而不再插入数据库，如果未注册，则直接让用户注册并添加到数据库。
        # 查询依据：因为微信用户标识问题，用户的open_id即为唯一标识符，所有只需查询微信用户的open_id
        # 定义验证返回的信息
        _response = dict()
        # 通过前端返回的数据进行验证
        req_data = request.data
        data = json.loads(req_data)
        _openid = data['open_id']
        # 通过用户open_id判断是否存入过数据，未存入，则可以注册，已注册过则直接返回用户数据，前端通过后端返回的数据进行登录
        if User.query.filter_by(open_id=_openid).first() is not None:
            # 查询成功，用户已经注册过，并且查询用户数据并且返回
            _response['msg'] = 'the user already exists.'
            userData = User.query.filter_by(open_id=_openid).all() # 通过微信用户的open_id查询用户是否注册过
            user_data = User.to_json(userData)
            _response['user_data'] = user_data
            return _response, 200
        else:
            # 用户不存在，则userData为空
            _response['msg'] = 'the user not register.'
            _response['userData'] = ''
            return _response, 201

api.add_resource(UserVerify, '/user/verify')

class UserLogout(Resource):
    def post(self):
        """
        用户登出
        :return:返回用户用户登出成功status
        """
        _response = dict()
        # 通过前端返回的数据进行验证
        req_data = request.data
        data = json.loads(req_data)
        user_id = data['user_id']
        user_log = UserLog()
        user_log.user_id = user_id
        user_log.logout_time = datetime.now()
        try:
            db.session.add(user_log)
            db.session.commit()
            _response['msg'] = 'logout successfully.'
            return _response, 200
        except:
            db.session.rollback()
            raise
            _response['msg'] = 'logout failed.'
            return _response, 201
        finally:
            db.session.close()
api.add_resource(UserLogout, '/user/logout')

class GetOneUser(Resource):
    def post(self):
        """
        在用户已经登陆的情况下，通过查询user_id获得某个用户的所有信息
        :return:返回查询到的改用户的所有信息
        """
        _response=dict()
        req_data = request.data
        data = json.loads(req_data)
        user_id = data['user_id']
        userData = User.query.filter_by(user_id=user_id).all()
        user_data = User.to_json(userData)
        _response['user_data'] = user_data
        return _response, 200
api.add_resource(GetOneUser, '/user/getone')

class UpdateUserSign(Resource):
    def post(self):
        """
        通过用户user_id更新用户个性签名
        :return: 成功200, 失败201
        """
        _response = dict()
        req_data = request.data
        data = json.loads(req_data)
        user_id = data['user_id']
        user_sign = data['user_sign']
        try:
            # 查询用户id，并且根据用户id进行更新信息
            User.query.filter_by(user_id=user_id).update({"user_sign": user_sign})
            db.session.commit()
        except:
            db.session.rollback()
            raise
        finally:
            db.session.close()
api.add_resource(UpdateUserSign, '/user/signs')
