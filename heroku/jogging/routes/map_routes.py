from flask import Blueprint,render_template, request,redirect
from jogging.models import Users,db,PointGroup,Points,traindata
from sklearn.linear_model import LogisticRegression
import json
import random
import os,pickle

map_routes = Blueprint('map_routes',__name__)


@map_routes.route('/<u_id>/',methods=['GET','POST'])
def main_map(u_id=None,sel=None):
    p_data=[]
    try:
        data=PointGroup.query.filter_by(u_id=u_id).order_by(PointGroup.id.asc()).all()
        sel=data[0].id
    except:
        data=None
    if request.method=='GET':
        if sel !=None:
            pdata=Points.query.filter_by(g_id=sel).order_by(Points.id.asc()).all()
            for p in pdata:
                p_data.append([p.lng,p.lat])
    if request.method=='POST':
        sel=int(request.form.get('column'))
        pdata=Points.query.filter_by(g_id=sel).order_by(Points.id.asc()).all()
        for p in pdata:
            p_data.append([p.lng,p.lat])
    return render_template('main_jog.html',u_id=u_id,data=data,p_data=p_data)
    

@map_routes.route('/<u_id>/add',methods=['GET','POST'])
def path_add(u_id=None):
    if request.method=='POST':
        group_name=request.form['path_name']
        dropoffs=json.loads(request.form['dropoffs'])
        n_group=PointGroup(u_id=u_id,Name=group_name)
        db.session.add(n_group)
        db.session.commit()
        print(n_group)
        for drop in dropoffs['features']:
            n_point=Points(g_id=n_group.id,lng=drop['geometry']['coordinates'][0],lat=drop['geometry']['coordinates'][1])
            print(n_point)
            db.session.add(n_point)
            db.session.commit()

        
    return render_template('path_add.html',u_id=u_id)

@map_routes.route('/<u_id>/del',methods=['GET','POST'])
def path_del(u_id=None):
    if request.method=='GET':
        data =PointGroup.query.filter_by(u_id=u_id).order_by(PointGroup.id.asc()).all()
        return render_template('path_del.html',u_id=u_id,sel=None,data=data)
    if request.method=='POST':
        sel=int(request.form.get('column'))
        d_group = PointGroup.query.filter_by(id=sel).first()
        d_point=Points.query.filter_by(g_id=d_group.id).all()
        for d_p in d_point:
            db.session.delete(d_p)
            db.session.commit()
        db.session.delete(d_group)       
        db.session.commit()
        data =PointGroup.query.filter_by(u_id=u_id).order_by(PointGroup.id.asc()).all()
        return render_template('path_del.html',u_id=u_id,sel=None,data=data)

@map_routes.route('/<u_id>/rec',methods=['GET','POST'])
def path_rec(u_id=None,p_data=None,sel=None):
    data=PointGroup.query.filter_by(u_id=u_id).order_by(PointGroup.Name.asc()).all()

    if request.method=='POST' and 'taste' in request.form:

        taste=request.form['taste']
        point=str(request.form['p_data']).split(",")

        p_list=[]
        ylabel=0
        for p in point:
            p_list.append(float(p))
        if taste == 'like':
            ylabel=1
        n_data=traindata(u_id=u_id,X=p_list,y=ylabel)
        db.session.add(n_data)
        db.session.commit()

        train_d=traindata.query.filter_by(u_id=u_id).all()
        if len(train_d) > 10:
            X=[]
            y=[]
            for td in train_d:
                X.append(td.X)
                y.append(td.y)
            cset=set(y)
            if len(cset)==2: # case가 2개 이상일 때(0,1이 모두 있을 때)만 모델 생성
                file_path = os.path.join(os.getcwd(),"""{}.pkl""".format(u_id))
                lg=LogisticRegression()
                lg.fit(X,y)
                with open(file_path, 'wb') as f:
                    pickle.dump(lg, f)

    if request.method=='POST' and 'column' in request.form:
        p_data=[]
        sel=int(request.form.get('column'))
        d_group = PointGroup.query.filter_by(id=sel).first()
        d_point=Points.query.filter_by(g_id=d_group.id).all()

        file_path = os.path.join(os.getcwd(),"""{}.pkl""".format(u_id))
        if os.path.isfile(file_path) == True: # 만들어둔 모델이 있을 때
            with open(file_path,'rb') as f:
                trained_model=pickle.load(f)
            while True:
                test_X=[]
                pdata=random.sample(d_point,4)
                pdata.append(pdata[0])
                for p in pdata:
                    p_data.append([p.lng,p.lat])
                    test_X.append(p.lng)
                    test_X.append(p.lat)
                result=trained_model.predict([test_X])[0]
                if(result==1):# 모델이 like 라고 예측되면 더이상 
                    break
        else : #모델이 없을 때는 그냥 무작위 경로 생성
            pdata=random.sample(d_point,4)
            pdata.append(pdata[0])
            for p in pdata:
                p_data.append([p.lng,p.lat])
    return render_template('path_rec.html',u_id=u_id,data=data,sel=sel,p_data=p_data)