from flask import *
from database import *
from werkzeug.security import generate_password_hash
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import uuid
admin=Blueprint('admin',__name__)


@admin.route('/admin_home')
def admin_homee():
    if 'login_id' in session:
        pass
    else:
        flash("You must login")
        return redirect(url_for('public.login'))
    return render_template('admin_home.html')  

# @admin.route('/admin_manage_farmer',methods=['get','post'])
# def admin_manage_farmer():
#     data={}
#     if 'login_id' in session:
#         pass
#     else:
#         flash("You must login")
#         return redirect(url_for('public.login'))
#     if 'submitbutton' in request.form:
#         fname=request.form['firstname']
#         lname=request.form['lastname']
#         city=request.form['city']
#         phone=request.form['phone']
#         email=request.form['email']
#         uname=request.form['username']
#         pwd=request.form['password']
#         confirm_password=request.form['confirm_password']
#         hashed_pwd = generate_password_hash(pwd)
#         kl="select * from login where username='%s'"%(uname)
#         gg=select(kl)
#         if gg:
#             flash("Username already exists.........!")
#         elif pwd != confirm_password:
#             flash("Password Do Not Match........!")
#         else:
#             jj="insert into login values(null,'%s','%s','farmer')"%(uname,hashed_pwd)
#             kk=insert(jj)
#             lk="insert into farmer values(null,'%s','%s','%s','%s','%s','%s')"%(kk,fname,lname,city,phone,email)
#             insert(lk)
#             flash("Registration success.......!")
#             return redirect(url_for('admin.admin_manage_farmer'))
#     user = "select * from farmer"
#     data={}
#     data['user_view'] = select(user)
#     if 'action' in request.args:
#         action=request.args['action']
#         farmer_id=request.args['farmer_id']
#         login_id=request.args['login_id']
#     else:
#         action=None  
#     if action=='delete':
#         hj="delete from farmer where farmer_id='%s'"%(farmer_id)
#         delete(hj)
#         hjj="delete from login where login_id='%s'"%(login_id)
#         delete(hjj)
#         flash("Deleted........!")
#         return redirect(url_for('admin.admin_manage_farmer'))
#     if action=='update':
#         vv="select * from farmer where farmer_id='%s'"%(farmer_id)
#         data['up']=select(vv)
#     if 'update' in request.form:
#         fname=request.form['firstname']
#         lname=request.form['lastname']
#         city=request.form['city']
#         phone=request.form['phone']
#         email=request.form['email']
#         km="update farmer set firstname='%s',lastname='%s',city='%s',phone='%s',email='%s' where farmer_id='%s' "%(fname,lname,city,phone,email,farmer_id)
#         update(km)
#         flash("Updated........!")
#         return redirect(url_for('admin.admin_manage_farmer'))
#     return render_template('admin_manage_farmer.html',data=data)  


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
        hashed_pwd = generate_password_hash(pwd)
        kl="select * from login where username='%s'"%(uname)
        gg=select(kl)
        if gg:
            flash("Username already exists.........!")
        else:
            jj="insert into login values(null,'%s','%s','farmer')"%(uname,hashed_pwd)
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


@admin.route('/admin_manage_milk_collection',methods=['get','post'])
def admin_manage_milk_collection():
    data={}
    if 'login_id' in session:
        pass
    else:
        flash("You must login")
        return redirect(url_for('public.login'))
    if 'submitbutton' in request.form:
        farmer=request.form['farmer']
        milk_in_litter=request.form['milk_in_litter']
        quality=request.form['quality']
        amount=int(milk_in_litter)*40
        zz="insert into milk_collection values(null,'%s','%s',curdate(),'%s')"%(farmer,milk_in_litter,quality)
        qq=insert(zz)
        gg = "INSERT INTO notification VALUES (NULL, '%s', '%s litter milk added', CURDATE(), 'pending')" % (farmer, milk_in_litter)
        insert(gg)
        ss="insert into payment_for_farmer values(null,'%s','%s',curdate())"%(qq,amount)
        insert(ss)
        flash("Milk collection added........!")
        return redirect(url_for('admin.admin_manage_milk_collection'))
    ff="select * from farmer"
    data['farmer']=select(ff)
    fff="select * from milk_collection inner join farmer using(farmer_id)"
    data['view']=select(fff)
    return render_template('admin_manage_milk_collection.html',data=data)  


@admin.route('/admin_manage_daily_collection', methods=['GET', 'POST'])
def admin_manage_daily_collection():
    data = {}

    # Check if the user is logged in
    if 'login_id' not in session:
        flash("You must login")
        return redirect(url_for('public.login'))

    if 'submitbutton' in request.form:
        farmer = request.form['farmer']
        milk_in_litter = request.form['milk_in_litter']
        fat = float(request.form['fat'])
        snf = float(request.form['snf'])

        # Validate Fat and SNF ranges
       

        amount = int(milk_in_litter) * 40  # Assuming price per liter is 40

        # Insert milk collection record with fat and SNF values
        zz = "INSERT INTO milk_collection VALUES (NULL, '%s', '%s', CURDATE(), '%s', '%s', '%s')" % (
            farmer, milk_in_litter, fat, snf, amount)
        qq = insert(zz)

        # Insert notification for the farmer
        gg = "INSERT INTO notification VALUES (NULL, '%s', '%s liters of milk added', CURDATE(), 'pending')" % (
            farmer, milk_in_litter)
        insert(gg)

        # Insert payment record
        ss = "INSERT INTO payment_for_farmer VALUES (NULL, '%s', '%s', CURDATE())" % (qq, amount)
        insert(ss)

        flash("Milk collection added successfully!")
        return redirect(url_for('admin.admin_manage_daily_collection'))

    # Fetch farmers
    ff = "SELECT * FROM farmer"
    data['farmer'] = select(ff)

    # Fetch milk collection records with farmer details
    fff = "SELECT * FROM milk_collection INNER JOIN farmer USING(farmer_id)"
    data['view'] = select(fff)

    return render_template('admin_daily_collection.html', data=data)

@admin.route('/admin_view_meeting')
def admin_view_meeting():
    data={}
    if 'login_id' in session:
        pass
    else:
        flash("You must login")
        return redirect(url_for('public.login'))
    dd="select * from schedule_meeting"
    data['view']=select(dd)
    return render_template('admin_view_meeting.html',data=data)  


@admin.route('/admin_view_complaint_send_reply')
def admin_view_complaint_send_reply():
    data={}
    if 'login_id' in session:
        pass
    else:
        flash("You must login")
        return redirect(url_for('public.login'))
    vv="SELECT * FROM `complaint`INNER JOIN `login`ON `login`.`login_id`=`complaint`.`sender_id`INNER JOIN `farmer`USING(login_id) UNION SELECT * FROM `complaint`INNER JOIN `login`ON `login`.`login_id`=`complaint`.`sender_id`INNER JOIN `customer`USING(login_id)"
    data['view']=select(vv)
    return render_template('admin_view_complaint_send_reply.html',data=data)  

@admin.route('/admin_send_reply',methods=['get','post'])
def admin_send_reply():
    if 'login_id' in session:
        pass
    else:
        flash("You must login")
        return redirect(url_for('public.login'))
    complaint_id=request.args['complaint_id']
    if 'submitbutton' in request.form:
        reply=request.form['reply']
        cc="update complaint set reply='%s' where complaint_id='%s' "%(reply,complaint_id)
        update(cc)
        flash("Reply sended successfully..........!")
        return redirect(url_for('admin.admin_view_complaint_send_reply'))
    return render_template('admin_send_reply.html')  


@admin.route('/admin_view_orders',methods=['get','post'])
def admin_view_orders():
    data={}
    if 'login_id' in session:
        pass
    else:
        flash("You must login")
        return redirect(url_for('public.login'))
    vv="SELECT * FROM `milk_order`INNER JOIN `customer`USING(`customer_id`)"
    data['view_order']=select(vv)
    if 'action' in request.args:
        action=request.args['action']
        milk_order_id=request.args['milk_order_id']
    else:
        action=None
    if action=='Accept':
        vv="update milk_order set status='Accept' where milk_order_id='%s'"%(milk_order_id)
        update(vv)
        flash("Accepted.........!")
        return redirect(url_for('admin.admin_view_orders'))
    if action=='Reject':
        vv="update milk_order set status='Reject' where milk_order_id='%s'"%(milk_order_id)
        update(vv)
        flash("Rejected.........!")
        return redirect(url_for('admin.admin_view_orders'))
    if action=='OutForDelivery':
        vv="update milk_order set status='Out For Delivery' where milk_order_id='%s'"%(milk_order_id)
        update(vv)
        flash("Out For Delivery.........!")
        return redirect(url_for('admin.admin_view_orders'))
    if action=='Delivered':
        vv="update milk_order set status='Delivered' where milk_order_id='%s'"%(milk_order_id)
        update(vv)
        flash("Delivered.........!")
        return redirect(url_for('admin.admin_view_orders'))
    return render_template('admin_view_orders.html',data=data)  


@admin.route('/admin_generate_report',methods=['get','post'])
def admin_generate_report():
    data={}
    if 'login_id' in session:
        pass
    else:
        flash("You must login")
        return redirect(url_for('public.login'))
    if 'submitbutton' in request.form:
        type=request.form['type']
        date=request.form['date']
        if type=="milk":
            cc="SELECT * FROM milk_collection INNER JOIN farmer USING(farmer_id) WHERE `collection_date`='%s'"%(date)
            data['milkview']=select(cc)
            print(data['milkview'],"kkkkkkkkkkkk",date)
        else:
            nn="SELECT * FROM `milk_order`INNER JOIN `customer`USING(`customer_id`) WHERE `order_date`='%s'"%(date)
            data['orderview']=select(nn)
            print(data['orderview'],"mmmmmmmmmmmmmmmmmmmmmmmmm")
    return render_template('admin_generate_report.html',data=data)  

@admin.route('/admin_manage_price',methods=['get','post'])
def admin_manage_price():
    if 'login_id' in session:
        pass
    else:
        flash("You must login")
        return redirect(url_for('public.login'))
    if 'submitbutton' in request.form:
        item=request.form['item']
        price=request.form['price']
        lk="insert into price values(null,'%s','%s')"%(item,price)
        insert(lk)
        flash("Success.......!")
        return redirect(url_for('admin.admin_manage_price'))
    user = "select * from price"
    data={}
    data['user_view'] = select(user)
    if 'action' in request.args:
        action=request.args['action']
        price_id=request.args['price_id']
    else:
        action=None  
    if action=='delete':
        hjj="delete from price where price_id='%s'"%(price_id)
        delete(hjj)
        flash("Deleted........!")
        return redirect(url_for('admin.admin_manage_price'))
    if action=='update':
        vv="select * from price where price_id='%s'"%(price_id)
        data['up']=select(vv)
    if 'update' in request.form:
        item=request.form['item']
        price=request.form['price']
        km="update price set item='%s',price='%s' where price_id='%s' "%(item,price,price_id)
        update(km)
        flash("Updated........!")
        return redirect(url_for('admin.admin_manage_price'))
    return render_template('admin_manage_price.html',data=data)  

@admin.route('/admin_manage_curd_stock',methods=['get','post'])
def admin_manage_curd_stock():
    data={}
    if 'login_id' in session:
        pass
    else:
        flash("You must login")
        return redirect(url_for('public.login'))
    if 'submitbutton' in request.form:
        stock=request.form['stock']
        lk="insert into curd_stock values(null,'%s')"%(stock)
        insert(lk)
        flash("Success.......!")
        return redirect(url_for('admin.admin_manage_curd_stock'))
    user = "select * from curd_stock"
    data={}
    data['user_view'] = select(user)
    if 'action' in request.args:
        action=request.args['action']
        curd_stock_id=request.args['curd_stock_id']
    else:
        action=None  
    if action=='delete':
        hjj="delete from curd_stock where curd_stock_id='%s'"%(curd_stock_id)
        delete(hjj)
        flash("Deleted........!")
        return redirect(url_for('admin.admin_manage_curd_stock'))
    if action=='update':
        vv="select * from curd_stock where curd_stock_id='%s'"%(curd_stock_id)
        data['up']=select(vv)
    if 'update' in request.form:
        stock=request.form['stock']
        km="update curd_stock set stock='%s' where curd_stock_id='%s' "%(stock,curd_stock_id)
        update(km)
        flash("Updated........!")
        return redirect(url_for('admin.admin_manage_curd_stock'))
    return render_template('admin_manage_curd_stock.html',data=data)  


@admin.route('/admin_view_request',methods=['get','post'])
def admin_view_request():
    data={}
    if 'login_id' in session:
        pass
    else:
        flash("You must login")
        return redirect(url_for('public.login'))
    vv="SELECT * FROM feed_request"
    data['view_order']=select(vv)
    if 'action' in request.args:
        action=request.args['action']
        feed_request_id=request.args['feed_request_id']
    else:
        action=None
    if action=='Accept':
        vv="update feed_request set status='Accept' where feed_request_id='%s'"%(feed_request_id)
        update(vv)
        flash("Accepted.........!")
        return redirect(url_for('admin.admin_view_request'))
    if action=='Reject':
        vv="update feed_request set status='Reject' where feed_request_id='%s'"%(feed_request_id)
        update(vv)
        flash("Rejected.........!")
        return redirect(url_for('admin.admin_view_request'))
    return render_template('admin_view_request.html',data=data)  



# @admin.route('/admin_manage_subsidy',methods=['get','post'])
# def admin_manage_subsidy():
#     if 'login_id' in session:
#         pass
#     else:
#         flash("You must login")
#         return redirect(url_for('public.login'))
#     if 'submitbutton' in request.form:
#         item=request.form['Subsidy']
#         price=request.form['Details']
        
        
        
        
        
#         hh = "SELECT * FROM customer"
#         xx = select(hh)

#         sender_email = "annaeldho4@gmail.com"  
#         sender_password = "fvhj ykzo epra turg" 

#         subject = "Subsidy Alert from Admin"

#         server = smtplib.SMTP('smtp.gmail.com', 587)
#         server.starttls()
#         server.login(sender_email, sender_password)

#         for i in xx:
#             receiver_email = i['email']

#             # Create email content
#             msg = MIMEMultipart()
#             msg['From'] = sender_email
#             msg['To'] = receiver_email
#             msg['Subject'] = subject
#             msg.attach(MIMEText(item, 'plain'))

#             server.sendmail(sender_email, receiver_email, msg.as_string())

#         server.quit()
#         flash("Subsidy details sent successfully!", "success")
        
#         lk="insert into subsidy values(null,'%s','%s')"%(item,price)
#         insert(lk)
#         flash("Success.......!")
#         return redirect(url_for('admin.admin_manage_subsidy'))
#     user = "select * from subsidy"
#     data={}
#     data['user_view'] = select(user)
#     if 'action' in request.args:
#         action=request.args['action']
#         price_id=request.args['Subsidy_id']
#     else:
#         action=None  
#     if action=='delete':
#         hjj="delete from subsidy where Subsidy_id='%s'"%(price_id)
#         delete(hjj)
#         flash("Deleted........!")
#         return redirect(url_for('admin.admin_manage_subsidy'))
#     if action=='update':
#         vv="select * from subsidy where Subsidy_id='%s'"%(price_id)
#         data['up']=select(vv)
#     if 'update' in request.form:
#         item=request.form['Subsidy']
#         price=request.form['Details']
#         km="update subsidy set Subsidy='%s',Details='%s' where Subsidy_id='%s' "%(item,price,price_id)
#         update(km)
#         flash("Updated........!")
#         return redirect(url_for('admin.admin_manage_subsidy'))
#     return render_template('admin_manage_subsidy.html',data=data)  




@admin.route('/admin_manage_product',methods=['get','post'])
def admin_manage_product():
    if 'login_id' in session:
        pass
    else:
        flash("You must login")
        return redirect(url_for('public.login'))
    data={}
    if 'submitbutton' in request.form:
        Product=request.form['Product']
        Price=request.form['Price']
        Quantity=request.form['Quantity']
        Image=request.files['Image']
        Description=request.form['Description']
        path="static/images/"+str(uuid.uuid4())+Image.filename
        Image.save(path)

        lk="insert into product values(null,'%s','%s','%s','%s','%s')"%(Product,Price,Quantity,path,Description)
        insert(lk)
        flash("Success.......!")
        return redirect(url_for('admin.admin_manage_product'))
    user = "select * from product"
    data={}
    data['user_view'] = select(user)
    if 'action' in request.args:
        action=request.args['action']
        product_id=request.args['product_id']
    else:
        action=None  
    if action=='delete':
        hj="delete from product where product_id='%s'"%(product_id)
        delete(hj)
        flash("Deleted........!")
        return redirect(url_for('admin.admin_manage_product'))
    if action=='update':
        vv="select * from product where product_id='%s'"%(product_id)
        data['up']=select(vv)
    if 'update' in request.form:
        Product=request.form['Product']
        Price=request.form['Price']
        Quantity=request.form['Quantity']
        Image=request.files['Image']
        Description=request.form['Description']
        path="static/images/"+str(uuid.uuid4())+Image.filename
        Image.save(path)
        km="update product set product_name='%s',price='%s',quantity='%s',description='%s',image='%s' where product_id='%s' "%(Product,Price,Quantity,Description,path,product_id)
        update(km)
        flash("Updated........!")
        return redirect(url_for('admin.admin_manage_product'))
    return render_template('admin_manage_product.html',data=data)  







@admin.route('/admin_view_feed_request',methods=['get','post'])
def admin_view_feed_request():
    if 'login_id' in session:
        pass
    else:
        flash("You must login")
        return redirect(url_for('public.login'))
    data={}
    user = "select * from feed_details"
    data={}
    data['user_view'] = select(user)
    if 'action' in request.args:
        action=request.args['action']
        product_id=request.args['product_id']
    else:
        action=None  
    
    return render_template('admin_view_feed_request.html',data=data)  



@admin.route('/admin_sent_feed_request', methods=['GET', 'POST'])
def admin_sent_feed_request():
    if 'login_id' not in session:
        flash("You must login", "danger")
        return redirect(url_for('public.login'))

    if request.method == 'POST' and 'submitbutton' in request.form:
        quantity = request.form.get('quantity')  # Get requested quantity
        product_id = request.args.get('product_id')

        if not quantity or not product_id:
            flash("Invalid request. Please provide all details.", "danger")
            return redirect(url_for('admin.admin_sent_feed_request', product_id=product_id))

        try:
            quantity = int(quantity)  # Convert to integer
            if quantity <= 0:
                flash("Invalid quantity entered!", "danger")
                return redirect(url_for('admin.admin_sent_feed_request', product_id=product_id))

            # Check current stock
            stock_query = "SELECT quantity FROM feed_details WHERE product_id = '%s'" % product_id
            stock_data = select(stock_query)

            if not stock_data or int(stock_data[0]['quantity']) < quantity:
                flash("Not enough stock available!", "danger")
                return redirect(url_for('admin.admin_sent_feed_request', product_id=product_id))

            # Insert feed request
            insert_query = "INSERT INTO feed_request (product_id, quantity, date, status) VALUES ('%s', '%s', CURDATE(), 'pending')" % (product_id, quantity)
            insert(insert_query)  # Call insert() with a single argument

            # Reduce stock quantity
            update_stock = "UPDATE feed_details SET quantity = quantity - %s WHERE product_id = '%s'" % (quantity, product_id)
            insert(update_stock)

            flash("Feed request submitted successfully!", "success")
            return redirect(url_for('admin.admin_view_feed_request', product_id=product_id))

        except ValueError:
            flash("Please enter a valid quantity!", "danger")
            return redirect(url_for('admin.admin_sent_feed_request', product_id=product_id))

    return render_template('admin_sent_feed_request.html')





@admin.route('/admin_view_subsidy_details', methods=['get', 'post'])
def admin_view_subsidy_details():
    if 'login_id' not in session:
        flash("You must login")
        return redirect(url_for('public.login'))

    # Query to get subsidy details
    user = "SELECT * FROM subsidy"
    data = {'user_view': select(user)}

    if 'action' in request.args and request.args['action'] == 'accept':
        price_id = request.args['Subsidy_id']
        title = request.args['title']
        details = request.args['details']

        # Fetching farmer details
        farmers_query = "SELECT * FROM farmer"
        farmers = select(farmers_query)

        sender_email = "annaeldho4@gmail.com"
        sender_password = "fvhj ykzo epra turg"
        subject = "Subsidy Alert from Admin"

        # Setting up the SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)

        for farmer in farmers:
            receiver_email = farmer['email']

            # Constructing the email
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = receiver_email
            msg['Subject'] = subject

            body = f"Dear Farmer,\n\nWe are pleased to inform you that the following subsidy details have been approved:\n\nTitle: {title}\nDetails: {details}\n\nBest Regards,\nAdmin"
            msg.attach(MIMEText(body, 'plain'))

            # Send email
            server.sendmail(sender_email, receiver_email, msg.as_string())

        # Close the SMTP server connection
        server.quit()

        # Flash success message and update the subsidy status
        flash("Subsidy details sent successfully!", "success")
        update_query = "UPDATE subsidy SET Subsidy_status='sent' WHERE Subsidy_id=%s" % price_id
        update(update_query)

        return redirect(url_for('admin.admin_view_subsidy_details'))

    return render_template('admin_view_subsidy_details.html', data=data)
