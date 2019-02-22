from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:123456@127.0.0.1:3306/iotplatformofcnlab'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
iotpdb = SQLAlchemy(app)

class user(userdb.Model):
    __tablename__ = 'user'
    user_id = userdb.Column(userdb.Integer, primary_key=True)  # primary_key会自动填充
    user_name = userdb.Column(userdb.String(40))
    password = userdb.Column(userdb.String(50))
    sex = userdb.Column(userdb.String(4))
    birthday = userdb.Column(userdb.Date)
    phone_model = userdb.Column(userdb.String(40))
    cpu_model = userdb.Column(userdb.String(100))
    memory_size = userdb.Column(userdb.Integer)
    battery_size = userdb.Column(userdb.Float)
    storage_size = userdb.Column(userdb.String(10))

@app.route('/usershow')
def usershow():
    ret = userdb.session.query(user).all()
    print(ret[0].user_name)
    print("4444444444")
    return ret[0].user_name

@app.route('/useradd')
def useradd():
    addTest = user( user_name = "akg", password = "444")
    userdb.session.add(addTest)
    userdb.session.commit()
    return '0'

@app.route('/userdelete')
def userdelete():
    userdb.session.query(user).filter( user.user_name == "akg").delete();
    userdb.session.commit()
    return '0'

@app.route('/useralter')
def useralter():
    userdb.session.query(user).filter(user.user_name == "akg").update({"password" : "111", "phone_model" : "1"})
    return '0'

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)