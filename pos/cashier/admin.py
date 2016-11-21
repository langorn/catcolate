from django.contrib import admin

# Register your models here.
from cashier.models import PaymentRecord
from cashier.models import Member
from cashier.models import OrderItem
from cashier.models import Product
from cashier.models import OrderRecord

# Register your models here.
admin.site.register(PaymentRecord)
admin.site.register(Member)
admin.site.register(OrderItem)
admin.site.register(Product)
admin.site.register(OrderRecord)