from flask import Flask
from flask_restful import Api, Resource, reqparse, abort

app = Flask(__name__)
api = Api(app)

USER_LIST = {
    1: {'name':'Michael'},
    2: {'name':'Tom'},
}

parser = reqparse.RequestParser()
parser.add_argument('name', type=str)

def abort_if_not_exist(userID):
    if userID not in USER_LIST:
        abort(404, message="User {} doesn't exist".format(userID))

class User(Resource):
    def get(self, userID):#查询信息
        abort_if_not_exist(userID)
        #从数据库查询相关信息
        return USER_LIST[userID]

    def delete(self, userID):#删除信息
        abort_if_not_exist(userID)
        #从数据库删除相关信息
        return '', 204

    def put(self, userID):#注册
        args = parser.parse_args(strict=True)
        #将args['username']}等信息存入数据库
        return USER_LIST[userID], 201#返回信息
    
    def post(self, userID):#修改信息
        args = parser.parse_args(strict=True)
        # 将args['username']}等信息修改入数据库
        return USER_LIST[userID], 201#返回信息

class UserList(Resource):#用于管理员查看用户列表，后续可添加批量新增、删除用户的功能
    def get(self):
        return USER_LIST#从数据库返回用户列表，分页

    # def post(self):
    #     args = parser.parse_args(strict=True)
    #     userID = int(max(USER_LIST.keys())) + 1
    #     USER_LIST[userID] = {'name': args['name']}
    #     return USER_LIST[userID], 201

class Login(Resource):#用于管理员查看用户列表，后续可添加批量新增、删除用户的功能
    def get(self):
        args = parser.parse_args(strict=True)
        userID = args['userID']
        password = args['password']
        if(1):#判断用户名密码是否匹配
            return '1'#返回相应的token
        else:
            return '用户名或密码错误'

api.add_resource(UserList, '/users')
api.add_resource(User, '/users/<str:userID>')
api.add_resource(Login, '/users/login')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)