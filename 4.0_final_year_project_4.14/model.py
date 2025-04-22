# flask_sqlalchemy是一个用于在Flask应用中处理数据库的扩展
from flask_sqlalchemy import SQLAlchemy

# 一个实例，用于数据库交互
db = SQLAlchemy()

# 用户数据表，                                                               这里后期可以调整，我的数据表的内容不是这样
class User(db.Model):
    __tablename__ = 'user'  # 数据表名称
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(400), nullable=False)

# 评估问卷数据表
class Question(db.Model):
    __tablename__ = 'assessment'
    questionID = db.Column(db.Integer, primary_key=True)
    Question = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # eg: 语言能力、社交能力
    

# 选项数据表
class Option(db.Model):
    __tablename__ = 'option'
    optionID = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    content_of_option = db.Column(db.String(255), nullable=False)

#答题记录
class Response(db.Model):
    __tablename__ = 'response'
    responseid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id = db.Column(db.String,db.ForeignKey('user.id'), nullable=True)  
    questionID = db.Column(db.Integer,db.ForeignKey('assessment.questionID'))
    optionID = db.Column(db.Integer,db.ForeignKey('option.optionID'))
    r_time = db.Column(db.Float, nullable=False) 


