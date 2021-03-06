from django import forms
from cashier.models import PaymentRecord, OrderRecord, OrderItem, Member


class PaymentRecordForm(forms.ModelForm):

    class Meta:
        model = PaymentRecord
        #my form dont want contain the following fields
        exclude = ['active','pay_status','price_type']


class OrderRecordForm(forms.ModelForm):
	class Meta:
		model = OrderRecord
		exclude = ['active']


class OrderItemForm(forms.ModelForm):
	class Meta:
		model = OrderItem
		fields = '__all__'


class MemberForm(forms.ModelForm):
	class Meta:
		model = Member
		exclude = ['active']