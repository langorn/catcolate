"""story URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include, url
from cashier.views import dashboard
from cashier import views
urlpatterns = [

    #index 
    url(r'^$',views.dashboard, name='index'),
    url(r'^bill/add/$', views.add_payment_record, name='add_bill'),
    url(r'^bill/update/(?P<payment_id>\d+)/$', views.edit_bill, name='edit_bill'),
    url(r'^bill/card/update/(?P<payment_id>\d+)/$', views.card_update, name='card_update'),
    url(r'^bill/remark/update/(?P<payment_id>\d+)/$', views.remark_update, name='remark_update'),

    url(r'^bill/hold/$', views.hold_bill, name='hold_bill'),
    url(r'^bill/hold_table/(?P<table_id>\d+)/$', views.hold_table, name='hold_table'),

    url(r'^bill/single_pay/(?P<payment_id>\d+)/$', views.single_bill, name='single_bill'),
    url(r'^bill/pay/$', views.pay_bill, name='pay_bill'),
    url(r'^bill/pay_table/$', views.pay_table, name='pay_table'),

    url(r'^bill/cancel/(?P<payment_id>\d+)/$', views.cancel_bill, name='cancel_bill'),
    url(r'^bill/card_no/(?P<card_no>\d+)/$', views.get_card_no, name='get_card_no'),
    url(r'^bill/move/(?P<payment_id>\d+)/$',views.move_table, name='move_table'),

    url(r'^bill/together/$', views.bill_together, name='bill_together'),
    url(r'^bill/membership_price/$', views.membership_price, name='membership_price'),


    #statistic
    url(r'^best_sell/$', views.best_sell, name='best_sell'),


    url(r'^payments/$', views.payments, name='payments'),
    url(r'^foods/$', views.foods, name='foods'),    
    url(r'^table/(?P<table_id>\d+)/$', views.get_table, name='get_table'),



]
