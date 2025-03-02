from flask import *
from database import *
# from flask import Flask, render_template, session


user = Blueprint('user', __name__)  # ✅ Renamed from 'admin' to 'user'

@user.route('/user_dashboard')  # ✅ Changed route to match function name
def user_dashboard():  # ✅ Renamed function to 'user_dashboard'
 if 'username' in session:
        return render_template('user_dashboard.html', username=session['username'])
 else:
        return redirect(url_for('public.login'))  # Redirect if not logged in


   

