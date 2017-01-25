from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages 

from django.db.models import Q
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
from cashier.forms import PaymentRecordForm, OrderItemForm, OrderRecordForm
from cashier.models import PaymentRecord, Product, OrderItem, OrderRecord, Product
import datetime
import time
# Create your views here.
PER_HRS = 6

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


	return HttpResponse()


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
		if len(orders) > 1:
			for order in orders:
				product = Product.objects.get(pk=order)
				total_amount += product.unit_price
				orderItem = OrderItem(product=product, unit_price=product.unit_price, qty=1, payment_record=payment)
				orderItem.save()

		form = OrderRecord(
			pay_status = payment.pay_status,
			member = payment.member,
			start_from = payment.start_from,
			end_time = payment.end_time,
			remark = payment.remark,
			orders = payment.orders,
			card_no = payment.card_no,
			table_no = payment.table_no,
			per_hrs = PER_HRS,
			total_amount = total_amount)
		form.save()

	return HttpResponse()

def pay_table(request):

	start_delta = datetime.datetime.now() - datetime.timedelta(0.5)
	end_delta = datetime.datetime.now() + datetime.timedelta(0.5)
	# records = PaymentRecord.objects.filter(start_from__gte=start_delta, start_from__lte=end_delta).filter(active=True)
	
	data = request.body.decode('utf-8')
	payment_set = json.loads(data)
	table_no = payment_set['table_no']

	payments = PaymentRecord.objects.filter(start_from__gte=start_delta, start_from__lte=end_delta).filter(table_no=table_no).filter(active=True)

	total_amount = 0
	for payment in payments:
		payment.pay_status = 2
		payment.end_time = datetime.datetime.now()
		payment.save()

		orders = payment.orders.split(',')
		if len(orders) > 1:
			for order in orders:
				try:
					product = Product.objects.get(pk=order)
					total_amount += product.unit_price
					orderItem = OrderItem(product=product, unit_price=product.unit_price, qty=1, payment_record=payment)
					orderItem.save()
				except:
					pass



		form = OrderRecord(
			pay_status = payment.pay_status,
			member = payment.member,
			start_from = payment.start_from,
			end_time = payment.end_time,
			remark = payment.remark,
			orders = payment.orders,
			card_no = payment.card_no,
			table_no = payment.table_no,
			per_hrs = PER_HRS,
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
			'orders':item.orders

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
			'unit_price':item.unit_price

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

# def update_book(request,book_id):
# 	book = Book.objects.get(pk=book_id)
# 	form = BookForm(instance=book)
# 	return render(request,'update_book.html',{'form':form,'book_id':book_id})
