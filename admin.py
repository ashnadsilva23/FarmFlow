from flask import *
from database import *

admin=Blueprint('admin',__name__)


@admin.route('/admin_home')
def admin_homee():
	return render_template('admin_home.html')  

@admin.route('/admin_manage_farmer',methods=['get','post'])
def admin_manage_farmer():
    data={}
    if 'submitbutton' in request.form:
        fname=request.form['firstname']
        lname=request.form['lastname']
        city=request.form['city']
        phone=request.form['phone']
        email=request.form['email']
        uname=request.form['username']
        pwd=request.form['password']
        kl="select * from login where username='%s'"%(uname)
        gg=select(kl)
        if gg:
            flash("Username already exists.........!")
        else:
            jj="insert into login values(null,'%s','%s','user')"%(uname,pwd)
            kk=insert(jj)
            lk="insert into farmer values(null,'%s','%s','%s','%s','%s','%s')"%(kk,fname,lname,city,phone,email)
            insert(lk)
            flash("Registration success.......!")
            return redirect(url_for('admin.admin_manage_farmer'))
    user = "select * from farmer"
    data={}
    data['user_view'] = select(user)
    if 'action' in request.args:
        action=request.args['action']
        farmer_id=request.args['farmer_id']
        login_id=request.args['login_id']
    else:
        action=None  
    if action=='delete':
        hj="delete from farmer where farmer_id='%s'"%(farmer_id)
        delete(hj)
        hjj="delete from login where login_id='%s'"%(login_id)
        delete(hjj)
        flash("Deleted........!")
        return redirect(url_for('admin.admin_manage_farmer'))
    if action=='update':
        vv="select * from farmer where farmer_id='%s'"%(farmer_id)
        data['up']=select(vv)
    if 'update' in request.form:
        fname=request.form['firstname']
        lname=request.form['lastname']
        city=request.form['city']
        phone=request.form['phone']
        email=request.form['email']
        km="update farmer set firstname='%s',lastname='%s',city='%s',phone='%s',email='%s' where farmer_id='%s' "%(fname,lname,city,phone,email,farmer_id)
        update(km)
        flash("Updated........!")
        return redirect(url_for('admin.admin_manage_farmer'))
    return render_template('admin_manage_farmer.html',data=data)  