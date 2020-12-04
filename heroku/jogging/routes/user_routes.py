from flask import Blueprint,render_template, request,redirect
from jogging.models import Users,parse_records,db,PointGroup,Points,traindata

user_routes = Blueprint('user_routes',__name__)

@user_routes.route('/',methods=['GET','POST'])
def inedx(data=None):
    data=Users.query.order_by(Users.id.asc()).all()
    return render_template('main_user.html',data=data)

@user_routes.route('/user_add',methods=['GET','POST'])
def add():
    if request.method == 'POST':
        uname=request.form['user_name']
        gen=request.form['gender']
        ad=request.form['addr']
        h=float(request.form['height'])
        w=float(request.form['weight'])
        bdate=request.form['birthday']
        print(uname,gen,h,w,bdate)
        n_user=Users(Name=uname,Gender=gen,Adress=ad,weight=w,height=h,Age=bdate)
        db.session.add(n_user)
        db.session.commit()
        return redirect('/')
    return render_template('user_add.html')
@user_routes.route('/users.json')
def json_data():
    raw_data = User.query.all()
    parsed_data = parse_records(raw_data)    
    return jsonify(parsed_data)
@user_routes.route('/user_mod',methods=['GET','POST'])
def mod():
    if request.method=='GET':
        data = Users.query.order_by(Users.id.asc()).all()
        return render_template('user_mod.html',id=None,change_val=None,data=data)
    if request.method=='POST':
        if request.form['u_id']!="" or request.form['u_id']!=None:
            u_id=int(request.form['u_id'])
        if request.form['val']!="" or request.form['val']!=None:
            val=request.form['val']
        sel=int(request.form.get('column'))
        if sel == 1:
            user = Users.query.filter_by(id=u_id).update({'Name' : val})
        elif sel == 2 :
            user = Users.query.filter_by(id=u_id).update({'Adress' : val})
        elif sel == 3 :
            user = Users.query.filter_by(id=u_id).update({'weight' : float(val)})
        elif sel == 4 :
            user = Users.query.filter_by(id=u_id).update({'height' : float(val)})    
        db.session.commit()
        data = Users.query.order_by(Users.id.asc()).all()
        return render_template('user_mod.html',id=u_id,val=val,data=data)


@user_routes.route('/user_del',methods=['GET','POST'])
def delete():
    if request.method=='GET':
        data = Users.query.order_by(Users.id.asc()).all()
        return render_template('user_del.html',sel=None,data=data)
    if request.method=='POST':
        sel=int(request.form.get('column'))
        print(sel)
        d_user = Users.query.filter_by(id=sel).first()
        d_group_all = PointGroup.query.filter_by(u_id=sel).all()
        print(d_group_all)
        for d_group in d_group_all:
            d_point=Points.query.filter_by(g_id=d_group.id).all()
            for d_p in d_point:
                print(d_p)
                db.session.delete(d_p)
                db.session.commit()
            db.session.delete(d_group)       
            db.session.commit()
        d_traindata=traindata.query.filter_by(u_id=sel).all()
        for d_train in d_traindata:
            db.session.delete(n_train)
            db.session.commit()
        db.session.delete(d_user)
        db.session.commit()
        data = Users.query.order_by(Users.id.asc()).all()
        return render_template('user_del.html',sel=None,data=data)
