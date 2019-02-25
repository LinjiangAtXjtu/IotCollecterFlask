from flask import Flask
from flask_restful import Api, Resource, reqparse, abort
from datetime import date
import db


app = Flask(__name__)
api = Api(app)


parser = reqparse.RequestParser()
parser.add_argument('username', type=str).add_argument('name', type=str).add_argument('password', type=str).add_argument('sex', type=int).add_argument('birthday', type=date)
parser.add_argument('groupname', type=str).add_argument('description', type=str)
parser.add_argument('page', type=int)


def abort_if_not_exist(username):
    if len(db.ShowUser("username"))==0:
        abort(404, message="User {} doesn't exist".format(username))


class User(Resource):
    def get(self, username):#查询信息
        abort_if_not_exist(username)
        return db.ShowUser(username)

    def delete(self, username):#删除信息
        abort_if_not_exist(username)
        db.DeleteAUser(username)
        return '', 204

    def put(self, username):#修改密码
        args = parser.parse_args(strict=True)
        db.SetPassword(username,args['password'])
        return [], 201#返回信息
    
    def post(self, username):#注册
        args = parser.parse_args(strict=True)
        db.AddAUser(username, args['name'], args['password'], args['sex'], args['birthday'])
        return db.ShowUser(username), 201#返回信息


class UserList(Resource):#用于管理员查看用户列表，后续可添加批量新增、删除用户的功能
    def get(self):
        args = parser.parse_args(strict=True)
        return [len(db.ShowUsers(args['page']))] + db.ShowUsers(args['page'])

    # def post(self):
    #     args = parser.parse_args(strict=True)
    #     userID = int(max(USER_LIST.keys())) + 1
    #     USER_LIST[userID] = {'name': args['name']}
    #     return USER_LIST[userID], 201


class Login(Resource):#用户登录
    def get(self):
        args = parser.parse_args(strict=True)
        username = args['username']
        password = args['password']
        if(1):#判断用户名密码是否匹配
            return '1'#返回相应的token
        else:
            return '用户名或密码错误'


api.add_resource(UserList, '/users')
api.add_resource(User, '/users/<str:username>')
api.add_resource(Login, '/users/login')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)