# flask_sqlalchemy是一个用于在Flask应用中处理数据库的扩展
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# 一个实例，用于数据库交互
db = SQLAlchemy()

# 用户数据表，                                                               这里后期可以调整，我的数据表的内容不是这样
class User(db.Model):
    __tablename__ = 'user'  # 数据表名称
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(400), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    education_level = db.Column(db.String(50), nullable=False)  # 学历
    email = db.Column(db.String(255), unique=True, nullable=False)

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

# 反馈
class Feedback(db.Model):
    __tablename__ = 'feedback'

    feedback_id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer)
    content = db.Column(db.Text)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)

# 管理员
class Admin(db.Model):
    __tablename__ = 'admin'  # 数据表名称
    admin_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.TEXT, unique=True, nullable=False)
    password = db.Column(db.TEXT, nullable=False)

# 更新通知
class Notification(db.Model):
    __tablename__ = 'notifications'

    Note_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

#记录用户填写的“是否准确”反馈
class Tracking(db.Model):
    __tablename__ = 'tracking'
    tracking_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text)
    accuracy_opinion = db.Column(db.Text)    # 您认为评估是否准确？
    suggestion = db.Column(db.Text)          # 您对本系统的建议？
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
