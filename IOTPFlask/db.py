from sqlalchemy import Column, Integer, String, DATE, ForeignKey, DateTime, func, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine("mysql+pymysql://root:123456@localhost/iotplatformofcnlab", encoding='utf-8', echo=True)
base = declarative_base()
Session_class = sessionmaker(bind=engine)  # 创建与数据库的会话，class,不是实例
Session = Session_class()
PAGE_SIZE = 30

# 创建grouping表，关联group和user表
Grouping = Table('grouping', base.metadata,
                 Column('userID',Integer,ForeignKey('user.id')),
                 Column('groupID',Integer,ForeignKey('group.id')),
                 Column('createTime', DateTime, server_default=func.now()),
                 Column('updateTime', DateTime, server_default=func.now(), onupdate=func.now())
                 )


class User(base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(64))
    name = Column(String(64))
    password = Column(String(64))
    sex = Column(Integer)
    birthday = Column(DATE)
    createTime = Column(DateTime, server_default=func.now())
    updateTime = Column(DateTime, server_default=func.now(), onupdate=func.now())
    groups = relationship('Group', secondary=Grouping, backref='users')


    def to_json(self):
        return {
            "username": self.username,
            "name": self.name,
            "sex": 'male' if self.sex else 'female',
            "birthday": self.birthday,
            "createTime": self.createTime,
            "updateTime": self.updateTime,
            "groups": [e.groupname for e in self.groups],
        }


class Group(base):
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True)
    groupname = Column(String(32))
    description = Column(String(128))
    createTime = Column(DateTime, server_default=func.now())
    updateTime = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def to_json(self):
        return {
            "groupname": self.groupname,
            "description": self.description,
            "createTime": self.createTime,
            "updateTime": self.updateTime
        }

    def to_json_detail(self):
        return {
            "groupname": self.groupname,
            "description": self.description,
            "createTime": self.createTime,
            "updateTime": self.updateTime,
            "users": [e.to_json() for e in self.users]
        }


def createall():
    base.metadata.drop_all(engine);
    base.metadata.create_all(engine)  # 创建表结构

#The following: operations in user
def AddAUser(username, name, password, sex, birthday):
    Session.add(User(username = username, name= name, password = password, sex = sex, birthday = birthday))
    Session.commit()

def DeleteAUser(username):
    Session.query(User).filter(username = username).delete()
    Session.commit()

def SetPassword(username, newPassword):
    Session.query(User).filter(username = username).update({"password" : newPassword})
    Session.commit();

def ShowUser(username):
    result = Session.query(User).filter_by(username = username).all()
    return [e.to_json(len(result)) for e in result]

def ShowUsers(page = 0):
    result = Session.query(User).limit(PAGE_SIZE).offset((page)*PAGE_SIZE)
    return [e.to_json() for e in result]

def getGroupListByNameList(nameList):
    return Session.query(Group).filter(Group.groupname.in_(nameList)).all()

def AddGroupToUser(username, groupNameList):
    Session.query(User).filter_by(username=username).first().groups = getGroupListByNameList(groupNameList)
    Session.commit()

#following: operations in group
def AddAGroup(groupname, description):
    Session.add(Group(groupname = groupname, description = description))
    Session.commit()

def DeleteAGroup(groupname):
    Session.query(Group).filter(groupname = groupname).delete()
    Session.commit()

def SetDescription(groupname, newDescription):
    Session.query(Group).filter(groupname = groupname).update({"description" : newDescription})
    Session.commit();

def ShowGroup(groupname):
    result = Session.query(Group).filter_by(groupname = groupname).all()
    return [e.to_json_detail() for e in result]

def ShowGroups(page = 0):
    result = Session.query(Group).limit(PAGE_SIZE).offset((page)*PAGE_SIZE)
    return [e.to_json() for e in result]