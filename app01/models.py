from django.db import models


# Create your models here.
class Customer(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    customer = models.CharField(max_length=255)
    linkman = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    number_of_employee = models.CharField(max_length=255)
    company_address = models.CharField(max_length=255)
    real_boss_and_phone = models.CharField(max_length=255)
    boss_birthday = models.DateField(auto_now=False, null=True, blank=True, )
    boss_chinese_zodiac = models.CharField(max_length=255)
    company_birthday = models.DateField(auto_now=False, null=True, blank=True, )
    area = models.CharField(max_length=255)
    saleman = models.CharField(max_length=255)
    sale_product_all_is_qb = models.CharField(max_length=255)
    other_product_name = models.CharField(max_length=255)
    total_annual_sales = models.CharField(max_length=255)
    Products_accounted_for_qb = models.CharField(max_length=255)
    Products_accounted_for_chenpi = models.CharField(max_length=255)
    Products_accounted_for_ganpucha = models.CharField(max_length=255)
    area_responsible = models.CharField(max_length=255)
    customer_level = models.CharField(max_length=255)
    task_money = models.CharField(max_length=255)
    finish_money = models.CharField(max_length=255)
    purchase_amount_of_qiyueguo = models.CharField(max_length=255)
    the_storage_amount_of_xinpi = models.CharField(max_length=255)
    the_qbproduct_sales_first = models.CharField(max_length=255)
    the_qbproduct_sales_second = models.CharField(max_length=255)
    the_qbproduct_sales_third = models.CharField(max_length=255)
    fenxiao_number_name = models.CharField(max_length=255)
    zhuangui_number_name = models.CharField(max_length=255)
    customer_specific_circumstance = models.CharField(max_length=255)
    question = models.CharField(max_length=255)
    remark = models.CharField(max_length=255)


class Manage(models.Model):
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)


class User(models.Model):
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)


class Saleman(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    superior = models.CharField(max_length=255)
    territory = models.CharField(max_length=255)
    level = models.CharField(max_length=255)
    superiorname = models.CharField(max_length=255)
    birthday = models.DateField(null=True, blank=True, )
    home_address = models.CharField(max_length=255, null=True)
    hiredate = models.DateField(null=True, blank=True, )
    resignation_time = models.DateField(null=True, blank=True, )
    salary = models.CharField(max_length=255, null=True)
    remake = models.CharField(max_length=255, null=True)


class SalemanReceivable(models.Model):
    indexdate = models.DateField(null=True, blank=True)
    saleman = models.CharField(max_length=255, null=True)
    area = models.CharField(max_length=255, null=True)
    money = models.FloatField(max_length=255, null=True)


class SalemanSaleInfo(models.Model):
    sale_date = models.DateField(null=True, blank=True)
    customer = models.CharField(max_length=255, null=True)
    product = models.CharField(max_length=255, null=True)
    product_number = models.FloatField(max_length=255, null=True)
    product_price = models.FloatField(max_length=255, null=True)
    sale_money = models.FloatField(max_length=255, null=True)
    saleman = models.CharField(max_length=255, null=True)
    area = models.CharField(max_length=255, null=True)
    remake = models.CharField(max_length=255, null=True)
    abstract = models.CharField(max_length=255, null=True)
    order_number = models.CharField(max_length=255, null=True)


class SalemanReceivableInfo(models.Model):
    date = models.DateTimeField(null=True, blank=True)
    bank = models.CharField(max_length=255, null=True)
    banking_heads = models.CharField(max_length=255, null=True)
    money = models.FloatField(max_length=255, null=True)
    customer = models.CharField(max_length=255, null=True)
    saleman = models.CharField(max_length=255, null=True)
    area = models.CharField(max_length=255, null=True)
    remake = models.CharField(max_length=255, null=True)
    earnest_money = models.FloatField(max_length=255, null=True)
    push_money = models.FloatField(max_length=255, null=True)


class CostTable(models.Model):
    date = models.DateField(blank=True,null=True)
    area = models.CharField(max_length=255, null=True)
    saleman = models.CharField(max_length=255, null=True)
    customer = models.CharField(max_length=255, null=True)
    cost_type = models.CharField(max_length=255, null=True)
    cost_number = models.FloatField(max_length=255, null=True)
    remake = models.CharField(max_length=255, null=True)

