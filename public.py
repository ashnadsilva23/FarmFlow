from flask import *
from database import *
from werkzeug.security import check_password_hash  # Import password verification
from werkzeug.security import generate_password_hash


public = Blueprint('public', __name__)

@public.route('/')
def public_homee():
    return render_template('public_home.html')

@public.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':  # Check if form was submitted
        uname = request.form['uname']
        pwd = request.form['password']

        # ✅ Secure Query (Prevents SQL Injection)
        fg = "SELECT * FROM login WHERE username=%s"
        ds = select(fg, (uname,))  # Using a parameterized query

        if ds:
            stored_hashed_password = ds[0]['password']  # Get stored hashed password
            
            # ✅ Compare user-entered password with stored hashed password
            if check_password_hash(stored_hashed_password, pwd):  
                session['login_id'] = ds[0]['login_id']  # Store login_id in session
                session['username'] = uname  # ✅ Store username in session

                user_type = ds[0]['usertype']  # Get user type
                flash("Login successful!")

                if user_type == 'admin':  
                    return redirect(url_for('admin.admin_homee'))
                elif user_type == 'user':  
                    return redirect(url_for('user.user_dashboard'))  
            else:
                flash("Invalid username or password!")

        else:
            flash("Invalid username or password!")  

        return redirect(url_for('public.login'))  # Redirect after failed login

    return render_template('login.html')


@public.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']

        # ✅ Check if email exists in database
        query = "SELECT * FROM farmer WHERE email=%s"
        user = select(query, (email,))

        if user:
            return render_template('reset_password.html', email=email)  # Show reset password form
            # Here, implement logic to send an email with a password reset link
        else:
            flash("This email is not registered!")

        return redirect(url_for('public.login'))  # Fixed blueprint issue

    return render_template('forgot_password.html')

@public.route('/reset-password', methods=['POST'])
def reset_password():
    if request.method == 'POST':
        # ✅ Get email from form
        email = request.form.get('email')
        new_password = request.form.get('password')

        if not email or not new_password:
            flash("Invalid request! Email or password missing.")
            return redirect(url_for('public.forgot_password'))

        # ✅ Find username linked to the email from the farmer table
        query = "SELECT username FROM login WHERE username = (SELECT firstname FROM farmer WHERE email = %s)"
        user = select(query, (email,))  # Fetch result

        if not user:
            flash("Email not found in the system.")
            return redirect(url_for('public.forgot_password'))

        username = user[0]['username']  # Extract username

        # ✅ Hash the new password
        hashed_password = generate_password_hash(new_password)

        # ✅ Update password in login table
        update_query = "UPDATE login SET password = %s WHERE username = %s"
        update(update_query, (hashed_password, username))

        flash("Password updated successfully! Please log in.")
        return redirect(url_for('public.login'))  # Redirect to login page

    return render_template('reset_password.html')


if __name__ == '__main__':
    app.run(debug=True)
