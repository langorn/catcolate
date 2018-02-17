from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages 

from django.db.models import Q, Sum
from django.core import serializers
import json

from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from django.utils.functional import Promise
from django.utils.encoding import force_text
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from cashier.forms import PaymentRecordForm, OrderItemForm, OrderRecordForm, MemberForm
from cashier.models import PaymentRecord, Product, OrderItem, OrderRecord, Product

import datetime
import time
# Create your views here.
PER_HRS = 6
MEMBER_PRICE = 5
WOLF_PRICE = 4

PRICE_TYPE = {
	1:6,
	2:5,
	3:4
}
###
# state of pay_status
# 0 = new created 
# 1 = hold
# 2 = payed
# 3 = cancel bill
###

def dashboard(request):
	return render(request, 'cashier.html')

def add_payment_record(request):
	if request.method =='POST':

		#get the table_no
		data = request.body.decode('utf-8')
		payment_set = json.loads(data)

		form = PaymentRecordForm(request.POST)
		if form.is_valid():
			newbook = form.save(commit=False)
			newbook.name = "non_member"
			newbook.start_from = datetime.datetime.now()
			newbook.end_time = None
			newbook.pay_status = 0
			newbook.card_no = 0
			newbook.table_no = payment_set['table_no']
			newbook.price_type = "1"
			# newbook.active = True
			newbook.save()
		else:
			messages.error(request, "Error")
	else:
		pass

	return HttpResponse()

def edit_bill(request,payment_id):
	payment = PaymentRecord.objects.get(pk=payment_id)
	data = request.body.decode('utf-8')
	payment_set = json.loads(data)
	order_list = ','.join(map(str,payment_set['orders']))

	payment.orders = order_list
	payment.save()

	return HttpResponse()

def change_time(request, payment_id):
	payment = PaymentRecord.objects.get(pk=1)
	data = request.body.decode('utf-8')
	payment_set = json.loads(data)
	print payment_set
	payment.start_from = payment_set['time']
	# order_list = ','.join(map(str,payment_set['orders']))
	# console.log(order_list)
	# console.log(payment_set)
	# payment.orders = order_list
	payment.save()

	return HttpResponse()

def card_update(request, payment_id):
	payment = PaymentRecord.objects.get(pk=payment_id)
	data = request.body.decode('utf-8')
	payment_set = json.loads(data)
	payment.card_no = payment_set['card_no']
	payment.save()

	return HttpResponse()

def remark_update(request, payment_id):
	payment = PaymentRecord.objects.get(pk=payment_id)
	data = request.body.decode('utf-8')
	payment_set = json.loads(data)
	payment.remark = payment_set['remark']
	payment.save()

	return HttpResponse()

def hold_it(request):
	data = request.body.decode('utf-8')
	payment_set = json.loads(data)
	bill_id = payment_set['id']
	# print bills
	payment = PaymentRecord.objects.get(pk=bill_id)
	# print payment.pay_status
	if payment.pay_status == '0':
		# print "not 2"
		payment.pay_status = '1'
		payment.end_time = datetime.datetime.now()
		payment.save()
	elif payment.pay_status == '1':
		payment.pay_status = '0'
		payment.end_time = datetime.datetime.now()
		payment.save()
	else:
		print 'p'+ str(payment.pay_status)
		pass
	payment_state = {
		'id':bill_id, 
		'pay_status':payment.pay_status
	}
	response = JsonResponse({'data':payment_state})
	return response

def hold_bill(request):
	data = request.body.decode('utf-8')
	payment_set = json.loads(data)
	bills = payment_set['bills']

	# print bills
	payments = []

	for bill in bills:
		payment = PaymentRecord.objects.get(pk=bill)
		# print payment.pay_status
		if payment.pay_status !=2:
			# print "not 2"
			payment.pay_status = 1
			payment.end_time = datetime.datetime.now()
			payment.save()
		payments.append(payment)

	return HttpResponse()

def hold_table(request,table_id):

	start_delta = datetime.datetime.now() - datetime.timedelta(0.5)
	end_delta = datetime.datetime.now() + datetime.timedelta(0.5)

	payments = PaymentRecord.objects.filter(start_from__gte=start_delta, start_from__lte=end_delta).filter(table_no=table_id).filter(active=True).filter(Q(pay_status="0") | Q(pay_status="1"))

	for payment in payments:
		print "---->"+payment.pay_status
		if payment.pay_status == 2:
			print payment.pay_status + " = cannot save"

		else:
			
			print payment.pay_status + " = save"
			payment.pay_status = "1"
			payment.end_time = datetime.datetime.now()
			payment.save()

	result = reconstruct(payments)
	response = JsonResponse({'records':result})
	return response


def single_bill(request,payment_id):
	data = request.body.decode('utf-8')
	payment_set = json.loads(data)
	bill_no = payment_set['bill_id']
	payment = PaymentRecord.objects.get(pk=bill_no)
	payment.pay_status = 2
	payment.end_time = datetime.datetime.now()
	payment.save()

	return HttpResponse(payment_id)

def pay_bill(request):

	data = request.body.decode('utf-8')
	payment_set = json.loads(data)
	bills = payment_set['bills']


	for bill in bills:
		payment = PaymentRecord.objects.get(pk=bill)
		payment.pay_status = 2
		payment.end_time = datetime.datetime.now()
		payment.save()


		total_amount = 0
		orders = payment.orders.split(',')
		print len(orders)
		if len(orders) > 0:
			for order in orders:
				product = Product.objects.get(pk=order)

				# if member , then discount the food
				if payment.price_type == 1:
					food_price = product.promotion_price
				else:
					food_price = product.unit_price

				total_amount += food_price
				orderItem = OrderItem(product=product, unit_price=food_price, qty=1, payment_record=payment)
				orderItem.save()

		per_hrs = get_price_hrs(payment.price_type)
		console.log(per_hrs);
		form = OrderRecord(
			pay_status = payment.pay_status,
			member = payment.member,
			start_from = payment.start_from,
			end_time = payment.end_time,
			remark = payment.remark,
			orders = payment.orders,
			card_no = payment.card_no,
			table_no = payment.table_no,
			per_hrs = per_hrs,
			total_amount = total_amount)
		form.save()

	return HttpResponse()

def get_price_hrs(request, price_type):
	return PRICE_TYPE[price_type]

def pay_table(request):

	start_delta = datetime.datetime.now() - datetime.timedelta(0.5)
	end_delta = datetime.datetime.now() + datetime.timedelta(0.5)
	# records = PaymentRecord.objects.filter(start_from__gte=start_delta, start_from__lte=end_delta).filter(active=True)
	
	data = request.body.decode('utf-8')
	payment_set = json.loads(data)
	table_no = payment_set['table_no']

	payments = PaymentRecord.objects.filter(start_from__gte=start_delta, start_from__lte=end_delta).filter(table_no=table_no).filter(active=True).exclude(pay_status=2)

	total_amount = 0
	for payment in payments:
		payment.pay_status = 2
		payment.end_time = datetime.datetime.now()
		payment.save()


		orders = payment.orders.split(',')
		print "len->" + str(len(orders))
		if len(orders) > 0:
			for order in orders:
				try:
					product = Product.objects.get(pk=order)

					# if member, then discount the food order
					if payment.price_type == 1:
						food_price = product.promotion_price
					else:
						food_price = product.unit_price

					total_amount += food_price
					orderItem = OrderItem(product=product, unit_price=food_price, qty=1, payment_record=payment)
					orderItem.save()
				except:
					pass

		else:
			pass

		# use member_price or not
		# if payment.member_price is True:
		# 	per_hrs = MEMBER_PRICE
		# else:
		# 	per_hrs = PER_HRS
		per_hrs = get_price_hrs(payment.price_type)
		console.log(per_hrs);
		form = OrderRecord(
			pay_status = payment.pay_status,
			member = payment.member,
			start_from = payment.start_from,
			end_time = payment.end_time,
			remark = payment.remark,
			orders = payment.orders,
			card_no = payment.card_no,
			table_no = payment.table_no,
			per_hrs = per_hrs,
			total_amount = total_amount)
		form.save()

	return HttpResponse()

def cancel_bill(request,payment_id):
	payment = PaymentRecord.objects.get(pk=payment_id)
	payment.pay_status = 3
	payment.save()

	return HttpResponse()


def bill_json(request):
	
	start_delta = datetime.datetime.now() - datetime.timedelta(0.5)
	end_delta = datetime.datetime.now() + datetime.timedelta(0.5)

	bill = PaymentRecord.objects.filter(active=True).filter(start_from__gte=start_delta, start_from__lte=end_delta)
	bills_collection = reconstruct(bill)
	response = JsonResponse({'bills':bills_collection})
	return response

# need to recontruct format to output json
def reconstruct(items):
	items_collections = []
	for item in items:
		try:
			name = item.member.name
		except:
			name = 'non_member'

		try:
			item.end_time = 1000 * time.mktime(item.end_time.timetuple())
		except:
			item.end_time = 0

		item.orders_all = [];
		for orde in item.orders:
			print orde


		record = {
			'id': item.pk,
			'member':name,		
			'start_from': 1000 * time.mktime(item.start_from.timetuple()),
			'end_time': item.end_time ,
			'remark':item.remark,
			'pay_status':item.pay_status,
			'card_no':item.card_no,
			'table_no':item.table_no,
			'orders':item.orders,
			'member_price':item.member_price,
			'pay_status':item.pay_status,
			'price_type':item.price_type

		}
		# time.mktime(mydate.timetuple())
		items_collections.append(record)
	return items_collections


def food_construct(items):
	items_collections = []
	for item in items:
		record = {
			'id': str(item.pk),
			'name':item.name,
			'unit_price':item.unit_price,
			'promotion_price':item.promotion_price

		}
		items_collections.append(record)

	return items_collections


def payments(request):

	start_delta = datetime.datetime.now() - datetime.timedelta(0.5)
	end_delta = datetime.datetime.now() + datetime.timedelta(0.5)
	records = PaymentRecord.objects.filter(start_from__gte=start_delta, start_from__lte=end_delta).filter(active=True)
	result = reconstruct(records)
	response = JsonResponse({'records':result})
	return response


def bill_together(request):
	records = []
	data = request.body.decode('utf-8')
	payment_set = json.loads(data)
	user_lists = payment_set['user_lists']

	for user_list in user_lists:
		record = PaymentRecord.objects.filter(pk = user_list)

		result = reconstruct(record)
		records.append(result[0])

	response = JsonResponse({'records':records})

	return response

def get_table(request, table_id):
	table_id = str(table_id)

	start_delta = datetime.datetime.now() - datetime.timedelta(0.5)
	end_delta = datetime.datetime.now() + datetime.timedelta(0.5)


	if table_id == "0" or table_id == "99":
		records = PaymentRecord.objects.filter(start_from__gte=start_delta, start_from__lte=end_delta).filter(active=True).filter(Q(pay_status="0") | Q(pay_status="1"))
	else:
		records = PaymentRecord.objects.filter(start_from__gte=start_delta, start_from__lte=end_delta).filter(table_no = table_id).filter(Q(pay_status="0") | Q(pay_status="1"))
	result = reconstruct(records)
	response = JsonResponse({'records':result})

	return response

def move_table(request, payment_id):
	print request.body
	data = request.body.decode('utf-8')
	payment_set = json.loads(data)
	table_no = payment_set['table_no']

	record = PaymentRecord.objects.get(pk = payment_id)
	record.table_no = table_no
	record.save()

	return HttpResponse()


def get_card_no(request, card_no):
	start_delta = datetime.datetime.now() - datetime.timedelta(0.5)
	end_delta = datetime.datetime.now() + datetime.timedelta(0.5)


	if card_no == None:
		records = PaymentRecord.objects.filter(start_from__gte=start_delta, start_from__lte=end_delta).filter(active=True)
	else:
		records = PaymentRecord.objects.filter(start_from__gte=start_delta, start_from__lte=end_delta).filter(card_no = card_no).filter(active=True)
	result = reconstruct(records)
	response = JsonResponse({'records':result})
	return response

def foods(request):

	records = Product.objects.filter(active=True)
	result = food_construct(records)
	response = JsonResponse({'records':result})
	return response


def best_sell(request):
    records = []
    products = Product.objects.all()
    for product in products:
        order = OrderItem.objects.filter(product=product).aggregate(Sum('unit_price'))
        print '{}: {}'.format(product.name, order['unit_price__sum'])
        record = {'name':product.name , 'price':order['unit_price__sum']}
        records.append(record)
    response = JsonResponse({'records':records})
    return response

def change_pricetype(request, price_type):
	data = request.body.decode('utf-8')
	payment_set = json.loads(data)
	payment_id = payment_set['payment_id']
	table_id = payment_set['table_id']
	payment = PaymentRecord.objects.get(pk=payment_id)

	if price_type == payment.price_type:
		payment.price_type = 1
	else:
		payment.price_type = price_type
	payment.save()

	start_delta = datetime.datetime.now() - datetime.timedelta(0.5)
	end_delta = datetime.datetime.now() + datetime.timedelta(0.5)

	payments = PaymentRecord.objects.filter(start_from__gte=start_delta, start_from__lte=end_delta).filter(table_no=table_id).filter(active=True).filter(Q(pay_status="0") | Q(pay_status="1"))
	result = reconstruct(payments)	
	response = JsonResponse({'records':result})
	# response = JsonResponse({'records':payment.member_price})
	return response



def add_member(request):

	if request.method == 'POST':

		form = MemberForm(request.POST)
		if form.is_valid():
			form.save()
		else:
			print "error"
		return HttpResponseRedirect('/counter/add_member/')
	else:
		member_form = MemberForm()

	return render(request, 'add_member.html', {'form':member_form})


def reports(request, start_date, end_date):
	if request.method == 'POST':
		payments = PaymentRecord.objects.filter(start_from__gte=start_delta, start_from__lte=end_delta).filter(table_no=table_id).filter(active=True).filter(Q(pay_status="0") | Q(pay_status="1"))
	else:
		pass
	return render(request, 'reports.html')

# def update_book(request,book_id):
# 	book = Book.objects.get(pk=book_id)
# 	form = BookForm(instance=book)
# 	return render(request,'update_book.html',{'form':form,'book_id':book_id})
