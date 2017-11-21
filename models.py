from exts import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(50),nullable=False,unique=True)
    password = db.Column(db.String(100),nullable=False)
    identity = db.Column(db.String(100),nullable=False)


class Index(db.Model):
    __tablename__ = 'index'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    # 学校
    schoolName = db.Column(db.String(50),nullable=False,unique=True)
    # 年份
    year = db.Column(db.String(50),nullable=False)
    # 学校地区
    schoolProvince = db.Column(db.String(50))
    schoolCity = db.Column(db.String(50))
    schoolCounty = db.Column(db.String(50))
    # 学校学生总数
    schoolStu = db.Column(db.Integer)
    # 学校年度投入
    schoolPut = db.Column(db.Float)
    # 区县生均经费
    studentAvg = db.Column(db.Float)
    # 计算机配置总数
    computerSum = db.Column(db.Integer)
    # 多媒体教室总数
    multiClass = db.Column(db.Integer)
    # 通用教室与专用教室总数
    classSum = db.Column(db.Integer)
    # 学校网络出口总宽带速度
    broadband = db.Column(db.Float)
    # 区县分配到学校平均值
    broadbandAvg = db.Column(db.Float)
    # 教师备课教学效果指数值
    effectPrepare = db.Column(db.Float)
    # 教师备课教学针对性指数值
    pertinencePrepare = db.Column(db.Float)
    # 教师教学优化课堂指数值
    optimizeTeach = db.Column(db.Float)
    # 教师教学转变学习方式指数值
    turnoverTeach = db.Column(db.Float)
    # 课程管理指数值
    manageCourse = db.Column(db.Float)
    # 课程交流指数值
    communicateCourse = db.Column(db.Float)
    I = db.Column(db.Float)
    C1 = db.Column(db.Float)
    C2 = db.Column(db.Float)
    C3 = db.Column(db.Float)
    C = db.Column(db.Float)
    E1 = db.Column(db.Float)
    E2 = db.Column(db.Float)
    E3 = db.Column(db.Float)
    E = db.Column(db.Float)


    # 就绪指数
    final_index = db.Column(db.Float)




class Person_add(db.Model):
    __tablename__ = 'person_add'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    create_time = db.Column(db.DateTime, default=datetime.now)
    author_id = db.Column(db.Integer,db.ForeignKey("user.id"))
    author = db.relationship('User',backref=db.backref('indexes'))

    index_id = db.Column(db.Integer, db.ForeignKey("index.id"))
    index = db.relationship('Index',backref=db.backref("person_add",uselist=False))

    __mapper_args__ = {
        "order_by": -create_time
    }

