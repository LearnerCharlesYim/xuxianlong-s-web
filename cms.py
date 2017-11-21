from flask import Flask,render_template,request,redirect,url_for,session,jsonify
import config
from exts import db
from models import User,Index,Person_add
from decorators import login_required


app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

@app.route('/')
def index():

    return render_template('index.html')

@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method =='GET':
        return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        member = request.form.get('member')
        # print(member)
        user = User.query.filter(User.username==username,User.password ==password,User.identity==member).first()
        if user:
            session['user_id'] = user.id
            # 如果想在31天内都不需要登录
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return u'用户名或密码或身份确认错误，请确认后再登录！'


@app.route('/regist/',methods=['GET','POST'])
def regist():
    if request.method =='GET':
        return render_template('regist.html')
    else:
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        member = request.form.get('member')
        print(member)
        # password1要和password2相等才可以
        if password1 != password2:
            return u'两次密码不相等，请核对后再填写！'
        else:
            user = User(username=username,password=password1,identity=member)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))


@app.route('/rank/',methods=['GET','POST'])
@login_required
def rank():
    if request.method == 'GET':

        context = {
            'indexes': Index.query.order_by(Index.final_index.desc()).all()
    }
        return render_template('schoolRank.html', **context)
    else:
        pass




@app.route('/rank/detail/<id>')
def rankDetail(id):
    school_info = Index.query.filter(Index.id == id).first()

    return render_template('schoolRankDetail.html',school_info=school_info)




@app.route('/analysis/', methods=['GET', 'POST'])
@login_required
def analysis():
    if request.method == 'GET':
        return render_template('schoolAnalysis.html')
    else:
        pass


@app.route('/search/',methods=['GET','POST'])
@login_required
def search():
    if request.method == 'GET':
        return render_template('schoolSearch.html')
    else:
        province = request.form.get('province')
        city = request.form.get('city')
        county = request.form.get('county')
        school = request.form.get('school')
        if school =="" and province != "" and city != ""and county != "":
            context = {
            'indexes': Index.query.filter(Index.schoolProvince == province,Index.schoolCity == city,Index.schoolCounty == county).all()
        }
            return render_template('searchDetail.html',**context)
        else:
            index = Index.query.filter(Index.schoolProvince == province,Index.schoolCity == city,Index.schoolCounty == county,Index.schoolName == school).first()
            if index:

                return redirect(url_for('rankDetail',id=index.id))
            else:
                return '没有找到您所检索的学校'





@app.route('/digReport/',methods=['GET','POST'])
@login_required
def diagno():
    if request.method == 'GET':
        return render_template('diagnosticReport.html')
    else:
        pass

@app.route('/newData/',methods=['GET','POST'])
@login_required
def dataManage():
    if request.method == 'GET':
        return render_template('dataManage.html')
    else:
        schoolName = request.form.get('schoolName')
        year = (request.form.get('year'))
        province = request.form.get('province')
        city = request.form.get('city')
        county = request.form.get('county')
        sumStu = int(request.form.get('sumStu'))
        schoolPut = float(request.form.get('schoolPut'))
        studentAvg = float(request.form.get('studentAvg'))
        computerSum = int(request.form.get('computerSum'))
        multiClass = int(request.form.get('multiClass'))
        classSum = int(request.form.get('classSum'))
        broadband = float(request.form.get('broadband'))
        broadbandAvg = float(request.form.get('broadbandAvg'))
        effectPrepare = float(request.form.get('effectPrepare'))
        pertinencePrepare = float(request.form.get('pertinencePrepare'))
        optimizeTeach = float(request.form.get('optimizeTeach'))
        turnoverTeach = float(request.form.get('turnoverTeach'))
        manageCourse = float(request.form.get('manageCourse'))
        communicateCourse = float(request.form.get('communicateCourse'))

        # 投入指数
        if (schoolPut/sumStu)/studentAvg > 1:
            I = 1
        else:
            I = round((schoolPut/sumStu)/studentAvg,2)

        C1 = round(computerSum/sumStu,2)
        C2 = round(multiClass/classSum,2)
        if broadband >= 1000:
            C3 = 1.0
        elif broadband >= 100:
            C3 = 0.5
        elif broadband > 0:
            C3 = 0.2
        else:
            broadband = 0
        # 配置指数
        C = round((C1*C2*C3) ** (1./3),2)

        E1 = round(0.67*effectPrepare+0.33*pertinencePrepare,2)
        E2 = round(0.33*optimizeTeach+0.67*turnoverTeach,2)
        E3 = round(0.67*manageCourse+0.33*communicateCourse,2)

        # 效果指数
        E = round((E1*E2*E3) ** (1./3),2)

        # 总指数
        final_index = round((I**0.25)*(C**0.25)*(E**0.5),2)
        # print(final_index)


        index = Index(schoolName=schoolName,year=year,schoolProvince=province,schoolCity=city,schoolCounty=county,schoolStu=sumStu,schoolPut=schoolPut,studentAvg=studentAvg,computerSum=computerSum,multiClass=multiClass,classSum=classSum,broadband=broadband,broadbandAvg=broadbandAvg,effectPrepare=effectPrepare,pertinencePrepare=pertinencePrepare,optimizeTeach=optimizeTeach,turnoverTeach=turnoverTeach,manageCourse=manageCourse,communicateCourse=communicateCourse,I=I,C1=C1,C2=C2,C3=C3,C=C,E1=E1,E2=E2,E3=E3,E=E,final_index=final_index)
        db.session.add(index)
        db.session.commit()

        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        person_add = Person_add(author_id=user.id,index_id=index.id)
        db.session.add(person_add)
        db.session.commit()

        return redirect(url_for('dataModification'))



@app.route('/alterData/',methods=['GET','POST'])
@login_required
def dataModification():
    if request.method == 'GET':
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()

        context = {
            'person_adds': Person_add.query.filter(Person_add.author_id==user.id)
        }
        return render_template('dataModification.html',**context)
    else:
        # school = request.get_data()
        # index = Index.query.filter(Index.schoolName == school).first()
        # db.session.delete(index)
        # db.session.commit()
        # return jsonify({"code":200,"message":"删除成功"})



@app.route('/alterData/detail/<id>',methods=['GET','POST'])
def dataModificationDetail(id):
    if request.method == 'GET':
        person_model = Person_add.query.filter(Person_add.index_id == id).first()
        return render_template('dataModificationDetail.html',person_model=person_model)
    else:
        person_model = Person_add.query.filter(Person_add.index_id == id).first()
        index = Index.query.filter(Index.id == person_model.index_id).first()
        index.schoolName = request.form.get('schoolName')
        index.year = request.form.get('year')
        index.schoolProvince = request.form.get('province')
        index.schoolCity = request.form.get('city')
        index.schoolCounty = request.form.get('county')
        index.schoolStu = int(request.form.get('sumStu'))
        index.schoolPut = float(request.form.get('schoolPut'))
        index.studentAvg = float(request.form.get('studentAvg'))
        index.computerSum = int(request.form.get('computerSum'))
        index.multiClass = int(request.form.get('multiClass'))
        index.classSum = int(request.form.get('classSum'))
        index.broadband = float(request.form.get('broadband'))
        index.broadbandAvg = float(request.form.get('broadbandAvg'))
        index.effectPrepare = float(request.form.get('effectPrepare'))
        index.pertinencePrepare = float(request.form.get('pertinencePrepare'))
        index.optimizeTeach = float(request.form.get('optimizeTeach'))
        index.turnoverTeach = float(request.form.get('turnoverTeach'))
        index.manageCourse = float(request.form.get('manageCourse'))
        index.communicateCourse = float(request.form.get('communicateCourse'))

        # 投入指数
        I = round((index.schoolPut / index.schoolStu) / index.studentAvg, 2)

        C1 = round(index.computerSum / index.schoolStu, 2)
        C2 = round(index.multiClass / index.classSum, 2)
        if index.broadband >= 1000:
            C3 = 1.0
        elif index.broadband >= 100:
            C3 = 0.5
        elif index.broadband > 0:
            C3 = 0.2
        else:
            index.broadband = 0
        # 配置指数
        C = round((C1 * C2 * C3) ** (1. / 3), 2)

        E1 = round(0.67 * index.effectPrepare + 0.33 * index.pertinencePrepare, 2)
        E2 = round(0.33 * index.optimizeTeach + 0.67 * index.turnoverTeach, 2)
        E3 = round(0.67 * index.manageCourse + 0.33 * index.communicateCourse, 2)

        # 效果指数
        E = round((E1 * E2 * E3) ** (1. / 3), 2)

        # 总指数
        final_index = round((I ** 0.25) * (C ** 0.25) * (E ** 0.5), 2)

        index.I = I
        index.C1 = C1
        index.C2 = C2
        index.C3 = C3
        index.C = C
        index.E1 = E1
        index.E2 = E2
        index.E3 = E3
        index.E = E
        index.final_index = final_index

        # print(final_index)

        # index = Index(schoolName=schoolName, year=year, schoolProvince=province, schoolCity=city, schoolCounty=county,
        #               schoolStu=sumStu, schoolPut=schoolPut, studentAvg=studentAvg, computerSum=computerSum,
        #               multiClass=multiClass, classSum=classSum, broadband=broadband, broadbandAvg=broadbandAvg,
        #               effectPrepare=effectPrepare, pertinencePrepare=pertinencePrepare, optimizeTeach=optimizeTeach,
        #               turnoverTeach=turnoverTeach, manageCourse=manageCourse, communicateCourse=communicateCourse)
        # db.session.add(index)
        # db.session.commit()

        # user_id = session.get('user_id')
        # user = User.query.filter(User.id == user_id).first()
        # person_add = Person_add(author_id=user.id, index_id=index.id)
        # db.session.add(person_add)
        db.session.commit()
        return redirect(url_for('dataModification'))




@app.route('/guidance/',methods=['GET','POST'])
@login_required
def guidance():
    if request.method == 'GET':
        return render_template('guidance.html')
    else:
        pass




# 上下文装饰器
@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user': user}

    return {}

# 注销登录
@app.route('/logout/')
def logout():
    # session.pop('user_id')
    # del session('user_id')
    session.clear()
    return redirect(url_for('login'))



if __name__ == '__main__':
    app.run()
