"""customer_info1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from app01 import views

urlpatterns = [
    url('^welcome/', views.welcome),
    url('^receivable_info/', views.receivable_info),
    url('^delete_receivable_info/', views.delete_receivable_info),
    url('^edit_receivable_info/', views.edit_receivable_info),
    url('^sale_money_info/', views.sale_money_info),
    url('^delete_sale_money_info/', views.delete_sale_money_info),
    url('^edit_sale_money_info/', views.edit_sale_money_info),
    url('^cost/', views.cost),
    url('^delete_cost_info/', views.delete_cost_info),
    url('^edit_cost_info/', views.edit_cost_info),
    url('^admin/', admin.site.urls),
    url('^login/', views.login),
    url('^user_judge/', views.user_judge),
    url('^manage_index/', views.manage_index),
    url('^all_saleman/', views.all_saleman),
    url('^delete_saleman/', views.delete_saleman),
    url('^edit_saleman/', views.edit_saleman),
    url('^add_saleman/', views.add_saleman),
    url('^all_customer/', views.all_customer),
    url('^delete_customer/', views.delete_customer),
    url('^edit_customer/', views.edit_customer),
    url('^add_customer/', views.add_customer),
    url('^saleman_welcome/', views.saleman_welcome),
    url('^saleman_receivable_info/', views.saleman_receivable_info),
    url('^delete_saleman_receivable_info/', views.delete_saleman_receivable_info),
    url('^edit_saleman_receivable_info/', views.edit_saleman_receivable_info),
    url('^saleman_sale_money_info/', views.saleman_sale_money_info),
    url('^delete_saleman_sale_money_info/', views.delete_saleman_sale_money_info),
    url('^edit_saleman_sale_money_info/', views.edit_saleman_sale_money_info),
    url('^saleman_cost/', views.saleman_cost),
    url('^customer_welcome/', views.customer_welcome),
    url('^customer_receivable_info/', views.customer_receivable_info),
    url('^delete_customer_receivable_info/', views.delete_customer_receivable_info),
    url('^edit_customer_receivable_info/', views.edit_customer_receivable_info),
    url('^customer_money_info/', views.customer_money_info),
    url('^delete_customer_sale_money_info/', views.delete_customer_sale_money_info),
    url('^edit_customer_sale_money_info/', views.edit_customer_sale_money_info),
    url('^customer_cost/', views.customer_cost),

]
