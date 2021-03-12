import os

import MySQLdb
import win32api
import win32con
import arrow
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect
from app01 import models as md
from django.db import connection


# Create your views here.
def login(request):
    return render(request, 'login.html')


def user_judge(request):
    if request.method == 'POST':
        user = request.POST.get('username')
        pwd = request.POST.get('password')
        captcha = request.POST.get('captcha')

        if md.User.objects.filter(name=user, password=pwd):
            request.session['user'] = user
            request.session['pwd'] = pwd
            # return redirect('/customer_list/')
            print('用户登陆成功')
        else:
            if md.Manage.objects.filter(name=user, password=pwd) and captcha == 'xszg':
                return redirect('/manage_index/')
            elif captcha != 'xszg':
                win32api.MessageBox(0, "验证码错误！！！", "登陆失败", win32con.MB_OK)
                return render(request, 'login.html')
            else:
                win32api.MessageBox(0, "账号或密码错误！！！", "登陆失败", win32con.MB_OK)
                return render(request, 'login.html')
    print(request.method)
    return render(request, 'login.html')


def welcome(request):
    six_sale_money_date = []
    month_list = []
    six_receivable_date = []
    six_cost_date = []
    six_chai_lv_cost_date = []
    six_yang_pin_cost_date = []
    six_pin_jian_cost_date = []
    six_he_xiao_cost_date = []
    product_date_name_list = []
    product_date_price_list = []
    product_number_list = [0, 1, 2, 3, 4]
    product_sql = f"SELECT id,product,sum(sale_money) sale_money FROM app01_salemansaleinfo WHERE  PERIOD_DIFF( date_format( now( ) , '%%Y%%m' ) , date_format( sale_date, '%%Y%%m' ) ) =5 GROUP BY product ORDER BY sum(sale_money) DESC LIMIT 7"
    product_date = md.SalemanSaleInfo.objects.raw(product_sql)
    for i in range(6):
        sale_money_sql = f"SELECT id,sum(sale_money) sale_money FROM app01_salemansaleinfo WHERE  PERIOD_DIFF( date_format( now( ) , '%%Y%%m' ) , date_format( sale_date, '%%Y%%m' ) ) =5-{i} "
        receivable_sql = f"SELECT id,sum(money) sum_money FROM app01_salemanreceivableinfo WHERE  PERIOD_DIFF( date_format( now( ) , '%%Y%%m' ) , date_format( date, '%%Y%%m' ) ) =5-{i} "
        cost_sql = f"SELECT id,sum(cost_number) sum_money FROM app01_costtable WHERE  PERIOD_DIFF( date_format( now( ) , '%%Y%%m' ) , date_format( date, '%%Y%%m' ) ) =5-{i} "
        chai_lv_cost_sql = f"SELECT id,sum(cost_number) sum_money FROM app01_costtable WHERE  PERIOD_DIFF( date_format( now( ) , '%%Y%%m' ) , date_format( date, '%%Y%%m' ) ) =5-{i}  and cost_type='差旅费'"
        yang_pin_cost_sql = f"SELECT id,sum(cost_number) sum_money FROM app01_costtable WHERE  PERIOD_DIFF( date_format( now( ) , '%%Y%%m' ) , date_format( date, '%%Y%%m' ) ) =5-{i} and cost_type='样品费'"
        pin_jian_cost_sql = f"SELECT id,sum(cost_number) sum_money FROM app01_costtable WHERE  PERIOD_DIFF( date_format( now( ) , '%%Y%%m' ) , date_format( date, '%%Y%%m' ) ) =5-{i} and cost_type='品鉴费'"
        he_xiao_cost_sql = f"SELECT id,sum(cost_number) sum_money FROM app01_costtable WHERE  PERIOD_DIFF( date_format( now( ) , '%%Y%%m' ) , date_format( date, '%%Y%%m' ) ) =5-{i} and cost_type='核销费'"
        month = arrow.now().shift(months=i - 5).format("YYYY-MM")
        month_list.append(month)
        print(he_xiao_cost_sql)
        sum_sale_money = md.SalemanSaleInfo.objects.raw(sale_money_sql)
        saleman_receivable = md.SalemanSaleInfo.objects.raw(receivable_sql)
        cost_number = md.CostTable.objects.raw(cost_sql)
        chai_lv_cost_number = md.CostTable.objects.raw(chai_lv_cost_sql)
        yang_pin_cost_number = md.CostTable.objects.raw(yang_pin_cost_sql)
        pin_jian_cost_number = md.CostTable.objects.raw(pin_jian_cost_sql)
        he_xiao_cost_number = md.CostTable.objects.raw(he_xiao_cost_sql)
        six_he_xiao_cost_date.append(
            0 if he_xiao_cost_number[0].sum_money is None else round(he_xiao_cost_number[0].sum_money, 2))
        six_chai_lv_cost_date.append(
            0 if chai_lv_cost_number[0].sum_money is None else round(chai_lv_cost_number[0].sum_money, 2))
        six_yang_pin_cost_date.append(
            0 if yang_pin_cost_number[0].sum_money is None else round(yang_pin_cost_number[0].sum_money, 2))
        six_pin_jian_cost_date.append(
            0 if pin_jian_cost_number[0].sum_money is None else round(pin_jian_cost_number[0].sum_money, 2))
        try:
            sum_sale_money1 = sum_sale_money[0].sale_money
            six_sale_money_date.append(round(float(sum_sale_money1), 2))
        except Exception:
            sum_sale_money = 0
            six_sale_money_date.append(sum_sale_money)
        try:
            saleman_receivable1 = saleman_receivable[0].sum_money
            six_receivable_date.append(round(saleman_receivable1, 2))
        except Exception:
            saleman_receivable = 0
            six_receivable_date.append(saleman_receivable)
        try:
            product_date_name_list.append(product_date[i].product)
            product_date_price_list.append(product_date[i].sale_money)
        except Exception:
            product_date_name_list.append('无')
            product_date_price_list.append(0)
        if cost_number[0].sum_money is not None:
            cost_money = cost_number[0].sum_money
            six_cost_date.append(round(float(cost_money), 2))
        else:
            cost_money = 0
            six_cost_date.append(cost_money)
    before_one_month_receivable = abs(six_receivable_date[3] - six_receivable_date[2])
    before_two_month_receivable = abs(six_receivable_date[3] - six_receivable_date[1])
    before_one_month_sale_money = abs(six_sale_money_date[3] - six_sale_money_date[2])
    before_two_month_sale_money = abs(six_sale_money_date[3] - six_sale_money_date[1])
    before_one_month_cost_number = abs(six_cost_date[3] - six_cost_date[2])
    before_two_month_cost_number = abs(six_cost_date[3] - six_cost_date[1])
    print(six_pin_jian_cost_date)
    return render(request, "welcome.html",
                  {'six_sale_money_date': six_sale_money_date,
                   'month_list': month_list, 'six_receivable_date': six_receivable_date,
                   'six_cost_date': six_cost_date, 'product_date_name_list': product_date_name_list,
                   'product_date_price_list': product_date_price_list, 'product_number_list': product_number_list,
                   'before_one_month_receivable': round(before_one_month_receivable, 2),
                   'before_two_month_receivable': round(before_two_month_receivable, 2),
                   'before_one_month_sale_money': round(before_one_month_sale_money, 2),
                   'before_two_month_sale_money': round(before_two_month_sale_money, 2),
                   'before_one_month_cost_number': round(before_one_month_cost_number, 2),
                   'before_two_month_cost_number': round(before_two_month_cost_number, 2),
                   'six_he_xiao_cost_date': six_he_xiao_cost_date, 'six_chai_lv_cost_date': six_chai_lv_cost_date,
                   'six_yang_pin_cost_date': six_yang_pin_cost_date, 'six_pin_jian_cost_date': six_pin_jian_cost_date})


def receivable_info(request):
    all_customer_name = md.SalemanReceivableInfo.objects.all().values('customer').distinct()
    all_saleman_name = md.SalemanReceivableInfo.objects.all().values('saleman').distinct()
    all_area_name = md.SalemanReceivableInfo.objects.all().values('area').distinct()
    money_sql = f"select id , sum(money) sum_money from app01_salemanreceivableinfo  "
    if request.method == 'GET':
        all_info = md.SalemanReceivableInfo.objects.all()
        # print(all_info[0].date)
    else:
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        customer = request.POST.get('customer')
        saleman = request.POST.get('saleman')
        area = request.POST.get('area')
        sql = f"select * from app01_salemanreceivableinfo where date (date) between if (length('{start_time}')=0 ,'2018-01-01','{start_time}' ) and if(length('{end_time}') =0,now(),'{end_time}') and saleman like '%%{saleman}%%' and customer like '%%{customer}%%'and area like '%%{area}%%' "
        money_sql = f"select id , sum(money) sum_money from app01_salemanreceivableinfo where date (date) between if (length('{start_time}')=0 ,'2018-01-01','{start_time}' ) and if(length('{end_time}') =0,now(),'{end_time}') and saleman like '%%{saleman}%%' and customer like '%%{customer}%%'and area like '%%{area}%%' "
        all_info = md.SalemanReceivableInfo.objects.raw(sql)
    sum_receivable = md.SalemanReceivableInfo.objects.raw(money_sql)[0].sum_money
    return render(request, 'receivable_info.html',
                  {'all_info': all_info, 'all_customer_name': all_customer_name, 'all_saleman_name': all_saleman_name,
                   'all_area_name': all_area_name, 'sum_receivable': sum_receivable})


def delete_receivable_info(request):
    if request.method == 'POST':
        receivable_id = request.POST.get('id')
        md.SalemanReceivableInfo.objects.filter(id=receivable_id).delete()
        return redirect('/receivable_info')


def edit_receivable_info(request):
    all_customer_name = md.SalemanReceivableInfo.objects.all().values('customer').distinct()
    all_saleman_name = md.SalemanReceivableInfo.objects.all().values('saleman').distinct()
    all_area_name = md.SalemanReceivableInfo.objects.all().values('area').distinct()
    if request.method == 'GET':
        receivable_info_id = request.GET.get('id')

        search_receivable_info = md.SalemanReceivableInfo.objects.get(id=receivable_info_id)
        return render(request, 'edit_receivable_info.html',
                      {'search_receivable_info': search_receivable_info, 'all_customer_name': all_customer_name,
                       'all_saleman_name': all_saleman_name,
                       'all_area_name': all_area_name})
    else:
        receivable_info_id = request.POST.get('id')
        customer = request.POST.get('customer')
        bank = request.POST.get('bank')
        banking_heads = request.POST.get('banking_heads')
        date = request.POST.get('date')
        money = request.POST.get('money')
        saleman = request.POST.get('saleman')
        area = request.POST.get('area')
        earnest_money = request.POST.get('earnest_money')
        push_money = request.POST.get('push_money')
        remake = request.POST.get('remake')
        judge_date = len(date)
        sql = f"UPDATE app01_salemanreceivableinfo SET customer = '{customer}' ,bank = '{bank}', banking_heads ='{banking_heads}', date = if({judge_date}=0  ,null,'{date}'),money='{money}',earnest_money='{earnest_money}',push_money='{push_money}',remake = '{remake}',saleman = '{saleman}',area = '{area}' where id = {receivable_info_id} "
        # win32api.MessageBox(0, "修改成功", "修改成功", win32con.MB_OK)
        db = MySQLdb.connect(user='root', db='customertable1', passwd='root', host='localhost', charset='utf8')
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        db.close()
        return HttpResponse('修改成功')


def sale_money_info(request):
    all_customer_name = md.SalemanSaleInfo.objects.all().values('customer').distinct()
    all_product_name = md.SalemanSaleInfo.objects.all().values('product').distinct()
    all_saleman_name = md.SalemanSaleInfo.objects.all().values('saleman').distinct()
    all_area_name = md.SalemanSaleInfo.objects.all().values('area').distinct()
    sum_sql = "select id,sum(sale_money) sum_money from app01_salemansaleinfo"
    if request.method == 'GET':
        all_info = md.SalemanSaleInfo.objects.all()
    else:
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        customer = request.POST.get('customer')
        product = request.POST.get('product')
        saleman = request.POST.get('saleman')
        area = request.POST.get('area')
        sql = f"select * from app01_salemansaleinfo where date (sale_date) between if (length('{start_time}')=0 ,'2018-01-01','{start_time}' ) and if(length('{end_time}') =0,now(),'{end_time}') and saleman like '%%{saleman}%%' and customer like '%%{customer}%%'and product like '%%{product}%%'and saleman like '%%{saleman}%%'and area like '%%{area}%%'"
        sum_sql = f"select id,sum(sale_money) sum_money from app01_salemansaleinfo where date (sale_date) between if (length('{start_time}')=0 ,'2018-01-01','{start_time}' ) and if(length('{end_time}') =0,now(),'{end_time}') and saleman like '%%{saleman}%%' and customer like '%%{customer}%%'and product like '%%{product}%%'and saleman like '%%{saleman}%%'and area like '%%{area}%%'"
        all_info = md.SalemanSaleInfo.objects.raw(sql)
    sum_money = md.SalemanSaleInfo.objects.raw(sum_sql)[0].sum_money
    return render(request, 'sale_money_info.html',
                  {'all_info': all_info, 'all_customer_name': all_customer_name, 'all_product_name': all_product_name,
                   'all_saleman_name': all_saleman_name, 'all_area_name': all_area_name, 'sum_money': sum_money})


def delete_sale_money_info(request):
    if request.method == 'POST':
        sale_money_info_id = request.POST.get('id')
        md.SalemanSaleInfo.objects.filter(id=sale_money_info_id).delete()
        return redirect('/sale_money_info')


def edit_sale_money_info(request):
    all_customer_name = md.SalemanSaleInfo.objects.all().values('customer').distinct()
    all_product_name = md.SalemanSaleInfo.objects.all().values('product').distinct()
    all_saleman_name = md.SalemanSaleInfo.objects.all().values('saleman').distinct()
    all_area_name = md.SalemanSaleInfo.objects.all().values('area').distinct()
    if request.method == 'GET':
        sale_money_info_id = request.GET.get('id')
        search_sale_money_info = md.SalemanSaleInfo.objects.get(id=sale_money_info_id)
        return render(request, 'edit_sale_money_info.html',
                      {'search_sale_money_info': search_sale_money_info, 'all_customer_name': all_customer_name,
                       'all_product_name': all_product_name,
                       'all_saleman_name': all_saleman_name, 'all_area_name': all_area_name})
    else:
        sale_money_info_id = request.POST.get('id')
        customer = request.POST.get('customer')
        date = request.POST.get('date')
        product = request.POST.get('product')
        number = request.POST.get('number')
        price = request.POST.get('price')
        sale_money = request.POST.get('sale_money')
        remake = request.POST.get('remake')
        judge_date = len(date)
        sql = f"UPDATE app01_salemansaleinfo SET customer = '{customer}' ,product = '{product}', product_number ='{number}', sale_date = if({judge_date}=0  ,null,'{date}'),product_price='{price}',sale_money='{sale_money}',remake = '{remake}' where id = {sale_money_info_id} "
        # win32api.MessageBox(0, "修改成功", "修改成功", win32con.MB_OK)
        db = MySQLdb.connect(user='root', db='customertable1', passwd='root', host='localhost', charset='utf8')
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        db.close()
        return HttpResponse('修改成功')


def cost(request):
    all_type = md.CostTable.objects.all().values('cost_type').distinct()
    all_area = md.CostTable.objects.all().values('area').distinct()
    all_saleman_name = md.CostTable.objects.all().values('saleman').distinct()
    all_customer_name = md.CostTable.objects.all().values('customer').distinct()
    all_cost_info = md.CostTable.objects.all()
    cost_sum = md.CostTable.objects.aggregate(sum=Sum('cost_number'))['sum']
    if request.method == 'POST':
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        saleman = request.POST.get('saleman')
        customer = request.POST.get('customer')
        cost_type = request.POST.get('type')
        area = request.POST.get('area')
        sql = f"select * from app01_costtable where date (date) between if (length('{start_time}')=0 ,'2018-01-01','{start_time}' ) and if(length('{end_time}') =0,now(),'{end_time}') and if(length('{customer}')=0,ISNULL(customer),customer='{customer}' ) and saleman like '%%{saleman}%%' and area like '%%{area}%%'and cost_type like '%%{cost_type}%%'"
        money_sql = f"select id, sum(cost_number) cost_sum from app01_costtable where date (date) between if (length('{start_time}')=0 ,'2018-01-01','{start_time}' ) and if(length('{end_time}') =0,now(),'{end_time}') and if(length('{customer}')=0,ISNULL(customer),customer='{customer}' ) and saleman like '%%{saleman}%%' and area like '%%{area}%%'and cost_type like '%%{cost_type}%%'"

        all_cost_info = md.CostTable.objects.raw(sql)
        cost_sum = md.CostTable.objects.raw(money_sql)[0].cost_sum
        print(money_sql)
    return render(request, 'cost.html',
                  {'all_type': all_type, 'all_area': all_area, 'all_saleman_name': all_saleman_name,
                   'all_customer_name': all_customer_name, 'all_cost_info': all_cost_info,
                   'cost_sum': cost_sum})


def delete_cost_info(request):
    if request.method == 'POST':
        cost_info_id = request.POST.get('id')
        md.CostTable.objects.filter(id=cost_info_id).delete()
        return redirect('/cost')


def edit_cost_info(request):
    all_type = md.CostTable.objects.all().values('cost_type').distinct()
    all_area = md.CostTable.objects.all().values('area').distinct()
    all_saleman_name = md.CostTable.objects.all().values('saleman').distinct()
    all_customer_name = md.CostTable.objects.all().values('customer').distinct()
    if request.method == 'GET':
        cost_info_id = request.GET.get('id')
        search_cost_info = md.CostTable.objects.get(id=cost_info_id)
        return render(request, 'edit_cost_info.html',
                      {'search_cost_info': search_cost_info, 'all_type': all_type, 'all_area': all_area,
                       'all_saleman_name': all_saleman_name,
                       'all_customer_name': all_customer_name})
    else:
        cost_info_id = request.POST.get('id')
        saleman = request.POST.get('saleman')
        customer = request.POST.get('customer')
        cost_type = request.POST.get('type')
        date = request.POST.get('date')
        cost_number = request.POST.get('cost_number')
        remake = request.POST.get('remake')
        judge_date = len(date)
        sql = f"UPDATE app01_costtable SET customer = '{customer}' ,saleman = '{saleman}', cost_number ='{cost_number}', date = if({judge_date}=0  ,null,'{date}'),cost_type='{cost_type}',remake = '{remake}' where id = {cost_info_id} "
        # win32api.MessageBox(0, "修改成功", "修改成功", win32con.MB_OK)
        db = MySQLdb.connect(user='root', db='customertable1', passwd='root', host='localhost', charset='utf8')
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        db.close()
        return HttpResponse('修改成功')


def manage_index(request):
    return render(request, 'admin.html')


def all_saleman(request):
    sql1 = f"SELECT id, name, territory,superiorname FROM app01_saleman"
    search_territory = md.Saleman.objects.all().values('territory').distinct()
    if request.method == 'GET':
        all_search_saleman = md.Saleman.objects.raw(sql1)
    else:
        territory = request.POST.get('territory')
        sql = f"SELECT id, name, territory,superiorname FROM app01_saleman  where  territory like '%%{territory}%%' "
        # print(sql)
        print(territory, type(territory))
        if territory is not None:
            all_search_saleman = md.Saleman.objects.raw(sql)
            # print(sql)
            # print(all_search_saleman[0].name)
        else:
            all_search_saleman = md.Saleman.objects.raw(sql1)
    # print(all_search_saleman[0].name)
    return render(request, 'saleman/all_saleman.html',
                  {'all_search_saleman': all_search_saleman, 'search_territory': search_territory})


def delete_saleman(request):
    if request.method == 'POST':
        saleman_id = request.POST.get('id')
        md.Saleman.objects.filter(id=saleman_id).delete()
        return redirect('/all_saleman')


def edit_saleman(request):
    # saleman_id = request.POST.get('id')
    if request.method == 'GET':
        saleman_id = request.GET.get('id')
        # print(sql)
        # print(saleman_id)
        # print(saleman_id2)
        search_saleman = md.Saleman.objects.get(id=saleman_id)
        all_superiorname = md.Saleman.objects.all().values('superiorname').distinct()
        all_territory = md.Saleman.objects.all().values('territory').distinct()
        all_level = md.Saleman.objects.all().values('level').distinct()
        # print(all_territory[0])
        # print(search_saleman.name)
        # print(search_territory[0].superior)
        return render(request, 'saleman/edit_saleman.html',
                      {'search_saleman': search_saleman, 'all_superiorname': all_superiorname,
                       'all_territory': all_territory, 'all_level': all_level})
    else:
        saleman_id = request.POST.get('saleman_id')
        saleman_name = request.POST.get('saleman_name')
        territory = request.POST.get('territory')
        superiorname = request.POST.get('superiorname')
        saleman_level = request.POST.get('saleman_level')
        birthday = request.POST.get('birthday')
        hiredate = request.POST.get('hiredate')
        resignation_time = request.POST.get('resignation_time')
        home_address = request.POST.get('home_address')
        salary = request.POST.get('salary')
        remake = request.POST.get('remake')

        # saleman = md.Saleman.objects.get(id=saleman_id)
        # saleman.name = saleman_name
        # saleman.territory = territory
        # saleman.superiorname = superiorname
        # saleman.level = saleman_level
        # saleman.birthday = birthday
        # saleman.save()
        judge_birthday = len(birthday)
        judge_hiredate = len(hiredate)
        judge_resignation_time = len(resignation_time)
        sql = f"UPDATE app01_saleman SET customertable1.app01_saleman.name = '{saleman_name}' ,territory = '{territory}', customertable1.app01_saleman.superiorname ='{superiorname}',level = {saleman_level} , birthday = if({judge_birthday}=0  ,null,'{birthday}'),hiredate=if({judge_hiredate}=0  ,null,'{hiredate}'),resignation_time=if({judge_resignation_time}=0  ,null,'{resignation_time}'),home_address='{home_address}',salary='{salary}',remake = '{remake}' where id = {saleman_id} "
        # win32api.MessageBox(0, "修改成功", "修改成功", win32con.MB_OK)
        db = MySQLdb.connect(user='root', db='customertable1', passwd='root', host='localhost', charset='utf8')
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        db.close()
        return HttpResponse('修改成功')


def add_saleman(request):
    if request.method == 'GET':
        saleman_number = len(md.Saleman.objects.all())
        # print(saleman_number)
        index = md.Saleman.objects.all()[saleman_number - 1].id
        # print(index)
        saleman_id = index + 1
        all_superiorname = md.Saleman.objects.all().values('superiorname').distinct()
        all_territory = md.Saleman.objects.all().values('territory').distinct()
        all_level = md.Saleman.objects.all().values('level').distinct()
        return render(request, 'saleman/add_saleman.html',
                      {'saleman_id': saleman_id, 'all_superiorname': all_superiorname, 'all_territory': all_territory,
                       'all_level': all_level})
    else:
        saleman_id = request.POST.get('saleman_id')
        saleman_name = request.POST.get('saleman_name')
        territory = request.POST.get('territory')
        superiorname = request.POST.get('superiorname')
        saleman_level = request.POST.get('saleman_level')
        birthday = request.POST.get('birthday')
        hiredate = request.POST.get('hiredate')
        resignation_time = request.POST.get('resignation_time')
        home_address = request.POST.get('home_address')
        salary = request.POST.get('salary')
        remake = request.POST.get('remake')
        sql = f"SELECT id  FROM app01_saleman  WHERE name like '%%{superiorname}%%' "
        superior = md.Saleman.objects.raw(sql)[0].id
        judge_birthday = len(birthday)
        judge_hiredate = len(hiredate)
        judge_resignation_time = len(resignation_time)
        add_sql = f"insert into customertable1.app01_saleman values ('{saleman_id}','{saleman_name}','{territory}','{superior}','{saleman_level}','{superiorname}',if({judge_birthday}=0,null,'{birthday}'),if({judge_hiredate}=0,null,'{hiredate}'),'{home_address}',if({judge_resignation_time}=0,null,'{resignation_time}'),'{salary}'),'{remake}'"
        # print(add_sql)
        db = MySQLdb.connect(user='root', db='customertable1', passwd='root', host='localhost', charset='utf8')
        cursor = connection.cursor()
        cursor.execute(add_sql)
        connection.commit()
        db.close()
        return HttpResponse('添加成功')


def all_customer(request):
    all_search_customer = md.Customer.objects.all()
    search_all_customer = md.Customer.objects.all().values('customer').distinct()
    search_customer_level = md.Customer.objects.all().values('customer_level').distinct()
    search_all_saleman = md.Customer.objects.all().values('saleman').distinct()
    search_all_area = md.Customer.objects.all().values('area').distinct()
    search_boss_chinese_zodiac = md.Customer.objects.all().values('boss_chinese_zodiac').distinct()
    boss_birthday_list = []
    for i in range(1, 13):
        boss_birthday_list.append(i)
    boss_birthday_list.append('NULL')
    if request.method == 'POST':
        customer = request.POST.get('customer')
        level = request.POST.get('level')
        area = request.POST.get('area')
        saleman = request.POST.get('saleman')
        boss_birthday = request.POST.get('boss_birthday')
        ShengXiao = request.POST.get('ShengXiao')
        company_birthday = request.POST.get('company_birthday')
        search_dict = {}
        if customer:
            search_dict['customer'] = customer
        if level:
            search_dict['customer_level'] = level
        if area:
            search_dict['area'] = area
        if saleman:
            search_dict['saleman'] = saleman
        if boss_birthday:
            search_dict['boss_birthday__month'] = boss_birthday
        if ShengXiao:
            search_dict['boss_chinese_zodiac'] = ShengXiao
        if company_birthday:
            search_dict['company_birthday__month'] = company_birthday
        all_search_customer = md.Customer.objects.filter(**search_dict)
    return render(request, 'customer/all_customer.html',
                  {'all_search_customer': all_search_customer, 'search_customer_level': search_customer_level,
                   'search_all_saleman': search_all_saleman, 'search_all_area': search_all_area,
                   'search_boss_chinese_zodiac': search_boss_chinese_zodiac,
                   'search_all_customer': search_all_customer, 'boss_birthday_list': boss_birthday_list})


def delete_customer(request):
    if request.method == 'POST':
        customer_id = request.POST.get('id')
        # print(customer_id)
        md.Customer.objects.filter(id=customer_id).delete()
        return redirect('/all_customer')


def edit_customer(request):
    if request.method == 'GET':
        customer_id = request.GET.get('customer_id')
        search_customer_level = md.Customer.objects.all().values('customer_level').distinct()
        search_all_saleman = md.Customer.objects.all().values('saleman').distinct()
        search_all_area = md.Customer.objects.all().values('area').distinct()
        search_boss_chinese_zodiac = md.Customer.objects.all().values('boss_chinese_zodiac').distinct()
        search_sale_product_all_is_qb = md.Customer.objects.all().values('sale_product_all_is_qb').distinct()
        search_customer_info = md.Customer.objects.get(id=customer_id)
        # print(search_customer_info.boss_birthday, type(search_customer_info.boss_birthday))
        return render(request, 'customer/edit_customer.html',
                      {'customer_info': search_customer_info, 'search_customer_level': search_customer_level,
                       'search_all_saleman': search_all_saleman, 'search_all_area': search_all_area,
                       'search_boss_chinese_zodiac': search_boss_chinese_zodiac,
                       'search_sale_product_all_is_qb': search_sale_product_all_is_qb})
    else:
        customer_id = request.POST.get('id')
        # print(customer_id)
        area = request.POST.get('area')
        saleman = request.POST.get('saleman')
        customer = request.POST.get('customer')
        linkman = request.POST.get('linkman')
        phone_number = request.POST.get('phone_number')
        company_address = request.POST.get('company_address')
        number_of_employee = request.POST.get('number_of_employee')
        real_boss_and_phone = request.POST.get('real_boss_and_phone')
        boss_birthday = request.POST.get('boss_birthday')
        boss_chinese_zodiac = request.POST.get('boss_chinese_zodiac')
        company_birthday = request.POST.get('company_birthday')
        sale_product_all_is_qb = request.POST.get('sale_product_all_is_qb')
        other_product_name = request.POST.get('other_product_name')
        total_annual_sales = request.POST.get('total_annual_sales')
        Products_accounted_for_qb = request.POST.get('Products_accounted_for_qb')
        Products_accounted_for_chenpi = request.POST.get('Products_accounted_for_chenpi')
        Products_accounted_for_ganpucha = request.POST.get('Products_accounted_for_ganpucha')
        area_responsible = request.POST.get('area_responsible')
        customer_level = request.POST.get('customer_level')
        task_money = request.POST.get('task_money')
        finish_money = request.POST.get('finish_money')
        purchase_amount_of_qiyueguo = request.POST.get('purchase_amount_of_qiyueguo')
        the_storage_amount_of_xinpi = request.POST.get('the_storage_amount_of_xinpi')
        the_qbproduct_sales_first = request.POST.get('the_qbproduct_sales_first')
        the_qbproduct_sales_second = request.POST.get('the_qbproduct_sales_second')
        the_qbproduct_sales_third = request.POST.get('the_qbproduct_sales_third')
        fenxiao_number_name = request.POST.get('fenxiao_number_name')
        zhuangui_number_name = request.POST.get('zhuangui_number_name')
        customer_specific_circumstance = request.POST.get('customer_specific_circumstance')
        question = request.POST.get('question')
        remark = request.POST.get('remark')
        judge_boss_birthday = len(boss_birthday)
        judge_company_birthday = len(company_birthday)
        sql = f"UPDATE customertable1.app01_customer SET area = '{area}' ,saleman = '{saleman}', customer='{customer}',linkman = '{linkman}' ,phone_number = '{phone_number}' ,company_address = '{company_address}' ,number_of_employee = '{number_of_employee}' ,real_boss_and_phone = '{real_boss_and_phone}' ,boss_chinese_zodiac = '{boss_chinese_zodiac}' ,sale_product_all_is_qb = '{sale_product_all_is_qb}' ,other_product_name = '{other_product_name}' ,total_annual_sales = '{total_annual_sales}' ,Products_accounted_for_qb = '{Products_accounted_for_qb}' ,Products_accounted_for_chenpi = '{Products_accounted_for_chenpi}' ,Products_accounted_for_ganpucha = '{Products_accounted_for_ganpucha}' ,area_responsible = '{area_responsible}' ,customer_level = '{customer_level}' ,task_money = '{task_money}' ,finish_money = '{finish_money}' ,purchase_amount_of_qiyueguo = '{purchase_amount_of_qiyueguo}' ,the_storage_amount_of_xinpi = '{the_storage_amount_of_xinpi}' ,the_qbproduct_sales_first = '{the_qbproduct_sales_first}' ,the_qbproduct_sales_second = '{the_qbproduct_sales_second}' ,the_qbproduct_sales_third = '{the_qbproduct_sales_third}' ,fenxiao_number_name = '{fenxiao_number_name}' ,zhuangui_number_name = '{zhuangui_number_name}' ,customer_specific_circumstance = '{customer_specific_circumstance}' ,question = '{question}' ,remark = '{remark}' , boss_birthday = if({judge_boss_birthday}=0  ,null,'{boss_birthday}'),company_birthday=if({judge_company_birthday}=0  ,null,'{company_birthday}') where id = {customer_id} "

        print(sql)
        db = MySQLdb.connect(user='root', db='customertable1', passwd='root', host='localhost', charset='utf8')
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        db.close()

        return HttpResponse('修改成功')


def add_customer(request):
    if request.method == 'GET':
        search_customer_level = md.Customer.objects.all().values('customer_level').distinct()
        search_all_saleman = md.Customer.objects.all().values('saleman').distinct()
        search_all_area = md.Customer.objects.all().values('area').distinct()
        search_boss_chinese_zodiac = md.Customer.objects.all().values('boss_chinese_zodiac').distinct()
        search_sale_product_all_is_qb = md.Customer.objects.all().values('sale_product_all_is_qb').distinct()
        return render(request, 'customer/add_customer.html',
                      {'search_customer_level': search_customer_level, 'search_all_saleman': search_all_saleman,
                       'search_all_area': search_all_area,
                       'search_boss_chinese_zodiac': search_boss_chinese_zodiac,
                       'search_sale_product_all_is_qb': search_sale_product_all_is_qb})
    else:
        customer_number = len(md.Customer.objects.all())
        # print(customer_number)
        index = md.Customer.objects.all()[customer_number - 1].id
        # print(index)
        customer_id = index + 1
        area = request.POST.get('area')
        saleman = request.POST.get('saleman')
        customer = request.POST.get('customer')
        linkman = request.POST.get('linkman')
        phone_number = request.POST.get('phone_number')
        company_address = request.POST.get('company_address')
        number_of_employee = request.POST.get('number_of_employee')
        real_boss_and_phone = request.POST.get('real_boss_and_phone')
        boss_birthday = request.POST.get('boss_birthday')
        boss_chinese_zodiac = request.POST.get('boss_chinese_zodiac')
        company_birthday = request.POST.get('company_birthday')
        sale_product_all_is_qb = request.POST.get('sale_product_all_is_qb')
        other_product_name = request.POST.get('other_product_name')
        total_annual_sales = request.POST.get('total_annual_sales')
        Products_accounted_for_qb = request.POST.get('Products_accounted_for_qb')
        Products_accounted_for_chenpi = request.POST.get('Products_accounted_for_chenpi')
        Products_accounted_for_ganpucha = request.POST.get('Products_accounted_for_ganpucha')
        area_responsible = request.POST.get('area_responsible')
        customer_level = request.POST.get('customer_level')
        task_money = request.POST.get('task_money')
        finish_money = request.POST.get('finish_money')
        purchase_amount_of_qiyueguo = request.POST.get('purchase_amount_of_qiyueguo')
        the_storage_amount_of_xinpi = request.POST.get('the_storage_amount_of_xinpi')
        the_qbproduct_sales_first = request.POST.get('the_qbproduct_sales_first')
        the_qbproduct_sales_second = request.POST.get('the_qbproduct_sales_second')
        the_qbproduct_sales_third = request.POST.get('the_qbproduct_sales_third')
        fenxiao_number_name = request.POST.get('fenxiao_number_name')
        zhuangui_number_name = request.POST.get('zhuangui_number_name')
        customer_specific_circumstance = request.POST.get('customer_specific_circumstance')
        question = request.POST.get('question')
        remark = request.POST.get('remark')
        judge_boss_birthday = len(boss_birthday)
        judge_company_birthday = len(company_birthday)
        sql = f"insert into app01_customer values ('{customer_id}','{customer}','{linkman}','{area}','{saleman}','{phone_number}','{number_of_employee}','{company_address}','{real_boss_and_phone}',if({judge_boss_birthday}=0,null,'{boss_birthday}'),'{boss_chinese_zodiac}',if({judge_company_birthday}=0,null,'{company_birthday}'),'{sale_product_all_is_qb}','{other_product_name}','{total_annual_sales}','{Products_accounted_for_qb}','{Products_accounted_for_chenpi}','{Products_accounted_for_ganpucha}','{area_responsible}','{customer_level}','{task_money}','{finish_money}','{purchase_amount_of_qiyueguo}','{the_storage_amount_of_xinpi}','{the_qbproduct_sales_first}','{the_qbproduct_sales_second}','{the_qbproduct_sales_third}','{fenxiao_number_name}','{zhuangui_number_name}','{customer_specific_circumstance}','{question}','{remark}')"
        print(sql)
        db = MySQLdb.connect(user='root', db='customertable1', passwd='root', host='localhost', charset='utf8')
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        db.close()

        return HttpResponse('添加成功')


def saleman_welcome(request):
    saleman_name = request.GET.get('saleman_name')
    request.session['saleman'] = saleman_name
    six_sale_money_date = []
    month_list = []
    six_receivable_date = []
    six_cost_date = []
    six_chai_lv_cost_date = []
    six_yang_pin_cost_date = []
    six_pin_jian_cost_date = []
    six_he_xiao_cost_date = []
    product_date_name_list = []
    product_date_price_list = []
    product_number_list = [0, 1, 2, 3, 4]
    product_sql = f"SELECT id,product,sum(sale_money) sale_money FROM app01_salemansaleinfo WHERE saleman = '{saleman_name}' and PERIOD_DIFF( date_format( now( ) , '%%Y%%m' ) , date_format( sale_date, '%%Y%%m' ) ) =5 GROUP BY product ORDER BY sum(sale_money) DESC LIMIT 7"
    # print(product_sql)
    product_date = md.SalemanSaleInfo.objects.raw(product_sql)
    for i in range(6):
        sale_money_sql = f"SELECT id,sum(sale_money) sale_money FROM app01_salemansaleinfo WHERE saleman = '{saleman_name}' and PERIOD_DIFF( date_format( now( ) , '%%Y%%m' ) , date_format( sale_date, '%%Y%%m' ) ) =5-{i} "
        receivable_sql = f"SELECT id,sum(money) sum_money FROM app01_salemanreceivableinfo WHERE saleman = '{saleman_name}' and PERIOD_DIFF( date_format( now( ) , '%%Y%%m' ) , date_format( date, '%%Y%%m' ) ) =5-{i} "
        cost_sql = f"SELECT id,sum(cost_number) sum_money FROM app01_costtable WHERE  PERIOD_DIFF( date_format( now( ) , '%%Y%%m' ) , date_format( date, '%%Y%%m' ) ) =5-{i} and saleman  = '{saleman_name}' "
        chai_lv_cost_sql = f"SELECT id,sum(cost_number) sum_money FROM app01_costtable WHERE  PERIOD_DIFF( date_format( now( ) , '%%Y%%m' ) , date_format( date, '%%Y%%m' ) ) =5-{i}  and cost_type='差旅费' and saleman = '{saleman_name}' "
        yang_pin_cost_sql = f"SELECT id,sum(cost_number) sum_money FROM app01_costtable WHERE  PERIOD_DIFF( date_format( now( ) , '%%Y%%m' ) , date_format( date, '%%Y%%m' ) ) =5-{i} and cost_type='样品费' and saleman = '{saleman_name}'"
        pin_jian_cost_sql = f"SELECT id,sum(cost_number) sum_money FROM app01_costtable WHERE  PERIOD_DIFF( date_format( now( ) , '%%Y%%m' ) , date_format( date, '%%Y%%m' ) ) =5-{i} and cost_type='品鉴费' and saleman = '{saleman_name}'"
        he_xiao_cost_sql = f"SELECT id,sum(cost_number) sum_money FROM app01_costtable WHERE  PERIOD_DIFF( date_format( now( ) , '%%Y%%m' ) , date_format( date, '%%Y%%m' ) ) =5-{i} and cost_type='核销费' and saleman = '{saleman_name}'"
        month = arrow.now().shift(months=i - 5).format("YYYY-MM")
        month_list.append(month)
        print(sale_money_sql)
        sum_sale_money = md.SalemanSaleInfo.objects.raw(sale_money_sql)
        saleman_receivable = md.SalemanSaleInfo.objects.raw(receivable_sql)
        cost_number = md.CostTable.objects.raw(cost_sql)
        chai_lv_cost_number = md.CostTable.objects.raw(chai_lv_cost_sql)
        yang_pin_cost_number = md.CostTable.objects.raw(yang_pin_cost_sql)
        pin_jian_cost_number = md.CostTable.objects.raw(pin_jian_cost_sql)
        he_xiao_cost_number = md.CostTable.objects.raw(he_xiao_cost_sql)
        six_he_xiao_cost_date.append(
            0 if he_xiao_cost_number[0].sum_money is None else round(he_xiao_cost_number[0].sum_money, 2))
        six_chai_lv_cost_date.append(
            0 if chai_lv_cost_number[0].sum_money is None else round(chai_lv_cost_number[0].sum_money, 2))
        six_yang_pin_cost_date.append(
            0 if yang_pin_cost_number[0].sum_money is None else round(yang_pin_cost_number[0].sum_money, 2))
        six_pin_jian_cost_date.append(
            0 if pin_jian_cost_number[0].sum_money is None else round(pin_jian_cost_number[0].sum_money, 2))
        try:
            sum_sale_money1 = sum_sale_money[0].sale_money
            six_sale_money_date.append(round(float(sum_sale_money1), 2))
        except Exception:
            sum_sale_money = 0
            six_sale_money_date.append(sum_sale_money)
        try:
            saleman_receivable1 = saleman_receivable[0].sum_money
            six_receivable_date.append(round(float(saleman_receivable1), 2))
        except Exception:
            saleman_receivable = 0
            six_receivable_date.append(saleman_receivable)
        try:
            product_date_name_list.append(product_date[i].product)
            product_date_price_list.append(product_date[i].sale_money)
        except Exception:
            product_date_name_list.append('无')
            product_date_price_list.append(0)
        if cost_number[0].sum_money is not None:
            cost_money = cost_number[0].sum_money
            six_cost_date.append(round(float(cost_money), 2))
        else:
            cost_money = 0
            six_cost_date.append(cost_money)
    print(six_sale_money_date)
    print(six_receivable_date)
    print(month_list)
    before_one_month_receivable = abs(six_receivable_date[3] - six_receivable_date[2])
    before_two_month_receivable = abs(six_receivable_date[3] - six_receivable_date[1])
    before_one_month_sale_money = abs(six_sale_money_date[3] - six_sale_money_date[2])
    before_two_month_sale_money = abs(six_sale_money_date[3] - six_sale_money_date[1])
    before_one_month_cost_number = abs(six_cost_date[3] - six_cost_date[2])
    before_two_month_cost_number = abs(six_cost_date[3] - six_cost_date[1])
    return render(request, "saleman/saleman_welcome.html",
                  {'saleman_name': saleman_name, 'six_sale_money_date': six_sale_money_date,
                   'month_list': month_list, 'six_receivable_date': six_receivable_date,
                   'six_cost_date': six_cost_date, 'product_date_name_list': product_date_name_list,
                   'product_date_price_list': product_date_price_list, 'product_number_list': product_number_list,
                   'before_one_month_receivable': round(before_one_month_receivable, 2),
                   'before_two_month_receivable': round(before_two_month_receivable, 2),
                   'before_one_month_sale_money': round(before_one_month_sale_money, 2),
                   'before_two_month_sale_money': round(before_two_month_sale_money, 2),
                   'before_one_month_cost_number': round(before_one_month_cost_number, 2),
                   'before_two_month_cost_number': round(before_two_month_cost_number, 2),
                   'six_he_xiao_cost_date': six_he_xiao_cost_date, 'six_chai_lv_cost_date': six_chai_lv_cost_date,
                   'six_yang_pin_cost_date': six_yang_pin_cost_date, 'six_pin_jian_cost_date': six_pin_jian_cost_date})


def saleman_receivable_info(request):
    saleman_name = request.session['saleman']
    sum_sql = f"select id,sum(money) sum_money from app01_salemanreceivableinfo where saleman = '{saleman_name}'"
    if request.method == 'GET':
        all_info = md.SalemanReceivableInfo.objects.filter(saleman=saleman_name)
        # print(all_info[0].date)
    else:
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        sql = f"select * from app01_salemanreceivableinfo where date (date) between if (length('{start_time}')=0 ,'2018-01-01','{start_time}' ) and if(length('{end_time}') =0,now(),'{end_time}') and saleman = '{saleman_name}'"
        sum_sql = f"select id,sum(money) sum_money from app01_salemanreceivableinfo where date (date) between if (length('{start_time}')=0 ,'2018-01-01','{start_time}' ) and if(length('{end_time}') =0,now(),'{end_time}') and saleman = '{saleman_name}'"
        all_info = md.SalemanReceivableInfo.objects.raw(sql)
    sum_money = md.SalemanReceivableInfo.objects.raw(sum_sql)[0].sum_money
    print(sum_money)
    return render(request, 'saleman/saleman-info/saleman_receivable_info.html',
                  {'aii_info': all_info, 'sum_money': 0 if sum_money is None else sum_money})


def delete_saleman_receivable_info(request):
    if request.method == 'POST':
        receivable_id = request.POST.get('id')
        md.SalemanReceivableInfo.objects.filter(id=receivable_id).delete()
        return redirect('/saleman_receivable_info')


def edit_saleman_receivable_info(request):
    if request.method == 'GET':
        receivable_info_id = request.GET.get('id')

        search_receivable_info = md.SalemanReceivableInfo.objects.get(id=receivable_info_id)
        return render(request, 'saleman/saleman-info/edit_saleman_receivable_info.html',
                      {'search_receivable_info': search_receivable_info})
    else:
        receivable_info_id = request.POST.get('id')
        customer = request.POST.get('customer')
        bank = request.POST.get('bank')
        banking_heads = request.POST.get('banking_heads')
        date = request.POST.get('date')
        money = request.POST.get('money')
        earnest_money = request.POST.get('earnest_money')
        push_money = request.POST.get('push_money')
        remake = request.POST.get('remake')
        judge_date = len(date)
        sql = f"UPDATE app01_salemanreceivableinfo SET customer = '{customer}' ,bank = '{bank}', banking_heads ='{banking_heads}', date = if({judge_date}=0  ,null,'{date}'),money='{money}',earnest_money='{earnest_money}',push_money='{push_money}',remake = '{remake}' where id = {receivable_info_id} "
        # win32api.MessageBox(0, "修改成功", "修改成功", win32con.MB_OK)
        db = MySQLdb.connect(user='root', db='customertable1', passwd='root', host='localhost', charset='utf8')
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        db.close()
        return HttpResponse('修改成功')


def saleman_sale_money_info(request):
    saleman_name = request.session['saleman']
    all_customer_name = md.SalemanSaleInfo.objects.filter(saleman=saleman_name).all().values('customer').distinct()
    all_product_name = md.SalemanSaleInfo.objects.filter(saleman=saleman_name).all().values('product').distinct()
    sum_sql = f"select id,sum(sale_money) sum_money from app01_salemansaleinfo where saleman = '{saleman_name}'"
    print(saleman_name)
    if request.method == 'GET':
        all_info = md.SalemanSaleInfo.objects.filter(saleman=saleman_name)
    else:
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        customer = request.POST.get('customer')
        product = request.POST.get('product')
        sql = f"select * from app01_salemansaleinfo where date (sale_date) between if (length('{start_time}')=0 ,'2018-01-01','{start_time}' ) and if(length('{end_time}') =0,now(),'{end_time}') and saleman = '{saleman_name}' and customer like '%%{customer}%%'and product like '%%{product}%%'"
        sum_sql = f"select id,sum(sale_money) sum_money from app01_salemansaleinfo where date (sale_date) between if (length('{start_time}')=0 ,'2018-01-01','{start_time}' ) and if(length('{end_time}') =0,now(),'{end_time}') and saleman = '{saleman_name}' and customer like '%%{customer}%%'and product like '%%{product}%%'"
        all_info = md.SalemanSaleInfo.objects.raw(sql)
    sum_money = md.SalemanSaleInfo.objects.raw(sum_sql)[0].sum_money
    return render(request, 'saleman/saleman-info/saleman_sale_money_info.html',
                  {'all_info': all_info, 'all_customer_name': all_customer_name, 'all_product_name': all_product_name,
                   'sum_money': sum_money})


def delete_saleman_sale_money_info(request):
    if request.method == 'POST':
        sale_money_info_id = request.POST.get('id')
        md.SalemanSaleInfo.objects.filter(id=sale_money_info_id).delete()
        return redirect('/saleman_sale_money_info')


def edit_saleman_sale_money_info(request):
    saleman_name = request.session['saleman']
    all_customer_name = md.SalemanSaleInfo.objects.filter(saleman=saleman_name).all().values('customer').distinct()
    all_product_name = md.SalemanSaleInfo.objects.filter(saleman=saleman_name).all().values('product').distinct()
    if request.method == 'GET':
        sale_money_info_id = request.GET.get('id')
        search_sale_money_info = md.SalemanSaleInfo.objects.get(id=sale_money_info_id)
        return render(request, 'saleman/saleman-info/edit_saleman_sale_money_info.html',
                      {'search_sale_money_info': search_sale_money_info, 'all_customer_name': all_customer_name,
                       'all_product_name': all_product_name})
    else:
        sale_money_info_id = request.POST.get('id')
        customer = request.POST.get('customer')
        date = request.POST.get('date')
        product = request.POST.get('product')
        number = request.POST.get('number')
        price = request.POST.get('price')
        sale_money = request.POST.get('sale_money')
        remake = request.POST.get('remake')
        judge_date = len(date)
        sql = f"UPDATE app01_salemansaleinfo SET customer = '{customer}' ,product = '{product}', product_number ='{number}', sale_date = if({judge_date}=0  ,null,'{date}'),product_price='{price}',sale_money='{sale_money}',remake = '{remake}' where id = {sale_money_info_id} "
        # win32api.MessageBox(0, "修改成功", "修改成功", win32con.MB_OK)
        db = MySQLdb.connect(user='root', db='customertable1', passwd='root', host='localhost', charset='utf8')
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        db.close()
        return HttpResponse('修改成功')


def saleman_cost(request):
    all_type = md.CostTable.objects.all().values('cost_type').distinct()
    all_area = md.CostTable.objects.all().values('area').distinct()
    all_saleman_name = md.CostTable.objects.all().values('saleman').distinct()
    all_customer_name = md.CostTable.objects.all().values('customer').distinct()
    all_cost_info = md.CostTable.objects.all().filter(saleman=request.session['saleman'])
    cost_sum = md.CostTable.objects.aggregate(sum=Sum('cost_number'))['sum']
    if request.method == 'POST':
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        saleman = request.POST.get('saleman')
        customer = request.POST.get('customer')
        cost_type = request.POST.get('type')
        area = request.POST.get('area')
        sql = f"select * from app01_costtable where date (date) between if (length('{start_time}')=0 ,'2018-01-01','{start_time}' ) and if(length('{end_time}') =0,now(),'{end_time}') and if(length('{customer}')=0,ISNULL(customer),customer='{customer}' ) and saleman like '%%{saleman}%%' and area like '%%{area}%%'and cost_type like '%%{cost_type}%%'"
        money_sql = f"select id, sum(cost_number) cost_sum from app01_costtable where date (date) between if (length('{start_time}')=0 ,'2018-01-01','{start_time}' ) and if(length('{end_time}') =0,now(),'{end_time}') and if(length('{customer}')=0,ISNULL(customer),customer='{customer}' ) and saleman like '%%{saleman}%%' and area like '%%{area}%%'and cost_type like '%%{cost_type}%%'"

        all_cost_info = md.CostTable.objects.raw(sql)
        cost_sum = md.CostTable.objects.raw(money_sql)[0].cost_sum
        print(money_sql)
    return render(request, 'saleman/saleman_cost.html',
                  {'all_type': all_type, 'all_area': all_area, 'all_saleman_name': all_saleman_name,
                   'all_customer_name': all_customer_name, 'all_cost_info': all_cost_info,
                   'cost_sum': cost_sum})


def customer_welcome(request):
    customer_name = request.GET.get('customer_name')
    request.session['customer_name'] = customer_name
    six_sale_money_date = []
    month_list = []
    six_receivable_date = []
    six_cost_date = []
    six_chai_lv_cost_date = []
    six_yang_pin_cost_date = []
    six_pin_jian_cost_date = []
    six_he_xiao_cost_date = []
    product_date_name_list = []
    product_date_price_list = []
    product_number_list = [0, 1, 2, 3, 4]
    product_sql = f"SELECT id,product,sum(sale_money) sale_money FROM app01_salemansaleinfo WHERE customer = '{customer_name}' and PERIOD_DIFF( date_format( now( ) , '%%Y%%m' ) , date_format( sale_date, '%%Y%%m' ) ) =5 GROUP BY product ORDER BY sum(sale_money) DESC LIMIT 7"
    # print(product_sql)
    product_date = md.SalemanSaleInfo.objects.raw(product_sql)
    for i in range(6):
        sale_money_sql = f"SELECT id,sum(sale_money) sale_money FROM app01_salemansaleinfo WHERE customer = '{customer_name}' and PERIOD_DIFF( date_format( now( ) , '%%Y%%m' ) , date_format( sale_date, '%%Y%%m' ) ) =5-{i} "
        receivable_sql = f"SELECT id,sum(money) sum_money FROM app01_salemanreceivableinfo WHERE customer= '{customer_name}' and PERIOD_DIFF( date_format( now( ) , '%%Y%%m' ) , date_format( date, '%%Y%%m' ) ) =5-{i} "
        cost_sql = f"SELECT id,sum(cost_number) sum_money FROM app01_costtable WHERE  PERIOD_DIFF( date_format( now( ) , '%%Y%%m' ) , date_format( date, '%%Y%%m' ) ) =5-{i} and customer = '{customer_name}' "
        chai_lv_cost_sql = f"SELECT id,sum(cost_number) sum_money FROM app01_costtable WHERE  PERIOD_DIFF( date_format( now( ) , '%%Y%%m' ) , date_format( date, '%%Y%%m' ) ) =5-{i}  and cost_type='差旅费' and customer = '{customer_name}' "
        yang_pin_cost_sql = f"SELECT id,sum(cost_number) sum_money FROM app01_costtable WHERE  PERIOD_DIFF( date_format( now( ) , '%%Y%%m' ) , date_format( date, '%%Y%%m' ) ) =5-{i} and cost_type='样品费' and customer = '{customer_name}'"
        pin_jian_cost_sql = f"SELECT id,sum(cost_number) sum_money FROM app01_costtable WHERE  PERIOD_DIFF( date_format( now( ) , '%%Y%%m' ) , date_format( date, '%%Y%%m' ) ) =5-{i} and cost_type='品鉴费' and customer = '{customer_name}'"
        he_xiao_cost_sql = f"SELECT id,sum(cost_number) sum_money FROM app01_costtable WHERE  PERIOD_DIFF( date_format( now( ) , '%%Y%%m' ) , date_format( date, '%%Y%%m' ) ) =5-{i} and cost_type='核销费' and customer = '{customer_name}'"
        month = arrow.now().shift(months=i - 5).format("YYYY-MM")
        month_list.append(month)
        sum_sale_money = md.SalemanSaleInfo.objects.raw(sale_money_sql)
        saleman_receivable = md.SalemanSaleInfo.objects.raw(receivable_sql)
        cost_number = md.CostTable.objects.raw(cost_sql)
        chai_lv_cost_number = md.CostTable.objects.raw(chai_lv_cost_sql)
        yang_pin_cost_number = md.CostTable.objects.raw(yang_pin_cost_sql)
        pin_jian_cost_number = md.CostTable.objects.raw(pin_jian_cost_sql)
        he_xiao_cost_number = md.CostTable.objects.raw(he_xiao_cost_sql)
        six_he_xiao_cost_date.append(
            0 if he_xiao_cost_number[0].sum_money is None else round(he_xiao_cost_number[0].sum_money, 2))
        six_chai_lv_cost_date.append(
            0 if chai_lv_cost_number[0].sum_money is None else round(chai_lv_cost_number[0].sum_money, 2))
        six_yang_pin_cost_date.append(
            0 if yang_pin_cost_number[0].sum_money is None else round(yang_pin_cost_number[0].sum_money, 2))
        six_pin_jian_cost_date.append(
            0 if pin_jian_cost_number[0].sum_money is None else round(pin_jian_cost_number[0].sum_money, 2))
        try:
            sum_sale_money1 = sum_sale_money[0].sale_money
            six_sale_money_date.append(round(float(sum_sale_money1), 2))
        except Exception:
            sum_sale_money = 0
            six_sale_money_date.append(sum_sale_money)

        print(saleman_receivable[0].sum_money)
        try:
            saleman_receivable1 = saleman_receivable[0].sum_money
            six_receivable_date.append(round(float(saleman_receivable1), 2))
        except Exception:
            saleman_receivable = 0
            six_receivable_date.append(saleman_receivable)
        try:
            product_date_name_list.append(product_date[i].product)
            product_date_price_list.append(product_date[i].sale_money)
        except Exception:
            product_date_name_list.append('无')
            product_date_price_list.append(0)
        if cost_number[0].sum_money is not None:
            cost_money = cost_number[0].sum_money
            six_cost_date.append(round(float(cost_money), 2))
        else:
            cost_money = 0
            six_cost_date.append(cost_money)
    print(six_cost_date)
    print(six_receivable_date)
    print(six_sale_money_date)
    before_one_month_receivable = abs(six_receivable_date[3] - six_receivable_date[2])
    before_two_month_receivable = abs(six_receivable_date[3] - six_receivable_date[1])
    before_one_month_sale_money = abs(six_sale_money_date[3] - six_sale_money_date[2])
    before_two_month_sale_money = abs(six_sale_money_date[3] - six_sale_money_date[1])
    before_one_month_cost_number = abs(six_cost_date[3] - six_cost_date[2])
    before_two_month_cost_number = abs(six_cost_date[3] - six_cost_date[1])
    return render(request, "customer/customer_welcome.html",
                  {'customer_name': customer_name, 'six_sale_money_date': six_sale_money_date,
                   'month_list': month_list, 'six_receivable_date': six_receivable_date,
                   'six_cost_date': six_cost_date, 'product_date_name_list': product_date_name_list,
                   'product_date_price_list': product_date_price_list, 'product_number_list': product_number_list,
                   'before_one_month_receivable': round(before_one_month_receivable, 2),
                   'before_two_month_receivable': round(before_two_month_receivable, 2),
                   'before_one_month_sale_money': round(before_one_month_sale_money, 2),
                   'before_two_month_sale_money': round(before_two_month_sale_money, 2),
                   'before_one_month_cost_number': round(before_one_month_cost_number, 2),
                   'before_two_month_cost_number': round(before_two_month_cost_number, 2),
                   'six_he_xiao_cost_date': six_he_xiao_cost_date, 'six_chai_lv_cost_date': six_chai_lv_cost_date,
                   'six_yang_pin_cost_date': six_yang_pin_cost_date, 'six_pin_jian_cost_date': six_pin_jian_cost_date})


def customer_receivable_info(request):
    customer_name = request.session['customer_name']
    sum_sql = f"select id, sum(money) sum_money from app01_salemanreceivableinfo where customer='{customer_name}'"
    if request.method == 'GET':
        all_info = md.SalemanReceivableInfo.objects.filter(customer=customer_name)
        # print(all_info[0].date)
    else:
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        sql = f"select * from app01_salemanreceivableinfo where date (date) between if (length('{start_time}')=0 ,'2018-01-01','{start_time}' ) and if(length('{end_time}') =0,now(),'{end_time}') and customer = '{customer_name}'"
        sum_sql = f"select  id, sum(money) sum_money from app01_salemanreceivableinfo where date (date) between if (length('{start_time}')=0 ,'2018-01-01','{start_time}' ) and if(length('{end_time}') =0,now(),'{end_time}') and customer = '{customer_name}'"
        all_info = md.SalemanReceivableInfo.objects.raw(sql)
    sum_money = md.SalemanReceivableInfo.objects.raw(sum_sql)[0].sum_money
    return render(request, 'customer/customer_info/customer_receivable_info.html',
                  {'aii_info': all_info, 'sum_money': sum_money})


def delete_customer_receivable_info(request):
    if request.method == 'POST':
        receivable_id = request.POST.get('id')
        md.SalemanReceivableInfo.objects.filter(id=receivable_id).delete()
        return redirect('/customer_receivable_info')


def edit_customer_receivable_info(request):
    # saleman_id = request.POST.get('id')
    if request.method == 'GET':
        receivable_info_id = request.GET.get('id')

        search_receivable_info = md.SalemanReceivableInfo.objects.get(id=receivable_info_id)
        return render(request, 'customer/customer_info/edit_customer_receivable_info.html',
                      {'search_receivable_info': search_receivable_info})
    else:
        receivable_info_id = request.POST.get('id')
        saleman = request.POST.get('saleman')
        bank = request.POST.get('bank')
        banking_heads = request.POST.get('banking_heads')
        date = request.POST.get('date')
        money = request.POST.get('money')
        earnest_money = request.POST.get('earnest_money')
        push_money = request.POST.get('push_money')
        remake = request.POST.get('remake')
        judge_date = len(date)
        sql = f"UPDATE app01_salemanreceivableinfo SET saleman = '{saleman}' ,bank = '{bank}', banking_heads ='{banking_heads}', date = if({judge_date}=0  ,null,'{date}'),money='{money}',earnest_money='{earnest_money}',push_money='{push_money}',remake = '{remake}' where id = {receivable_info_id} "
        # win32api.MessageBox(0, "修改成功", "修改成功", win32con.MB_OK)
        db = MySQLdb.connect(user='root', db='customertable1', passwd='root', host='localhost', charset='utf8')
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        db.close()
        return HttpResponse('修改成功')


def customer_money_info(request):
    customer_name = request.session['customer_name']
    sum_sql = f"select id, sum(sale_money) sum_money from app01_salemansaleinfo where customer='{customer_name}'"
    all_saleman_name = md.SalemanSaleInfo.objects.filter(customer=customer_name).all().values('saleman').distinct()
    all_product_name = md.SalemanSaleInfo.objects.filter(customer=customer_name).all().values('product').distinct()
    if request.method == 'GET':
        all_info = md.SalemanSaleInfo.objects.filter(customer=customer_name)
    else:
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        saleman = request.POST.get('saleman')
        product = request.POST.get('product')
        sql = f"select * from app01_salemansaleinfo where date (sale_date) between if (length('{start_time}')=0 ,'2018-01-01','{start_time}' ) and if(length('{end_time}') =0,now(),'{end_time}') and customer = '{customer_name}' and saleman like '%%{saleman}%%'and product like '%%{product}%%'"
        sum_sql = f"select id, sum(sale_money) sum_money from app01_salemansaleinfo where date (sale_date) between if (length('{start_time}')=0 ,'2018-01-01','{start_time}' ) and if(length('{end_time}') =0,now(),'{end_time}') and customer = '{customer_name}' and saleman like '%%{saleman}%%'and product like '%%{product}%%'"
        all_info = md.SalemanSaleInfo.objects.raw(sql)
    sum_money = md.SalemanSaleInfo.objects.raw(sum_sql)[0].sum_money
    return render(request, 'customer/customer_info/customer_money_info.html',
                  {'all_info': all_info, 'all_saleman_name': all_saleman_name, 'all_product_name': all_product_name,
                   'sum_money': sum_money})


def delete_customer_sale_money_info(request):
    if request.method == 'POST':
        sale_money_info_id = request.POST.get('id')
        md.SalemanSaleInfo.objects.filter(id=sale_money_info_id).delete()
        return redirect('/sale_customer_money_info')


def edit_customer_sale_money_info(request):
    # saleman_id = request.POST.get('id')
    if request.method == 'GET':
        sale_money_info_id = request.GET.get('id')
        search_sale_money_info = md.SalemanSaleInfo.objects.get(id=sale_money_info_id)
        return render(request, 'customer/customer_info/edit_customer_sale_money_info.html',
                      {'search_sale_money_info': search_sale_money_info})
    else:
        sale_money_info_id = request.POST.get('id')
        customer = request.POST.get('customer')
        date = request.POST.get('date')
        product = request.POST.get('product')
        number = request.POST.get('number')
        price = request.POST.get('price')
        sale_money = request.POST.get('sale_money')
        remake = request.POST.get('remake')
        judge_date = len(date)
        sql = f"UPDATE app01_salemansaleinfo SET customer = '{customer}' ,product = '{product}', product_number ='{number}', sale_date = if({judge_date}=0  ,null,'{date}'),product_price='{price}',sale_money='{sale_money}',remake = '{remake}' where id = {sale_money_info_id} "
        # win32api.MessageBox(0, "修改成功", "修改成功", win32con.MB_OK)
        db = MySQLdb.connect(user='root', db='customertable1', passwd='root', host='localhost', charset='utf8')
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        db.close()
        return HttpResponse('修改成功')


def customer_cost(request):
    all_type = md.CostTable.objects.all().values('cost_type').distinct()
    all_area = md.CostTable.objects.all().values('area').distinct()
    all_saleman_name = md.CostTable.objects.all().values('saleman').distinct()
    all_customer_name = md.CostTable.objects.all().values('customer').distinct()
    all_cost_info = md.CostTable.objects.all().filter(customer=request.session['customer_name'])
    cost_sum = md.CostTable.objects.aggregate(sum=Sum('cost_number'))['sum']
    if request.method == 'POST':
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        saleman = request.POST.get('saleman')
        customer = request.POST.get('customer')
        cost_type = request.POST.get('type')
        area = request.POST.get('area')
        sql = f"select * from app01_costtable where date (date) between if (length('{start_time}')=0 ,'2018-01-01','{start_time}' ) and if(length('{end_time}') =0,now(),'{end_time}') and if(length('{customer}')=0,ISNULL(customer),customer='{customer}' ) and saleman like '%%{saleman}%%' and area like '%%{area}%%'and cost_type like '%%{cost_type}%%'"
        money_sql = f"select id, sum(cost_number) cost_sum from app01_costtable where date (date) between if (length('{start_time}')=0 ,'2018-01-01','{start_time}' ) and if(length('{end_time}') =0,now(),'{end_time}') and if(length('{customer}')=0,ISNULL(customer),customer='{customer}' ) and saleman like '%%{saleman}%%' and area like '%%{area}%%'and cost_type like '%%{cost_type}%%'"

        all_cost_info = md.CostTable.objects.raw(sql)
        cost_sum = md.CostTable.objects.raw(money_sql)[0].cost_sum
        print(money_sql)
    return render(request, 'customer/customer_cost.html',
                  {'all_type': all_type, 'all_area': all_area, 'all_saleman_name': all_saleman_name,
                   'all_customer_name': all_customer_name, 'all_cost_info': all_cost_info,
                   'cost_sum': cost_sum})
