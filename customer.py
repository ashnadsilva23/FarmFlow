from flask import *
from database import *

customer=Blueprint('customer',__name__)


@customer.route('/customer_home')
def customer_home():
	if 'login_id' in session:
		data={}
		hh="select * from login where login_id='%s'"%(session['login_id'])
		data['view']=select(hh)
	else:
		flash("You must login")
		return redirect(url_for('public.login'))
	return render_template('customer_home.html',data=data)  


@customer.route('/customer_send_complaint',methods=['get','post'])
def customer_send_complaint():
	data={}
	if 'login_id' in session:
		pass
	else:
		flash("You must login")
		return redirect(url_for('public.login'))
	if 'submitbutton' in request.form:
		complaint=request.form['complaint']
		ff="insert into complaint values(null,'%s','%s','pending',curdate())"%(session['login_id'],complaint)
		insert(ff)
		flash("Coplaint sent successfully.......!")
		return redirect(url_for('customer.customer_send_complaint'))
	gh="select * from complaint where sender_id='%s'"%(session['login_id'])
	data['view']=select(gh)
	return render_template('customer_send_complaint.html',data=data)  


@customer.route('/customer_order_milk',methods=['get','post'])
def customer_order_milk():
	if 'login_id' in session:
		pass
	else:
		flash("You must login")
		return redirect(url_for('public.login'))
	if 'submitbutton' in request.form:
		item=request.form['item']
		Litter=request.form['Litter']
		address=request.form['address']
		Comments=request.form['Comments']
		kk="select * from price where item='%s'"%(item)
		ss=select(kk)
		if ss[0]['item']=='Curd':
			kk="SELECT * FROM `curd_stock`"
			rr=select(kk)
			if int(rr[0]['stock']) < int(Litter) :
				flash("Out of Stock...........!")
				return redirect(url_for('customer.customer_order_milk'))
		amount=int(Litter)*int(ss[0]['price'])
		ff="insert into milk_order values(null,'%s','%s','%s','%s','%s',curdate(),'pending','%s')"%(session['customer_id'],Litter,address,Comments,amount,item)
		milk_order_id=insert(ff)
		return redirect(url_for('customer.customer_payment',amount=amount,milk_order_id=milk_order_id))
	return render_template('customer_order_milk.html')  


@customer.route('/customer_payment',methods=['get','post'])
def customer_payment():
	if 'login_id' in session:
		pass
	else:
		flash("You must login")
		return redirect(url_for('public.login'))
	amount=request.args['amount']
	milk_order_id=request.args['milk_order_id']
	if 'btn' in request.form:
		lk="insert into payment values(null,'%s','%s',curdate())"%(milk_order_id,amount)
		insert(lk)
		gg="update milk_order set `status`='paid' where milk_order_id='%s' "%(milk_order_id)
		update(gg)
		flash("payment success........!")
		return redirect(url_for('customer.customer_home'))
	return render_template('customer_payment.html',amount=amount)  


@customer.route('/customer_view_my_order')
def customer_view_my_order():
	data={}
	if 'login_id' in session:
		pass
	else:
		flash("You must login")
		return redirect(url_for('public.login'))
	cc="SELECT * FROM `milk_order`WHERE `customer_id`='%s'"%(session['customer_id'])
	data['view']=select(cc)
	return render_template('customer_view_my_order.html',data=data)  


@customer.route('/customer_view_product')
def customer_view_product():
	if 'login_id' in session:
		pass
	else:
		flash("You must login")
		return redirect(url_for('public.login'))
	data={}
	if 'action2' in request.args:
		action=request.args['action2']
		product_id=request.args['product_id']
		price=request.args['price']
	else:
		action=None
	if action=='addtocartproduct':
		hhg="select * from master_cart where user_id='%s' and status='pending'"%(session['customer_id'])
		ss=select(hhg)
		if ss:
			book_om=ss[0]['master_cart_id']
			f="update master_cart set total=total+'%s' where master_cart_id='%s'"%(price,book_om)
			update(f)
			hjk="select * from child_cart where master_cart_id='%s' and product_id='%s'"%(book_om,product_id)
			ssd=select(hjk)
			if ssd:
				book_oc=ssd[0]['child_cart_id']
				df="update child_cart set quantity=quantity+1,amount=amount+'%s' where child_cart_id='%s'"%(price,book_oc)
				update(df)
			else:
				h="insert into child_cart values(null,'%s','%s','1','%s')"%(book_om,product_id,price)
				insert(h)
			flash("Added.......!")
			return redirect(url_for('customer.user_view_cart'))
		else:
			jj="insert into master_cart values(null,'%s','%s',curdate(),'pending')"%(session['customer_id'],price)
			res1=insert(jj)
			kk="insert into child_cart values(null,'%s','%s',1,'%s')"%(res1,product_id,price)
			insert(kk)
			flash("Added.......!")
			return redirect(url_for('customer.user_view_cart'))
	kk="select * from product"
	data['view']=select(kk)
	return render_template('customer_view_product.html',data=data)  





@customer.route('/user_view_orders')
def user_view_orders():
	if 'login_id' in session:
		data={}
		gf="SELECT *,`child_cart`.`amount` AS c_t ,`child_cart`.`quantity`as o_q FROM `master_cart` INNER JOIN `child_cart` USING (`master_cart_id`)INNER JOIN `product` ON `product`.`product_id` = `child_cart`.`product_id` where user_id='%s' and `master_cart`.`status` <>'pending' "%(session['customer_id'])
		print(gf,"iii")
		data['view_book_booking']=select(gf)
	else:
		flash("You must login")
		return redirect(url_for('public.login'))
	return render_template('user_view_orders.html',data=data)  





@customer.route('/user_view_cart')
def user_view_cart():
	if 'login_id' in session:
		data={}
		if 'actionn' in request.args:
			action = request.args['actionn']
			child_cart_id = request.args['child_cart_id']
			master_cart_id=request.args['master_cart_id']
			product_id = request.args['product_id']
			amount = request.args['amount']
		else:
			action = None
		if action == 'decrease':
			k = "select * from child_cart where child_cart_id='%s'" % (child_cart_id)
			res2 = select(k)
			if res2:
				if int(res2[0]['quantity']) == 1:
					flash("Minimum product quantity should be 1")
					return redirect(url_for('customer.user_view_cart'))
				else:
					j = "update child_cart set quantity=quantity-'1',amount=amount-'%s' where child_cart_id='%s'" % (amount,child_cart_id)
					update(j)
					k="update master_cart set total=total-'%s' where master_cart_id='%s'"%(amount,master_cart_id)
					update(k)
					return redirect(url_for('customer.user_view_cart'))
		if action == 'increase':
			kl = "select * from product where product_id='%s'" % (product_id)
			res4 = select(kl)
			stock1111 = res4[0]['quantity']
			l = "select * from child_cart where child_cart_id='%s'" % (child_cart_id)
			res3 = select(l)
			if res3:
				qty11111 = res3[0]['quantity']
				if stock1111 == qty11111:
					flash("Cart Quantity Must be Less Than Stock.")
					return redirect(url_for('customer.user_view_cart'))
				else:
					h = "update child_cart set quantity=quantity+'1',amount=amount+'%s' where  child_cart_id='%s'" % (amount,child_cart_id)
					update(h)
					k="update master_cart set total=total+'%s' where master_cart_id='%s'"%(amount,master_cart_id)
					update(k)
					return redirect(url_for('customer.user_view_cart'))
		if 'actionn1' in request.args:
			action = request.args['actionn1']
			child_cart_id = request.args['child_cart_id']
			master_cart_id=request.args['master_cart_id']
			amo=request.args['amo']
		else:
			action = None
		if action == 'remove':
			l = "delete from child_cart where child_cart_id='%s'" % (child_cart_id)
			delete(l)
			ll="select * from master_cart where master_cart_id='%s'"%(master_cart_id)
			sdd=select(ll)
			if sdd[0]['total']==amo:
				l = "delete from master_cart where master_cart_id='%s'" % (master_cart_id)
				delete(l)
				flash("Removed..........!")
				return redirect(url_for('customer.user_view_cart'))
			else:
				j="update master_cart set total=total-'%s' where master_cart_id='%s' "%(amo,master_cart_id)
				update(j)
				flash("Removed..........!")
				return redirect(url_for('customer.user_view_cart'))
		gf="SELECT *,`child_cart`.`amount` AS c_t ,`child_cart`.`quantity`as o_q FROM `master_cart` INNER JOIN `child_cart` USING (`master_cart_id`)INNER JOIN `product` ON `product`.`product_id` = `child_cart`.`product_id` where user_id='%s' and `master_cart`.`status`='pending' "%(session['customer_id'])
		data['view_book_cart']=select(gf)
	else:
		flash("You must login")
		return redirect(url_for('public.login'))
	return render_template('user_view_cart.html',data=data)   




@customer.route('/user_payment',methods=['get','post'])
def user_payment():
	if 'login_id' in session:
		total_amount=request.args['total_amount']
		master_cart_id=request.args['master_cart_id']
		if 'btn' in request.form:
			lk="insert into payments values(null,'%s','%s',curdate(),'product')"%(master_cart_id,total_amount)
			insert(lk)
			gg="update master_cart set `status`='paid' where master_cart_id='%s' "%(master_cart_id)
			update(gg)
			df="select * from child_cart where master_cart_id='%s'"%(master_cart_id)
			res1=select(df)
			for i in res1:
				product_id=int(i['product_id'])
				qtyy=int(i['quantity'])
				hjh="update product set quantity=quantity-'%s' where product_id='%s'"%(qtyy,product_id)
				update(hjh)
			flash("payment success........!")
			return redirect(url_for('customer.user_view_cart'))
	else:
		flash("You must login")
		return redirect(url_for('public.login'))
	return render_template('user_payment.html',total_amount=total_amount) 



