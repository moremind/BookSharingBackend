from flask import Flask, request, json, jsonify
from flask_restful import Resource, Api, reqparse
from . import api_blueprint as api_bp
from ..models.user import User
from app import db
import requests
from baseConfig import baseConfig

api = Api(api_bp)


class UserApi(Resource):
    def get(self):
        return {'user': '1'}
api.add_resource(UserApi, '/users')
class RegisterSession(Resource):
    def post(self):
        """
        :以微信方式的登陆应用
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
class RegisterUser(Resource):
    def post(self):
        """
        :登陆成功后将微信数据注册到数据库中
        :return:
        """
        # print(request.encryptedData)
        _response = dict()
        data = request.data
        data = json.loads(data)
        user_data = data['data']
        new_user = User()
        _openid = user_data['openId']
        # 查询是否存在当前用户，使用微信NickName作为username
        # 如果查询微信用户已经注册，则让用户直接登录，而不再插入数据库，如果未注册，则直接让用户注册并添加到数据库。
        # 查询依据：因为微信用户标识问题，用户的open_id即为唯一标识符，所有只需查询微信用户的open_id
        if User.query.filter_by(open_id=_openid).first() is not None:
            _response["error"] = "the user already exists."
            return user_data, 401
        else:
            new_user.open_id = user_data['openId']
            new_user.user_name = user_data['nickName']
            new_user.country = user_data['country']
            new_user.province = user_data['province']
            new_user.city = user_data['city']
            new_user.nick_name = user_data['nickName']
            new_user.user_pic = user_data['avatarUrl']
            new_user.gender = user_data['gender'] # 1:表示男,0表示女

            user_id = ''
            # 数据库事物
            try:
                db.session.add(new_user)
                db.session.flush()
                # 新插入用户需要返回用户id，用于用户查询
                _response[user_id] = user_id
                db.session.commit()
            except:
                db.session.rollback()
                raise
            finally:
                db.session.close()

            return _response, 201

api.add_resource(RegisterUser, '/user/register')
