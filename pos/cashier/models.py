from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Member(models.Model):
	name = models.CharField(max_length=200)
	created_at = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return '(%s)' % (self.name)


class Product(models.Model):
	name = models.CharField(max_length=50)
	# define the category ur self , 1= time, 2=drink, 3=food, 
	category = models.CharField(max_length=200)
	unit_price = models.DecimalField(max_digits=15, decimal_places=2, default=0)
	promotion_price = models.DecimalField(max_digits=15, decimal_places=2, default=0)
	active = models.BooleanField()
	def __unicode__(self):
		return '(%s)' % (self.name)

class PaymentRecord(models.Model):
	member = models.ForeignKey(Member, null=True, blank=True)
	start_from = models.DateTimeField(null = True, blank=True)
	remark = models.TextField(blank=True)
	end_time = models.DateTimeField(null = True, blank=True)
	orders = models.CharField(max_length=100, blank=True)
	card_no = models.IntegerField(max_length=8,default=0,null=True, blank=True)
	table_no = models.IntegerField(max_length=8,default=0,null=True, blank=True)
	pay_status = models.CharField(max_length=5,default="0")
	member_price = models.BooleanField(default=False)
	active = models.BooleanField(default=True)

	def __unicode__(self):
		return '(%s)' % (self.remark)

class OrderRecord(models.Model):
	member = models.ForeignKey(Member, null=True, blank=True)
	start_from = models.DateTimeField(null = True, blank=True)
	end_time = models.DateTimeField(null = True, blank=True)
	remark = models.TextField(blank=True)	
	orders = models.CharField(max_length=100, blank=True)
	card_no = models.IntegerField(max_length=8,default=0,null=True, blank=True)
	table_no = models.IntegerField(max_length=8,default=0,null=True, blank=True)
	per_hrs = models.DecimalField(max_digits=15, decimal_places=2, default=0)
	total_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
	pay_status = models.CharField(max_length=5,default="0")
	active = models.BooleanField(default=True)

	def __unicode__(self):
		return '(%s)' % (self.member)

class OrderItem(models.Model):
	product = models.ForeignKey(Product)
	unit_price = models.DecimalField(max_digits=15, decimal_places=2, default=0)
	qty = models.IntegerField(max_length=5)
	payment_record = models.ForeignKey(PaymentRecord,null=True,blank=True)

	def __unicode__(self):
		return '(%s)' % (self.product.name)