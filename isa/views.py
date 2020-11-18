import tempfile
import logging
import hashlib
import os
import base64
import paho.mqtt.client as mqtt
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import auth
from rest_framework.views import APIView

from .models import *
from django.contrib.auth.models import User
from django.db.models import Avg, Count, Min, Sum, Max, IntegerField, Window, Func, Subquery, Case, When, F, Func, Q
from django.db.models.expressions import RawSQL, Window
from django.db.models.functions import Cast, Right, Lag, Left, Substr, Coalesce
from django.template.loader import render_to_string
from weasyprint import HTML
from django.utils import timezone
from django.contrib import messages
from django.db import connections, IntegrityError
from datetime import datetime
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

# from .forms import UserCreationForm, UsersForm
month = {'1': 'Janauary',
         '2': 'February',
         '3': 'March',
         '4': 'April',
         '5': 'May',
         '6': 'June',
         '7': 'July',
         '8': 'August',
         '9': 'September',
         '10': 'October',
         '11': 'November',
         '12': 'December'}

LOG_FORMAT = "%(Levelname)s:%(asctime)s:%(message)s"
logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s:%(name)s:%(message)s')
logger = logging.getLogger(__name__)


@login_required(login_url="/accounts/login")
def index(request):
    user = request.user
    logger.info('accessing homepage')
    return render(request, 'isa/index.html', {'user': user})


@login_required(login_url="/accounts/login")
def income(request):
    # operators = Transaction.objects.values('pos_name').distinct()
    operators = Transaction.objects.values('pos_name').distinct()
    logger.info('accessing bir report')
    return render(request, 'isa/income.html', {'operators': operators})


@login_required(login_url="/accounts/login")
def bir(request):
    if request.method == 'POST':
        if request.POST['start'] and request.POST['end'] and request.POST['pos']:
            start_date = request.POST['start']
            end_date = request.POST['end']
            pos = request.POST['pos']
            user = request.user
            incomer = Transaction.objects.raw(
                'SELECT t.business_date as business_date, t.pos_name, min(or_number) as beginning_or, min(or_number) as id, max(or_number) as ending_or, (SELECT SUM(x.gross_amount) FROM transaction x WHERE x.id <= MAX(t.id) AND t.pos_name = x.pos_name) - SUM(t.gross_amount) AS accum_sales_beginning, (SELECT SUM(x.gross_amount) FROM transaction x WHERE x.id <= MAX(t.id) AND t.pos_name = x.pos_name) AS accum_sales_ending, 0.00 as manual_or, sum(gross_amount) as gross_sales, sum(gross_amount) as gross_sales_day, SUM(vat_sales) as vatable_sales, SUM(vat) as vat_amount,  sum(vat_exempt_sales) as vat_exempt_sales, sum(vat_zero_rated_sales) as zero_rated_sales, sum(discount_regular) as regular_discount, sum(discount_special) as special_discount, 0.00 as returns, 0.00 as void, sum(discount_regular) + sum(discount_special) as total_deductions, sum(vat_spcl_disc) as vat_special_discount, 0.00 as vat_on_returns, 0.00 as other, sum(vat_spcl_disc) as total_vat_spcl_disc, sum(vat_payable) as vat_payable, sum(gross_amount) - sum(discount_regular) - sum(discount_special) - sum(vat)  as net_sales, 0.00 as other_income, 0.00 as sales_overrun_overflow, sum(gross_amount) - sum(discount_regular) - sum(discount_special) - sum(vat) as total_net_sales, 0 as reset_counter FROM transaction t WHERE t.business_date between %s and %s and t.pos_name = %s GROUP BY t.business_date, t.pos_name order by t.business_date;',
                [start_date, end_date, pos])
            incomerg = Transaction.objects.raw(
                'SELECT min(or_number) as id, 0.00 as manual_or, sum(gross_amount) as gross_sales, max(business_date) as max_date, min(business_date) as min_date, sum(gross_amount) as gross_sales_day, SUM(vat_sales) as vatable_sales, SUM(vat) as vat_amount,  sum(vat_exempt_sales) as vat_exempt_sales, sum(vat_zero_rated_sales) as zero_rated_sales, sum(discount_regular) as regular_discount, sum(discount_special) as special_discount, 0.00 as returns, 0.00 as void, sum(discount_regular) + sum(discount_special) as total_deductions, sum(vat_spcl_disc) as vat_special_discount, 0.00 as vat_on_returns, 0.00 as other, sum(vat_spcl_disc) as total_vat_spcl_disc, sum(vat_payable) as vat_payable, sum(gross_amount) - sum(discount_regular) - sum(discount_special) - sum(vat)  as net_sales, 0.00 as other_income, 0.00 as sales_overrun_overflow, sum(gross_amount) - sum(discount_regular) - sum(discount_special) - sum(vat) as total_net_sales, 0 as reset_counter FROM transaction t WHERE t.business_date between %s and %s and t.pos_name = %s GROUP BY t.pos_name;',
                [start_date, end_date, pos])

            com = Companydb.objects.all()
            context = {
                'incomer': incomer,
                'incomerg': incomerg,
                'start_date': start_date,
                'end_date': end_date,
                'pos': pos,
                'com': com,
                'user': user,
            }

            if not com:
                return render(request, 'isa/income.html', {'error': 'No Company Details'})
            if not incomer:
                return render(request, 'isa/income.html', {'error': 'No Data on Selected Date'})
        else:
            logger.info('Missing field')
            return render(request, 'isa/income.html', {'error': 'All fields required'})

    # Rendered

    html_string = render_to_string('isa/bir.html', context)
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=income_report.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())
    logger.info('bir pdfreport generated successfully')
    return response


@login_required(login_url="/accounts/login")
def birmonthly(request):
    if request.method == 'POST':
        if request.POST['start']:
            start_date = request.POST['start']

            new_start = list(start_date)
            start_month = new_start[0]
            year_join = new_start[2:]
            year_join = ''.join(year_join)
            start_year = year_join
            user = request.user
            com = Companydb.objects.all()
            incomer = Transaction.objects.raw(
                'SELECT t.business_date as business_date, t.pos_name, min(or_number) as beginning_or, min(or_number) as id, max(or_number) as ending_or, (SELECT SUM(x.gross_amount) FROM transaction x WHERE x.id <= MAX(t.id) AND t.pos_name = x.pos_name) - SUM(t.gross_amount) AS accum_sales_beginning, (SELECT SUM(x.gross_amount) FROM transaction x WHERE x.id <= MAX(t.id) AND t.pos_name = x.pos_name) AS accum_sales_ending, 0.00 as manual_or, sum(gross_amount) as gross_sales, sum(gross_amount) as gross_sales_day, SUM(vat_sales) as vatable_sales, SUM(vat) as vat_amount,  sum(vat_exempt_sales) as vat_exempt_sales, sum(vat_zero_rated_sales) as zero_rated_sales, sum(discount_regular) as regular_discount, sum(discount_special) as special_discount, 0.00 as returns, 0.00 as void, sum(discount_regular) + sum(discount_special) as total_deductions, sum(vat_spcl_disc) as vat_special_discount, 0.00 as vat_on_returns, 0.00 as other, sum(vat_spcl_disc) as total_vat_adjustment, sum(vat_payable) as vat_payable, sum(gross_amount) - sum(discount_regular) - sum(discount_special) - sum(vat)  as net_sales, 0.00 as other_income, 0.00 as sales_overrun_overflow, sum(gross_amount) - sum(discount_regular) - sum(discount_special) - sum(vat) as total_net_sales, 0 as reset_counter FROM transaction t WHERE year(t.business_date) = %s and month(t.business_date) = %s and t.pos_name = "pos-1" GROUP BY t.business_date, t.pos_name order by t.business_date;',
                [start_year, start_month])
            incomerg = Transaction.objects.raw(
                'SELECT min(or_number) as id, 0.00 as manual_or, sum(gross_amount) as gross_sales, sum(gross_amount) as gross_sales_day, SUM(vat_sales) as vatable_sales, SUM(vat) as vat_amount,  sum(vat_exempt_sales) as vat_exempt_sales, sum(vat_zero_rated_sales) as zero_rated_sales, sum(discount_regular) as regular_discount, sum(discount_special) as special_discount, 0.00 as returns, 0.00 as void, sum(discount_regular) + sum(discount_special) as total_deductions, sum(vat_spcl_disc) as vat_special_discount, 0.00 as vat_on_returns, 0.00 as other, sum(vat_spcl_disc) as total_vat_adjustment, sum(vat_payable) as vat_payable, sum(gross_amount) - sum(discount_regular) - sum(discount_special) - sum(vat)  as net_sales, 0.00 as other_income, 0.00 as sales_overrun_overflow, sum(gross_amount) - sum(discount_regular) - sum(discount_special) - sum(vat) as total_net_sales, 0 as reset_counter FROM transaction t WHERE year(t.business_date) = %s and month(t.business_date) = %s and t.pos_name = "pos-1" order by t.business_date',
                [start_year, start_month])
            incomer2 = Transaction.objects.raw(
                'SELECT t.business_date as business_date, t.pos_name, min(or_number) as beginning_or, min(or_number) as id, max(or_number) as ending_or, (SELECT SUM(x.gross_amount) FROM transaction x WHERE x.id <= MAX(t.id) AND t.pos_name = x.pos_name) - SUM(t.gross_amount) AS accum_sales_beginning, (SELECT SUM(x.gross_amount) FROM transaction x WHERE x.id <= MAX(t.id) AND t.pos_name = x.pos_name) AS accum_sales_ending, 0.00 as manual_or, sum(gross_amount) as gross_sales, sum(gross_amount) as gross_sales_day, SUM(vat_sales) as vatable_sales, SUM(vat) as vat_amount,  sum(vat_exempt_sales) as vat_exempt_sales, sum(vat_zero_rated_sales) as zero_rated_sales, sum(discount_regular) as regular_discount, sum(discount_special) as special_discount, 0.00 as returns, 0.00 as void, sum(discount_regular) + sum(discount_special) as total_deductions, sum(vat_spcl_disc) as vat_special_discount, 0.00 as vat_on_returns, 0.00 as other, sum(vat_spcl_disc) as total_vat_adjustment, sum(vat_payable) as vat_payable, sum(gross_amount) - sum(discount_regular) - sum(discount_special) - sum(vat)  as net_sales, 0.00 as other_income, 0.00 as sales_overrun_overflow, sum(gross_amount) - sum(discount_regular) - sum(discount_special) - sum(vat) as total_net_sales, 0 as reset_counter FROM transaction t WHERE year(t.business_date) = %s and month(t.business_date) = %s and t.pos_name = "pos-2" GROUP BY t.business_date, t.pos_name order by t.business_date;',
                [start_year, start_month])

            incomer2g = Transaction.objects.raw(
                'SELECT min(or_number) as id, 0.00 as manual_or, sum(gross_amount) as gross_sales, sum(gross_amount) as gross_sales_day, SUM(vat_sales) as vatable_sales, SUM(vat) as vat_amount,  sum(vat_exempt_sales) as vat_exempt_sales, sum(vat_zero_rated_sales) as zero_rated_sales, sum(discount_regular) as regular_discount, sum(discount_special) as special_discount, 0.00 as returns, 0.00 as void, sum(discount_regular) + sum(discount_special) as total_deductions, sum(vat_spcl_disc) as vat_special_discount, 0.00 as vat_on_returns, 0.00 as other, sum(vat_spcl_disc) as total_vat_adjustment, sum(vat_payable) as vat_payable, sum(gross_amount) - sum(discount_regular) - sum(discount_special) - sum(vat)  as net_sales, 0.00 as other_income, 0.00 as sales_overrun_overflow, sum(gross_amount) - sum(discount_regular) - sum(discount_special) - sum(vat) as total_net_sales, 0 as reset_counter FROM transaction t WHERE year(t.business_date) = %s and month(t.business_date) = %s order by t.business_date',
                [start_year, start_month])

            incomer3 = Transaction.objects.raw(
                'SELECT t.business_date as business_date, t.pos_name, min(or_number) as beginning_or, min(or_number) as id, max(or_number) as ending_or, (SELECT SUM(x.gross_amount) FROM transaction x WHERE x.id <= MAX(t.id) AND t.pos_name = x.pos_name) - SUM(t.gross_amount) AS accum_sales_beginning, (SELECT SUM(x.gross_amount) FROM transaction x WHERE x.id <= MAX(t.id) AND t.pos_name = x.pos_name) AS accum_sales_ending, 0.00 as manual_or, sum(gross_amount) as gross_sales, sum(gross_amount) as gross_sales_day, SUM(vat_sales) as vatable_sales, SUM(vat) as vat_amount,  sum(vat_exempt_sales) as vat_exempt_sales, sum(vat_zero_rated_sales) as zero_rated_sales, sum(discount_regular) as regular_discount, sum(discount_special) as special_discount, 0.00 as returns, 0.00 as void, sum(discount_regular) + sum(discount_special) as total_deductions, sum(vat_spcl_disc) as vat_special_discount, 0.00 as vat_on_returns, 0.00 as other, sum(vat_spcl_disc) as total_vat_adjustment, sum(vat_payable) as vat_payable, sum(gross_amount) - sum(discount_regular) - sum(discount_special) - sum(vat)  as net_sales, 0.00 as other_income, 0.00 as sales_overrun_overflow, sum(gross_amount) - sum(discount_regular) - sum(discount_special) - sum(vat) as total_net_sales, 0 as reset_counter FROM transaction t WHERE year(t.business_date) = %s and month(t.business_date) = %s and t.pos_name = "pos-3" GROUP BY t.business_date, t.pos_name order by t.business_date;',
                [start_year, start_month])

            incomer3g = Transaction.objects.raw(
                'SELECT min(or_number) as id, 0.00 as manual_or, sum(gross_amount) as gross_sales, sum(gross_amount) as gross_sales_day, SUM(vat_sales) as vatable_sales, SUM(vat) as vat_amount,  sum(vat_exempt_sales) as vat_exempt_sales, sum(vat_zero_rated_sales) as zero_rated_sales, sum(discount_regular) as regular_discount, sum(discount_special) as special_discount, 0.00 as returns, 0.00 as void, sum(discount_regular) + sum(discount_special) as total_deductions, sum(vat_spcl_disc) as vat_special_discount, 0.00 as vat_on_returns, 0.00 as other, sum(vat_spcl_disc) as total_vat_adjustment, sum(vat_payable) as vat_payable, sum(gross_amount) - sum(discount_regular) - sum(discount_special) - sum(vat)  as net_sales, 0.00 as other_income, 0.00 as sales_overrun_overflow, sum(gross_amount) - sum(discount_regular) - sum(discount_special) - sum(vat) as total_net_sales, 0 as reset_counter FROM transaction t WHERE year(t.business_date) = %s and month(t.business_date) = %s and t.pos_name = "pos-3" order by t.business_date',
                [start_year, start_month])

            incomerm = ManualTransaction.objects.raw(
                'SELECT t.business_date, t.pos_name, min(ticket_no) as id, min(ticket_no) as beginning_or, max(ticket_no) as ending_or, (SELECT SUM(x.gross_amount) FROM manual_transaction x WHERE x.id <= MAX(t.id) AND t.pos_name = x.pos_name) - SUM(t.gross_amount) AS accum_sales_beginning,(SELECT SUM(x.gross_amount) FROM manual_transaction x WHERE x.id <= MAX(t.id) AND t.pos_name = x.pos_name) AS accum_sales_ending, sum(gross_amount) as gross_sales_day, 0.00 as manual_or, sum(gross_amount) as gross_sales_pos, SUM(vatable_sale) as vatable_sales, SUM(vat) as vat_amount,  sum(vat_exempt_sale) as vat_exempt_sales, 0.00 as zero_rated_sales, sum(regular_discount) as regular_discount, sum(special_discount) as special_discount, 0.00 as returns, 0.00 as void, sum(special_discount) + sum(regular_discount) as total_deductions, sum(vat_adjustment) as vat_special_discount, 0 as vat_on_returns, 0.00 as other, sum(vat_adjustment) as total_vat_adjustment, sum(vat_payable) as vat_payable, sum(gross_amount) - sum(regular_discount) - sum(special_discount) - sum(vat)  as net_sales, 0.00 as other_income, 0 as sales_overrun_overflow, sum(gross_amount) - sum(regular_discount) - sum(special_discount) - sum(vat) as total_net_sales, 0 as reset_counter FROM manual_transaction t WHERE year(business_date) = %s and month(business_date) = %s group by t.business_date, t.pos_name;',
                [start_year, start_month])

            incomermg = ManualTransaction.objects.raw(
                'SELECT min(ticket_no) as id, 0.00 as manual_or, sum(gross_amount) as gross_sales_day, SUM(vatable_sale) as vatable_sales, SUM(vat) as vat_amount,  sum(vat_exempt_sale) as vat_exempt_sales, 0.00 as zero_rated_sales, sum(regular_discount) as regular_discount, sum(special_discount) as special_discount, 0.00 as returns, 0 as void, sum(special_discount) + sum(regular_discount) as total_deductions, sum(vat_adjustment) as vat_special_discount, 0.00 as vat_on_returns, 0.00 as other, sum(vat_adjustment) as total_vat_adjustment, sum(vat_payable) as vat_payable, sum(gross_amount) - sum(regular_discount) - sum(special_discount) - sum(vat)  as net_sales, 0.00 as other_income, 0.00 as sales_overrun_overflow, sum(gross_amount) - sum(regular_discount) - sum(special_discount) - sum(vat) as total_net_sales, 0 as reset_counter FROM manual_transaction WHERE year(business_date) = %s and month(business_date) = %s;',
                [start_year, start_month])

            incomer4 = Transaction.objects.raw(
                'select 1 as id, sum(gross_amount) as gross_sales_day, sum(vat_sales) as vatable_sales, sum(vat)as vat_amount, sum(vat_exempt_sales)as vat_exempt_sales, 0.00 as zero_rated_sales, sum(discount_regular)as regular_discount,sum(discount_special)as special_discount, 0.00 as void, 0.00 as returns, sum(discount_regular) + sum(discount_special) as total_deductions, sum(vat_spcl_disc) as vat_special_discount, 0.00 as vat_on_returns, 0.00 as other, sum(net_amount)as net_sales, 0.00 as other_income, 0.00 as sales_overrun_overflow, sum(net_amount)as total_net_sales, 0 as reset_counter from `transaction` where year(business_date) = %s and month(business_date) = %s;',
                [start_year, start_month])

            incom = Transaction.objects.raw(
                'SELECT t.business_date as business_date, t.pos_name, min(or_number) as beginning_or, min(or_number) as id, max(or_number) as ending_or, (SELECT SUM(x.gross_amount) FROM transaction x WHERE x.id <= MAX(t.id) AND t.pos_name = x.pos_name) - SUM(t.gross_amount) AS accum_sales_beginning, (SELECT SUM(x.gross_amount) FROM transaction x WHERE x.id <= MAX(t.id) AND t.pos_name = x.pos_name) AS accum_sales_ending, 0.00 as manual_or, sum(gross_amount) as gross_sales, sum(gross_amount) as gross_sales_day, SUM(vat_sales) as vatable_sales, SUM(vat) as vat_amount,  sum(vat_exempt_sales) as vat_exempt_sales, sum(vat_zero_rated_sales) as zero_rated_sales, sum(discount_regular) as regular_discount, sum(discount_special) as special_discount, 0.00 as returns, 0.00 as void, sum(discount_regular) + sum(discount_special) as total_deductions, sum(vat_spcl_disc) as vat_special_discount, 0.00 as vat_on_returns, 0.00 as other, sum(vat_spcl_disc) as total_vat_adjustment, sum(vat_payable) as vat_payable, sum(gross_amount) - sum(discount_regular) - sum(discount_special) - sum(vat)  as net_sales, 0.00 as other_income, 0.00 as sales_overrun_overflow, sum(gross_amount) - sum(discount_regular) - sum(discount_special) - sum(vat) as total_net_sales, 0 as reset_counter FROM transaction t WHERE year(t.business_date) = %s and month(t.business_date) = %s GROUP BY t.business_date, t.pos_name order by t.business_date;',[start_year, start_month])
            for p in incomer3:
                print(p)
            month = {'1': 'Janauary',
                     '2': 'February',
                     '3': 'March',
                     '4': 'April',
                     '5': 'May',
                     '6': 'June',
                     '7': 'July',
                     '8': 'August',
                     '9': 'September',
                     '10': 'October',
                     '11': 'November',
                     '12': 'December'}

            new_date = month[start_month]
            b = Transaction.objects.filter(business_date__year=start_year).filter(business_date__month=start_month).values('pos_name','business_date')
            a = list()
            for i in range(0,Tblpermit.objects.all().values('pc').count()):
                a.append(str(i))
            context = {
                'start_month': start_month,
                'start_year': start_year,

                'incomer': incomer,
                'incomerg': incomerg,
                'incomer2': incomer2,

                'incomer2g': incomer2g,

                'incomer3': incomer3,
                'incomer3g': incomer3g,
                'incomerm': incomerm,
                'incomermg': incomermg,
                'incomer4': incomer4,

                'start_date': start_date,
                'com': com,
                'user': user,
                'new_date': new_date,
                'start_year': start_year,
                'pos_name': Tblpermit.objects.all(),
                'sampsss': incom.order_by('business_date', '-pos_name'),
            }

            if not com:
                return render(request, 'isa/income.html', {'error': 'No Company Details'})
            if not incomer:
                return render(request, 'isa/income.html', {'error': 'No Data on Selected Date'})

        else:
            logger.info('Missing field')
            return render(request, 'isa/income.html', {'error': 'All fields required'})

    # Rendered

    html_string = render_to_string('isa/birmonthly.html', context)
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=income_report_monthly.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())
    logger.info('bir monthly pdfreport generated successfully')
    return response

@login_required(login_url="/accounts/login")
def discountpos(request):
    operators = Transaction.objects.values('pos_name').distinct()

    context = {
        'operators': operators,
    }
    logger.info('accessing discount bir report')
    return render(request, 'isa/discountpos.html', context)


@login_required(login_url="/accounts/login")
def seniorpospdf(request):
    if request.method == 'POST':
        if request.POST['start'] and request.POST['end']:
            start_date = request.POST['start']
            end_date = request.POST['end']
            # new_start = list(start_date)
            # new_start = month['6']
            user = request.user
            seniors = Transaction.objects.values(
                'business_date', 'vat_spcl_disc', 'vat_exempt_sales', 'discount_special', 'net_amount', 'or_number',
                'parker_name', 'parker_ref_id', 'discount_name', 'gross_amount', 'discount_special').filter(
                business_date__gte=start_date, business_date__lte=end_date).filter(
                Q(discount_name__startswith='pw') | Q(discount_name__startswith='Se'))
            gtotal = Transaction.objects.filter(
                business_date__gte=start_date, business_date__lte=end_date).filter(
                Q(discount_name__startswith='pw') | Q(discount_name__startswith='Se')).aggregate(
                min_date=Min('business_date'), max_date=Max('business_date'), vat_special=Sum('vat_spcl_disc'),
                gross=Sum('gross_amount'), discount=Sum('discount_special'), vat_exempt=Sum('vat_exempt_sales'),
                net_sales=Sum('net_amount'))

            com = Companydb.objects.all()

            context = {
                'start_date': start_date,
                'end_date': end_date,
                'seniors': seniors,
                'com': com,
                'user': user,
                'gtotal': gtotal,
            }

            if not com:
                return render(request, 'isa/discountpos.html', {'error': 'No Company Details'})
            if not seniors:
                return render(request, 'isa/discountpos.html', {'error': 'No Data on Selected Date'})

        else:
            logger.info('Missing field')
            return render(request, 'isa/discountpos.html', {'error': 'All fields required'})

    # Rendered

    html_string = render_to_string('isa/isa/seniorpospdf.html', context)
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=seniorcitizen_report.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())
    logger.info('senior discount pdfreport generated successfully')
    return response


@login_required(login_url="/accounts/login")
def cash(request):
    operators = Transaction.objects.values('username').distinct()
    # operator_id = Transaction.objects.values('users_id').distinct()
    pos = Transaction.objects.values('pos_name').distinct()

    context = {
        'operators': operators,
        'pos': pos,
    }
    logger.info('accessing cash and card report')
    return render(request, 'isa/cash.html', context)


@login_required(login_url="/accounts/login")
def cashpdf(request):
    if request.method == 'POST':
        try:
            operator = request.POST['operator']
        except Exception:
            return render(request, 'isa/cash.html', {'error': 'No Operator Selected'})

        # if not operator:
        #     return render(request, 'isa/cash.html',{'error': 'No Operator Selected'})
        if request.POST['start'] and request.POST['end'] and request.POST['operator']:

            start_date = request.POST['start']
            end_date = request.POST['end']
            operator = request.POST['operator']
            print(operator)
            user = request.user
            com = Companydb.objects.all()
            cash = Transaction.objects.values('username').filter(
                business_date__gte=start_date, business_date__lte=end_date, username=operator).aggregate(
                gross=Sum('gross_amount'), vatsales=Sum('vat_sales'), vatspecial=Sum('vat_spcl_disc'),
                voucher=Sum('voucher'), vatpayable=Sum('vat_payable'), vatamount=Sum('vat'),
                vatexemptsales=Sum('vat_exempt_sales'),
                specialdiscount=Sum('discount_special'), discount=Sum('discount_regular'), netsales=Sum('net_amount'),
                cash=Sum('cash'),
                credit=Sum('credit'), orstart=Min('or_number'), orend=Max('or_number'), txncount=Count('or_number'),
                timein=Min('time_in'), timeout=Max('time_out'), lost_card=Sum('fee_lostcard'))

            cashes = Transaction.objects.values('username', 'pos_name').filter(
                business_date__gte=start_date, business_date__lte=end_date, username=operator).annotate(
                gross=Sum('gross_amount'), vatsales=Sum('vat_sales'), vatspecial=Sum('vat_spcl_disc'),
                vatamount=Sum('vat'), vatexemptsales=Sum('vat_exempt_sales'),
                specialdiscount=Sum('discount_special'), discount=Sum('discount_regular'), voucher=Sum('voucher'),
                vatpayable=Sum('vat_payable'), netsales=Sum('net_amount'), cash=Sum('cash'),
                credit=Sum('credit'), orstart=Min('or_number'), orend=Max('or_number'), txncount=Count('or_number'),
                timein=Min('time_in'), timeout=Max('time_out'), lost_card=Sum('fee_lostcard')).order_by('pos_name')

            losts = Transaction.objects.filter(
                business_date__gte=start_date, business_date__lte=end_date, username=operator,
                fee_lostcard__gte=1).aggregate(clost=Count('fee_lostcard'),
                                               lost_sum=Sum('fee_lostcard'))

            trans = Transaction.objects.values('vehicle_type').annotate(txncount=Count('or_number'),
                                                                        gross=Sum('gross_amount')).filter(
                business_date__gte=start_date, business_date__lte=end_date, username=operator)

            lostd = Transaction.objects.annotate(clost=Count('fee_lostcard')).filter(
                business_date__gte=start_date, business_date__lte=end_date, username=operator, fee_lostcard__gte=1)

            grace = TransactionZeroAmount.objects.values('vehicle_type').annotate(
                cgrace=Count('transaction_datetime')).filter(
                business_date__gte=start_date, business_date__lte=end_date, username=operator)

            graces = TransactionZeroAmount.objects.filter(
                business_date__gte=start_date, business_date__lte=end_date, username=operator).aggregate(
                cgrace=Count('transaction_datetime'),
            )

            context = {
                'start_date': start_date,
                'end_date': end_date,
                'operator': operator,
                'cashes': cashes,
                'cash': cash,
                'com': com,
                'trans': trans,
                'losts': losts,
                'user': user,
                'lostd': lostd,
                'grace': grace,
                'graces': graces,
            }

            if not com:
                return render(request, 'isa/cash.html', {'error': 'No Company Details'})
            if not cash:
                return render(request, 'isa/cash.html', {'error': 'No Data on Selected Date'})
        else:
            logger.info('Missing field')
            return render(request, 'isa/cash.html', {'error': 'All fields required'})

    # Rendered

    html_string = render_to_string('isa/pdf/cashpdf.html', context)
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=cash_report.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())
    logger.info('cash accountability pdfreport generated successfully')
    return response


@login_required(login_url="/accounts/login")
def cashpospdf(request):
    if request.method == 'POST':
        try:
            # pos = request.POST['pos']
            pass
        except Exception:
            return render(request, 'isa/cash.html', {'error': 'No POS Selected'})
        if request.POST['start'] and request.POST['end'] and request.POST['pos']:
            start_date = request.POST['start']
            end_date = request.POST['end']
            pos = request.POST['pos']
            com = Companydb.objects.all()
            user = request.user

            cash = Transaction.objects.values('pos_name', 'username').annotate(
                gross=Sum('gross_amount'), vatsales=Sum('vat_sales'), vatamount=Sum('vat'),
                vatexemptsales=Sum('vat_exempt_sales'),
                specialdiscount=Sum('discount_special'), vatspecial=Sum('vat_spcl_disc'),
                discount=Sum('discount_regular'), voucher=Sum('voucher'), vatpayable=Sum('vat_payable'),
                netsales=Sum('net_amount'), cash=Sum('cash'),
                credit=Sum('credit'), orstart=Min('or_number'), orend=Max('or_number'), txncount=Count('or_number'),
                timein=Min('time_in'), timeout=Max('time_out'), lost_card=Sum('fee_lostcard')).filter(
                business_date__gte=start_date, business_date__lte=end_date, pos_name=pos)

            tocash = Transaction.objects.values('pos_name').filter(
                business_date__gte=start_date, business_date__lte=end_date, pos_name=pos).aggregate(
                gross=Sum('gross_amount'), vatsales=Sum('vat_sales'), vatamount=Sum('vat'),
                vatexemptsales=Sum('vat_exempt_sales'),
                specialdiscount=Sum('discount_special'), vatspecial=Sum('vat_spcl_disc'),
                discount=Sum('discount_regular'), vatpayable=Sum('vat_payable'), netsales=Sum('net_amount'),
                cash=Sum('cash'),
                credit=Sum('credit'), voucher=Sum('voucher'), orstart=Min('or_number'), orend=Max('or_number'),
                txncount=Count('or_number'),
                timein=Min('time_in'), timeout=Max('time_out'), lost_card=Sum('fee_lostcard'))

            trans = Transaction.objects.values('vehicle_type').annotate(txncount=Count('or_number'),
                                                                        gross=Sum('gross_amount')).filter(
                business_date__gte=start_date, business_date__lte=end_date, pos_name=pos)

            losts = Transaction.objects.values('vehicle_type').filter(
                business_date__gte=start_date, business_date__lte=end_date, pos_name=pos,
                fee_lostcard__gte=1).aggregate(clost=Count('fee_lostcard'),
                                               lost_sum=Sum('fee_lostcard'))

            lostd = Transaction.objects.annotate(clost=Count('fee_lostcard')).filter(
                business_date__gte=start_date, business_date__lte=end_date, pos_name=pos, fee_lostcard__gte=1)

            grace = TransactionZeroAmount.objects.values('vehicle_type').annotate(
                cgrace=Count('transaction_datetime')).filter(
                business_date__gte=start_date, business_date__lte=end_date, pos_name=pos)

            graces = TransactionZeroAmount.objects.filter(
                business_date__gte=start_date, business_date__lte=end_date, pos_name=pos).aggregate(
                cgrace=Count('transaction_datetime'),
            )

            context = {
                'start_date': start_date,
                'pos': pos,
                'user': user,
                'com': com,
                'cash': cash,
                'tocash': tocash,
                'trans': trans,
                'losts': losts,
                'lostd': lostd,
                'grace': grace,
                'graces': graces,

            }

        else:
            logger.info('Missing field')
            return render(request, 'isa/cash.html', {'error': 'All fields required'})

    # Rendered

    html_string = render_to_string('isa/pdf/cashpospdf.html', context)
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=cash_report.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())
    logger.info('cashpos accountability pdfreport generated successfully')
    return response


@login_required(login_url="/accounts/login")
def cashallpdf(request):
    if request.method == 'POST':
        if request.POST['start'] and request.POST['end']:
            start_date = request.POST['start']
            end_date = request.POST['end']
            user = request.user
            com = Companydb.objects.all()

            cash = Transaction.objects.values('username', 'pos_name').annotate(
                gross=Sum('gross_amount'), vatpayable=Sum('vat_payable'), vatsales=Sum('vat_sales'),
                vatamount=Sum('vat'), vatexemptsales=Sum('vat_exempt_sales'),
                specialdiscount=Sum('discount_special'), vatspecial=Sum('vat_spcl_disc'), voucher=Sum('voucher'),
                discount=Sum('discount_regular'), netsales=Sum('net_amount'), cash=Sum('cash'),
                credit=Sum('credit'), orstart=Min('or_number'), orend=Max('or_number'), txncount=Count('or_number'),
                timein=Min('time_in'), timeout=Max('time_out'), lost_card=Sum('fee_lostcard')).filter(
                business_date__gte=start_date, business_date__lte=end_date).order_by('pos_name')

            # cash = Transaction.objects.values('username', 'pos_name').annotate(
            #     gross=Sum('gross_amount'), vatpayable=Sum('vat_payable'), vatsales=Sum('vat_sales'), vatamount=Sum('vat'), vatexemptsales=Sum('vat_exempt_sales'),
            #     specialdiscount=Sum('discount_special'), vatspecial=Sum('vat_spcl_disc'), voucher=Sum('voucher'), discount=Sum('discount_regular'), netsales=Sum('net_amount'), cash=Sum('cash'),
            #     credit=Sum('credit'), orstart=Min('or_number'), orend=Max('or_number'), txncount=Count('or_number'),
            #     timein=Min('time_in'), timeout=Max('time_out'), lost_card=Sum('fee_lostcard')).filter(
            #   business_date__gte=start_date, business_date__lte=end_date).order_by('pos_name')

            tocash = Transaction.objects.values('pos_name').filter(
                business_date__gte=start_date, business_date__lte=end_date).aggregate(
                gross=Sum('gross_amount'), vatpayable=Sum('vat_payable'), vatsales=Sum('vat_sales'),
                vatamount=Sum('vat'), vatexemptsales=Sum('vat_exempt_sales'),
                specialdiscount=Sum('discount_special'), vatspecial=Sum('vat_spcl_disc'), voucher=Sum('voucher'),
                discount=Sum('discount_regular'), netsales=Sum('net_amount'), cash=Sum('cash'),
                credit=Sum('credit'), orstart=Min('or_number'), orend=Max('or_number'), txncount=Count('or_number'),
                timein=Min('time_in'), timeout=Max('time_out'), lost_card=Sum('fee_lostcard'))

            trans = Transaction.objects.values('vehicle_type').annotate(txncount=Count('or_number'),
                                                                        gross=Sum('gross_amount')).filter(
                business_date__gte=start_date, business_date__lte=end_date)

            losts = Transaction.objects.filter(
                business_date__gte=start_date, business_date__lte=end_date, fee_lostcard__gte=1).aggregate(
                clost=Count('fee_lostcard'),
                lost_sum=Sum('fee_lostcard'))

            lostd = Transaction.objects.annotate(clost=Count('fee_lostcard')).filter(
                business_date__gte=start_date, business_date__lte=end_date, fee_lostcard__gte=1)

            grace = TransactionZeroAmount.objects.values('vehicle_type').annotate(
                cgrace=Count('transaction_datetime')).filter(
                business_date__gte=start_date, business_date__lte=end_date)

            graces = TransactionZeroAmount.objects.filter(
                business_date__gte=start_date, business_date__lte=end_date).aggregate(
                cgrace=Count('transaction_datetime'),
            )

            context = {
                'start_date': start_date,
                'end_date': end_date,
                'com': com,
                'user': user,
                'cash': cash,
                'tocash': tocash,
                'trans': trans,
                'losts': losts,
                'lostd': lostd,
                'grace': grace,
                'graces': graces,

            }

            if not com:
                return render(request, 'isa/cash.html', {'error': 'No Company Details'})
            if not cash:
                return render(request, 'isa/cash.html', {'error': 'No Data on Selected Date'})

        else:
            logger.info('Missing field')
            return render(request, 'isa/cash.html', {'error': 'All fields required'})

    # Rendered

    html_string = render_to_string('isa/pdf/cashallpdf.html', context)
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=cash_report.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())
    logger.info('cash all accountability pdfreport generated successfully')
    return response


@login_required(login_url="/accounts/login")
def transaction(request):
    pos = Transaction.objects.values('pos_name').distinct()

    context = {
        'pos': pos,
    }
    logger.info('accessing transaction flow report')
    return render(request, 'isa/transaction.html', context)


@login_required(login_url="/accounts/login")
def transactionpdf(request):
    if request.method == 'POST':
        if request.POST['start'] and request.POST['end'] and request.POST['pos']:
            start_date = request.POST['start']
            end_date = request.POST['end']
            pos = request.POST['pos']
            user = request.user
            com = Companydb.objects.all()

            tocash = Transaction.objects.values('business_date').annotate(
                gross=Sum('gross_amount'), vatsales=Sum('vat_sales'), vatamount=Sum('vat'),
                vatexemptsales=Sum('vat_exempt_sales'),
                specialdiscount=Sum('discount_special'), discount=Sum('discount_regular'), netsales=Sum('net_amount'),
                cash=Sum('cash'),
                credit=Sum('credit'), orstart=Min('or_number'), orend=Max('or_number'),
                txncount=Count('or_number')).filter(
                business_date__gte=start_date, business_date__lte=end_date, pos_name=pos)

            trans = Transaction.objects.values('pos_name').filter(
                business_date__gte=start_date, business_date__lte=end_date, pos_name=pos).aggregate(
                gross=Sum('gross_amount'), vatsales=Sum('vat_sales'), vatamount=Sum('vat'),
                vatexemptsales=Sum('vat_exempt_sales'),
                specialdiscount=Sum('discount_special'), discount=Sum('discount_regular'), netsales=Sum('net_amount'),
                cash=Sum('cash'),
                credit=Sum('credit'), orstart=Min('or_number'), orend=Max('or_number'), txncount=Count('or_number'),
                timein=Min('time_in'), timeout=Max('time_out'))

            context = {
                'start_date': start_date,
                'com': com,
                'pos': pos,
                'trans': trans,
                'user': user,
                'tocash': tocash,

            }

        else:
            logger.info('Missing field')
            return render(request, 'isa/transaction.html', {'error': 'All fields required'})

    # Rendered

    html_string = render_to_string('isa/pdf/transactionpdf.html', context)
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=transaction_flow.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())
    logger.info('transaction flow pdfreport generated successfully')
    return response


@login_required(login_url="/accounts/login")
def transactionxl(request):
    pos = Transaction.objects.values('pos_name').distinct()

    context = {
        'pos': pos,
    }

    logger.info('accessing transactionxl report')
    return render(request, 'isa/excel/transactionxl.html', context)


@login_required(login_url="/accounts/login")
def transactionexcel(request):
    if request.method == 'POST':
        if request.POST['start'] and request.POST['end'] and request.POST['pos']:
            start_date = request.POST['start']
            end_date = request.POST['end']
            pos = request.POST['pos']
            user = request.user
            com = Companydb.objects.all()

            tocash = Transaction.objects.values('business_date').annotate(
                gross=Sum('gross_amount'), vatsales=Sum('vat_sales'), vatamount=Sum('vat'),
                vatexemptsales=Sum('vat_exempt_sales'),
                specialdiscount=Sum('discount_special'), discount=Sum('discount_regular'), netsales=Sum('net_amount'),
                cash=Sum('cash'),
                credit=Sum('credit'), orstart=Min('or_number'), orend=Max('or_number'),
                txncount=Count('or_number')).filter(
                business_date__gte=start_date, business_date__lte=end_date, pos_name=pos)

            trans = Transaction.objects.values('pos_name').filter(
                business_date__gte=start_date, business_date__lte=end_date, pos_name=pos).aggregate(
                gross=Sum('gross_amount'), vatsales=Sum('vat_sales'), vatamount=Sum('vat'),
                vatexemptsales=Sum('vat_exempt_sales'),
                specialdiscount=Sum('discount_special'), discount=Sum('discount_regular'), netsales=Sum('net_amount'),
                cash=Sum('cash'),
                credit=Sum('credit'), orstart=Min('or_number'), orend=Max('or_number'), txncount=Count('or_number'),
                timein=Min('time_in'), timeout=Max('time_out'))

            context = {
                'start_date': start_date,
                'com': com,
                'tocash': tocash,
                'pos': pos,
                'transaction': transaction,
                'user': user,
                'trans': trans,
            }

        else:
            logger.info('Missing field')
            return render(request, 'isa/excel/transactionxl.html', {'error': 'All fields required'})

    return render(request, 'isa/excel/transactionexcel.html', context)


class Vehicle(APIView):
    def get(self, request):
        logger.info('accessing vehicle in/out report')
        return render(request, 'isa/vehicle.html')

    def post(self, request):
        # vehicle pdf
        if request.POST['start'] and request.POST['end']:
            start_date = request.POST['start']
            end_date = request.POST['end']
            com = Companydb.objects.all()
            user = request.user

            cash = Transaction.objects.values('pos_name', 'or_number', 'cardcode', 'plate_num', 'vehicle_type',
                                              'time_in', 'time_out', 'duration', 'gross_amount').filter(
                time_out__gte=start_date, time_out__lte=end_date).order_by('pos_name', 'time_in').order_by('or_number')

            trans = Transaction.objects.filter(
                time_out__gte=start_date, time_out__lte=end_date).aggregate(
                gross=Sum('gross_amount'), timein=Min('time_in'), timeout=Max('time_out'), txncount=Count('or_number'))

            context = {
                'user': user,
                'com': com,
                'cash': cash,
                'trans': trans,

            }
        else:
            logger.info('Missing field')
            return render(request, 'isa/vehicle.html', {'error': 'All fields required'})

        # Rendered

        html_string = render_to_string('isa/pdf/vehiclepdf.html', context)
        html = HTML(string=html_string)
        result = html.write_pdf()

        # Creating http response
        response = HttpResponse(content_type='application/pdf;')
        response['Content-Disposition'] = 'inline; filename=exited_vehicles.pdf'
        response['Content-Transfer-Encoding'] = 'binary'
        with tempfile.NamedTemporaryFile(delete=True) as output:
            output.write(result)
            output.flush()
            output = open(output.name, 'rb')
            response.write(output.read())
        print('vehicle in/out pdfreport generated successfully')
        return response


@login_required(login_url="/accounts/login")
def vehiclepdf(request):
    if request.method == 'POST':
        if request.POST['start'] and request.POST['end']:
            start_date = request.POST['start']
            end_date = request.POST['end']
            com = Companydb.objects.all()
            user = request.user

            cash = Transaction.objects.values('pos_name', 'or_number', 'cardcode', 'plate_num', 'vehicle_type',
                                              'time_in', 'time_out', 'duration', 'gross_amount').filter(
                time_out__gte=start_date, time_out__lte=end_date).order_by('pos_name', 'time_in').order_by('or_number')

            trans = Transaction.objects.filter(
                time_out__gte=start_date, time_out__lte=end_date).aggregate(
                gross=Sum('gross_amount'), timein=Min('time_in'), timeout=Max('time_out'), txncount=Count('or_number'))

            context = {
                'user': user,
                'com': com,
                'cash': cash,
                'trans': trans,

            }
            html_string = render_to_string('isa/pdf/vehiclepdf.html', context)
            html = HTML(string=html_string)
            result = html.write_pdf()
            response = HttpResponse(content_type='application/pdf;')
            response['Content-Disposition'] = 'inline; filename=exited_vehicles.pdf'
            response['Content-Transfer-Encoding'] = 'binary'
            with tempfile.NamedTemporaryFile(delete=True) as output:
                output.write(result)
                output.flush()
                output = open(output.name, 'rb')
                response.write(output.read())
            print('vehicle in/out pdfreport generated successfully')
            return response
        else:
            logger.info('Missing field')
            return render(request, 'isa/vehicle.html', {'error': 'All fields required'})


@login_required(login_url="/accounts/login")
def vehiclepdfbdate(request):
    if request.method == 'POST':
        if request.POST['start'] and request.POST['end']:
            start_date = request.POST['start']
            end_date = request.POST['end']
            com = Companydb.objects.all()
            user = request.user

            cash = Transaction.objects.values('pos_name', 'or_number', 'cardcode', 'plate_num', 'vehicle_type',
                                              'time_in', 'time_out', 'duration', 'gross_amount').filter(
                business_date__gte=start_date, business_date__lte=end_date).order_by('pos_name', 'time_in').order_by(
                'or_number')

            trans = Transaction.objects.filter(
                business_date__gte=start_date, business_date__lte=end_date).aggregate(
                gross=Sum('gross_amount'), timein=Min('time_in'), timeout=Max('time_out'), txncount=Count('or_number'))

            context = {
                'user': user,
                'com': com,
                'cash': cash,
                'trans': trans,

            }
            # Rendered

            html_string = render_to_string('isa/pdf/vehiclepdfbdate.html', context)
            html = HTML(string=html_string)
            result = html.write_pdf()

            # Creating http response
            response = HttpResponse(content_type='application/pdf;')
            response['Content-Disposition'] = 'inline; filename=exited_vehicles.pdf'
            response['Content-Transfer-Encoding'] = 'binary'
            with tempfile.NamedTemporaryFile(delete=True) as output:
                output.write(result)
                output.flush()
                output = open(output.name, 'rb')
                response.write(output.read())
            logger.info('vehicle in/out pdfreport generated successfully')
            return response
        else:
            logger.info('Missing field')
            return render(request, 'isa/vehicle.html', {'error': 'All fields required'})


@login_required(login_url="/accounts/login")
def stay_in(request):
    logger.info('accessing stay-in vehicles report')
    return render(request, 'isa/stay_in.html')


@login_required(login_url="/accounts/login")
def stay_inpdf(request):
    # start_date = request.POST['start']
    # end_date = request.POST['end']
    # time = Transaction.objects.values('cardcode', 'time_in', 'duration', 'plate_num', 'parker_address').filter(time_in__gte=start_date, time_in__lte=end_date)
    # totime = Transaction.objects.filter(time_in__gte=start_date, time_in__lte=end_date).aggregate(txncount=Count('cardcode'))
    com = Companydb.objects.all()
    user = request.user

    context = {

        'com': com,
        'user': user,

    }

    # Rendered

    html_string = render_to_string('isa/pdf/stay_inpdf.html', context)
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=stay_in_report.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())
    logger.info('vehicle in/out pdfreport generated successfully')
    return response


class Cashier(APIView):
    def get(self, request):
        operators = Transaction.objects.values('username').distinct()
        pos = Transaction.objects.values('pos_name').distinct()

        context = {
            'operators': operators,
            'pos': pos,
        }
        logger.info('accessing cashier detailed report')
        return render(request, 'isa/cashier.html', context)

    def post(self, request):
        user = request.user
        operator = request.POST.get('pos', '')
        pos = request.POST.get('pos', '')
        start_date = request.POST['start']
        end_date = request.POST['end']
        com = Companydb.objects.all()
        rep = request.POST.get("rep", None)
        if rep == "operators":
            cash = Transaction.objects.values(
                'or_number', 'pos_name', 'business_date', 'cardcode', 'plate_num', 'voucher', 'vehicle_type', 'time_in',
                'time_out', 'duration', 'gross_amount', 'discount_special', 'discount_regular', 'vat_exempt_sales',
                'net_amount', 'vat_sales', 'vat', 'cash', 'credit', 'vat_payable', 'vat_spcl_disc').filter(
                business_date__gte=start_date, business_date__lte=end_date, username=operator).order_by('or_number')

            trans = Transaction.objects.filter(
                business_date__gte=start_date, business_date__lte=end_date, username=operator).aggregate(
                gross=Sum('gross_amount'), vatsales=Sum('vat_sales'), vatamount=Sum('vat'),
                vatexemptsales=Sum('vat_exempt_sales'),
                specialdiscount=Sum('discount_special'), discount=Sum('discount_regular'), netsales=Sum('net_amount'),
                cash=Sum('cash'),
                credit=Sum('credit'), orstart=Min('or_number'), orend=Max('or_number'), txncount=Count('or_number'),
                voucher=Sum('voucher'),
                timein=Min('time_in'), timeout=Max('time_out'), vat_payable=Sum('vat_payable'),
                vat_special=Sum('vat_spcl_disc'))

            context = {
                'start_date': start_date,
                'operator': operator,
                'cash': cash,
                'com': com,
                'trans': trans,
                'user': user,
            }
            html_string = render_to_string('isa/pdf/cashierpdf.html', context)
            html = HTML(string=html_string)
            result = html.write_pdf()

            # Creating http response
            response = HttpResponse(content_type='application/pdf;')
            response['Content-Disposition'] = 'inline; filename=cashier_detailed_report.pdf'
            response['Content-Transfer-Encoding'] = 'binary'
            with tempfile.NamedTemporaryFile(delete=True) as output:
                output.write(result)
                output.flush()
                output = open(output.name, 'rb')
                response.write(output.read())
            logger.info('cash operator pdfreport generated successfully')
            return response
        elif rep == "terminal":
            cash = Transaction.objects.values(
                'or_number', 'pos_name', 'business_date', 'cardcode', 'voucher', 'plate_num', 'vehicle_type', 'time_in',
                'time_out', 'duration', 'gross_amount', 'discount_special', 'discount_regular', 'vat_exempt_sales',
                'net_amount', 'vat_sales', 'vat', 'cash', 'credit', 'vat_payable', 'vat_spcl_disc').filter(
                business_date__gte=start_date, business_date__lte=end_date, pos_name=pos).order_by('or_number')

            trans = Transaction.objects.filter(
                business_date__gte=start_date, business_date__lte=end_date, pos_name=pos).aggregate(
                gross=Sum('gross_amount'), voucher=Sum('voucher'), vatsales=Sum('vat_sales'), vatamount=Sum('vat'),
                vatexemptsales=Sum('vat_exempt_sales'),
                specialdiscount=Sum('discount_special'), discount=Sum('discount_regular'), netsales=Sum('net_amount'),
                cash=Sum('cash'),
                credit=Sum('credit'), orstart=Min('or_number'), orend=Max('or_number'), txncount=Count('or_number'),
                timein=Min('time_in'), timeout=Max('time_out'), vat_payable=Sum('vat_payable'),
                vat_special=Sum('vat_spcl_disc'))

            context = {
                'cash': cash,
                'com': com,
                'trans': trans,
                'pos': pos,
                'user': user
            }
            html_string = render_to_string('isa/pdf/cashierpospdf.html', context)
            html = HTML(string=html_string)
            result = html.write_pdf()

            # Creating http response
            response = HttpResponse(content_type='application/pdf;')
            response['Content-Disposition'] = 'inline; filename=cashier_detailed_report.pdf'
            response['Content-Transfer-Encoding'] = 'binary'
            with tempfile.NamedTemporaryFile(delete=True) as output:
                output.write(result)
                output.flush()
                output = open(output.name, 'rb')
                response.write(output.read())
            logger.info('cashier pos detailed pdfreport successfully')
            return response
        else:
            start_date = request.POST['start']
            end_date = request.POST['end']
            com = Companydb.objects.all()
            user = request.user
            cash = Transaction.objects.values(
                'or_number', 'username', 'pos_name', 'business_date', 'voucher', 'cardcode', 'plate_num',
                'vehicle_type', 'time_in', 'time_out', 'duration', 'gross_amount', 'discount_special',
                'discount_regular', 'vat_exempt_sales', 'net_amount', 'vat_sales', 'vat', 'cash', 'credit',
                'vat_payable', 'vat_spcl_disc').filter(
                business_date__gte=start_date, business_date__lte=end_date).order_by('or_number')

            trans = Transaction.objects.filter(
                business_date__gte=start_date, business_date__lte=end_date).aggregate(
                gross=Sum('gross_amount'), vatsales=Sum('vat_sales'), vatamount=Sum('vat'),
                vatexemptsales=Sum('vat_exempt_sales'),
                specialdiscount=Sum('discount_special'), discount=Sum('discount_regular'), netsales=Sum('net_amount'),
                cash=Sum('cash'),
                credit=Sum('credit'), orstart=Min('or_number'), orend=Max('or_number'), txncount=Count('or_number'),
                timein=Min('time_in'), voucher=Sum('voucher'), timeout=Max('time_out'), vat_payable=Sum('vat_payable'),
                vat_special=Sum('vat_spcl_disc'))

            context = {
                'start_date': start_date,
                'cash': cash,
                'com': com,
                'trans': trans,
                'user': user,
            }
            html_string = render_to_string('isa/pdf/cashierallpdf.html', context)
            html = HTML(string=html_string)
            result = html.write_pdf()

            # Creating http response
            response = HttpResponse(content_type='application/pdf;')
            response['Content-Disposition'] = 'inline; filename=cashier_detailed_report.pdf'
            response['Content-Transfer-Encoding'] = 'binary'
            with tempfile.NamedTemporaryFile(delete=True) as output:
                output.write(result)
                output.flush()
                output = open(output.name, 'rb')
                response.write(output.read())
            logger.info('cash all detailed pdfreport successfully')
            return response
        logger.info('Missing field')
        return render(request, 'isa/cashier.html', {'error': 'All fields required'})

        # Rendered


@login_required(login_url="/accounts/login")
def cashier(request):
    operators = Transaction.objects.values('username').distinct()
    pos = Transaction.objects.values('pos_name').distinct()

    context = {
        'operators': operators,
        'pos': pos,
    }
    logger.info('accessing cashier detailed report')
    return render(request, 'isa/cashier.html', context)


@login_required(login_url="/accounts/login")
def cashierpdf(request):
    if request.method == 'POST':
        if request.POST['start'] and request.POST['pos'] and request.POST['end']:
            start_date = request.POST['start']
            end_date = request.POST['end']
            operator = request.POST['pos']
            user = request.user
            print(user)
            print(operator)
            com = Companydb.objects.all()

            cash = Transaction.objects.values(
                'or_number', 'pos_name', 'business_date', 'cardcode', 'plate_num', 'voucher', 'vehicle_type', 'time_in',
                'time_out', 'duration', 'gross_amount', 'discount_special', 'discount_regular', 'vat_exempt_sales',
                'net_amount', 'vat_sales', 'vat', 'cash', 'credit', 'vat_payable', 'vat_spcl_disc').filter(
                business_date__gte=start_date, business_date__lte=end_date, username=operator).order_by('or_number')

            trans = Transaction.objects.filter(
                business_date__gte=start_date, business_date__lte=end_date, username=operator).aggregate(
                gross=Sum('gross_amount'), vatsales=Sum('vat_sales'), vatamount=Sum('vat'),
                vatexemptsales=Sum('vat_exempt_sales'),
                specialdiscount=Sum('discount_special'), discount=Sum('discount_regular'), netsales=Sum('net_amount'),
                cash=Sum('cash'),
                credit=Sum('credit'), orstart=Min('or_number'), orend=Max('or_number'), txncount=Count('or_number'),
                voucher=Sum('voucher'),
                timein=Min('time_in'), timeout=Max('time_out'), vat_payable=Sum('vat_payable'),
                vat_special=Sum('vat_spcl_disc'))

            context = {
                'start_date': start_date,
                'operator': operator,
                'cash': cash,
                'com': com,
                'trans': trans,
                'user': user,
            }

        else:
            logger.info('Missing field')
            return render(request, 'isa/cashier.html', {'error': 'All fields required'})

    # Rendered

    html_string = render_to_string('isa/pdf/cashierpdf.html', context)
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=cashier_detailed_report.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())
    logger.info('cash operator pdfreport generated successfully')
    return response


@login_required(login_url="/accounts/login")
def cashierallpdf(request):
    if request.method == 'POST':
        if request.POST['start'] and request.POST['end']:
            start_date = request.POST['start']
            end_date = request.POST['end']
            com = Companydb.objects.all()
            user = request.user
            print(user)

            cash = Transaction.objects.values(
                'or_number', 'username', 'pos_name', 'business_date', 'voucher', 'cardcode', 'plate_num',
                'vehicle_type', 'time_in', 'time_out', 'duration', 'gross_amount', 'discount_special',
                'discount_regular', 'vat_exempt_sales', 'net_amount', 'vat_sales', 'vat', 'cash', 'credit',
                'vat_payable', 'vat_spcl_disc').filter(
                business_date__gte=start_date, business_date__lte=end_date).order_by('or_number')

            trans = Transaction.objects.filter(
                business_date__gte=start_date, business_date__lte=end_date).aggregate(
                gross=Sum('gross_amount'), vatsales=Sum('vat_sales'), vatamount=Sum('vat'),
                vatexemptsales=Sum('vat_exempt_sales'),
                specialdiscount=Sum('discount_special'), discount=Sum('discount_regular'), netsales=Sum('net_amount'),
                cash=Sum('cash'),
                credit=Sum('credit'), orstart=Min('or_number'), orend=Max('or_number'), txncount=Count('or_number'),
                timein=Min('time_in'), voucher=Sum('voucher'), timeout=Max('time_out'), vat_payable=Sum('vat_payable'),
                vat_special=Sum('vat_spcl_disc'))

            context = {
                'start_date': start_date,
                'cash': cash,
                'com': com,
                'trans': trans,
                'user': user,
            }

        else:
            logger.info('Missing field')
            return render(request, 'isa/cashier.html', {'error': 'All fields required'})

    # Rendered

    html_string = render_to_string('isa/pdf/cashierallpdf.html', context)
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=cashier_detailed_report.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())
    logger.info('cash all detailed pdfreport successfully')
    return response


@login_required(login_url="/accounts/login")
def cashierpospdf(request):
    if request.method == 'POST':
        if request.POST['start'] and request.POST['end'] and request.POST['pos']:
            start_date = request.POST['start']
            end_date = request.POST['end']
            pos = request.POST['pos']
            user = request.user
            print(pos)
            print(user)
            com = Companydb.objects.all()

            cash = Transaction.objects.values(
                'or_number', 'pos_name', 'business_date', 'cardcode', 'voucher', 'plate_num', 'vehicle_type', 'time_in',
                'time_out', 'duration', 'gross_amount', 'discount_special', 'discount_regular', 'vat_exempt_sales',
                'net_amount', 'vat_sales', 'vat', 'cash', 'credit', 'vat_payable', 'vat_spcl_disc').filter(
                business_date__gte=start_date, business_date__lte=end_date, pos_name=pos).order_by('or_number')

            trans = Transaction.objects.filter(
                business_date__gte=start_date, business_date__lte=end_date, pos_name=pos).aggregate(
                gross=Sum('gross_amount'), voucher=Sum('voucher'), vatsales=Sum('vat_sales'), vatamount=Sum('vat'),
                vatexemptsales=Sum('vat_exempt_sales'),
                specialdiscount=Sum('discount_special'), discount=Sum('discount_regular'), netsales=Sum('net_amount'),
                cash=Sum('cash'),
                credit=Sum('credit'), orstart=Min('or_number'), orend=Max('or_number'), txncount=Count('or_number'),
                timein=Min('time_in'), timeout=Max('time_out'), vat_payable=Sum('vat_payable'),
                vat_special=Sum('vat_spcl_disc'))

            context = {
                'cash': cash,
                'com': com,
                'trans': trans,
                'pos': pos,
                'user': user
            }
            html_string = render_to_string('isa/pdf/cashierpospdf.html', context)
            html = HTML(string=html_string)
            result = html.write_pdf()

            # Creating http response
            response = HttpResponse(content_type='application/pdf;')
            response['Content-Disposition'] = 'inline; filename=cashier_detailed_report.pdf'
            response['Content-Transfer-Encoding'] = 'binary'
            with tempfile.NamedTemporaryFile(delete=True) as output:
                output.write(result)
                output.flush()
                output = open(output.name, 'rb')
                response.write(output.read())
            logger.info('cashier pos detailed pdfreport successfully')
            return response
        else:
            logger.info('Missing field')
            return render(request, 'isa/cashier.html', {'error': 'All fields required'})


@login_required(login_url="/accounts/login")
def cashierxl(request):
    operators = Transaction.objects.values('username').distinct()
    pos = Transaction.objects.values('pos_name').distinct()

    context = {
        'operators': operators,
        'pos': pos,
    }
    logger.info('accessing cashierexcel report')
    return render(request, 'isa/excel/cashierxl.html', context)


@login_required(login_url="/accounts/login")
def excel(request):
    if request.method == 'POST':
        if request.POST['start'] and request.POST['end'] and request.POST['operator']:
            start_date = request.POST['start']
            end_date = request.POST['end']
            operator = request.POST['operator']
            user = request.user
            com = Companydb.objects.all()

            cash = Transaction.objects.values(
                'or_number', 'pos_name', 'business_date', 'cardcode', 'voucher', 'plate_num', 'vehicle_type', 'time_in',
                'time_out', 'duration', 'gross_amount', 'discount_special', 'discount_regular', 'vat_exempt_sales',
                'net_amount', 'vat_sales', 'vat', 'cash', 'credit', 'vat_payable', 'vat_spcl_disc').filter(
                business_date__gte=start_date, business_date__lte=end_date, username=operator).order_by('or_number')

            trans = Transaction.objects.filter(
                business_date__gte=start_date, business_date__lte=end_date, username=operator).aggregate(
                gross=Sum('gross_amount'), voucher=Sum('voucher'), vatsales=Sum('vat_sales'), vatamount=Sum('vat'),
                vatexemptsales=Sum('vat_exempt_sales'),
                specialdiscount=Sum('discount_special'), discount=Sum('discount_regular'), netsales=Sum('net_amount'),
                cash=Sum('cash'),
                credit=Sum('credit'), orstart=Min('or_number'), orend=Max('or_number'), txncount=Count('or_number'),
                timein=Min('time_in'), timeout=Max('time_out'), vat_payable=Sum('vat_payable'),
                vat_special=Sum('vat_spcl_disc'))

            context = {
                'start_date': start_date,
                'cash': cash,
                'com': com,
                'trans': trans,
                'operator': operator,
                'user': user,
            }

        else:
            logger.info('Missing field')
            return render(request, 'isa/excel/cashierxl.html', {'error': 'All fields required'})

    return render(request, 'isa/excel/excel.html', context)


@login_required(login_url="/accounts/login")
def cashierposexcel(request):
    if request.method == 'POST':
        if request.POST['start'] and request.POST['end'] and request.POST['pos']:
            start_date = request.POST['start']
            end_date = request.POST['end']
            pos = request.POST['pos']
            user = request.user
            com = Companydb.objects.all()

            cash = Transaction.objects.values(
                'or_number', 'pos_name', 'business_date', 'cardcode', 'voucher', 'plate_num', 'vehicle_type', 'time_in',
                'time_out', 'duration', 'gross_amount', 'discount_special', 'discount_regular', 'vat_exempt_sales',
                'net_amount', 'vat_sales', 'vat', 'cash', 'credit', 'vat_payable', 'vat_spcl_disc').filter(
                business_date__gte=start_date, business_date__lte=end_date, pos_name=pos).order_by('or_number')

            trans = Transaction.objects.filter(
                business_date__gte=start_date, business_date__lte=end_date, pos_name=pos).aggregate(
                gross=Sum('gross_amount'), voucher=Sum('voucher'), vatsales=Sum('vat_sales'), vatamount=Sum('vat'),
                vatexemptsales=Sum('vat_exempt_sales'),
                specialdiscount=Sum('discount_special'), discount=Sum('discount_regular'), netsales=Sum('net_amount'),
                cash=Sum('cash'),
                credit=Sum('credit'), orstart=Min('or_number'), orend=Max('or_number'), txncount=Count('or_number'),
                timein=Min('time_in'), timeout=Max('time_out'), vat_payable=Sum('vat_payable'),
                vat_special=Sum('vat_spcl_disc'))

            context = {
                'pos': pos,
                'user': user,
                'cash': cash,
                'com': com,
                'trans': trans,

            }

        else:
            logger.info('Missing field')
            return render(request, 'isa/excel/cashierxl.html', {'error': 'All fields required'})

    return render(request, 'isa/excel/cashierposexcel.html', context)


@login_required(login_url="/accounts/login")
def cashierallexcel(request):
    if request.method == 'POST':
        if request.POST['start'] and request.POST['end']:
            start_date = request.POST['start']
            end_date = request.POST['end']
            user = request.user
            com = Companydb.objects.all()
            cash = Transaction.objects.values(
                'or_number', 'username', 'pos_name', 'business_date', 'voucher', 'cardcode', 'plate_num',
                'vehicle_type', 'time_in', 'time_out', 'duration', 'gross_amount', 'discount_special',
                'discount_regular', 'vat_exempt_sales', 'net_amount', 'vat_sales', 'vat', 'cash', 'credit',
                'vat_payable', 'vat_spcl_disc').filter(
                business_date__gte=start_date, business_date__lte=end_date).order_by('or_number')

            trans = Transaction.objects.filter(
                business_date__gte=start_date, business_date__lte=end_date).aggregate(
                gross=Sum('gross_amount'), vatsales=Sum('vat_sales'), vatamount=Sum('vat'),
                vatexemptsales=Sum('vat_exempt_sales'),
                specialdiscount=Sum('discount_special'), discount=Sum('discount_regular'), netsales=Sum('net_amount'),
                cash=Sum('cash'),
                credit=Sum('credit'), orstart=Min('or_number'), orend=Max('or_number'), txncount=Count('or_number'),
                timein=Min('time_in'), voucher=Sum('voucher'), timeout=Max('time_out'), vat_payable=Sum('vat_payable'),
                vat_special=Sum('vat_spcl_disc'))

            context = {
                'start_date': start_date,
                'cash': cash,
                'com': com,
                'user': user,
                'trans': trans,
            }

        else:
            logger.info('Missing field')
            return render(request, 'isa/cashier.html', {'error': 'All fields required'})

    return render(request, 'isa/excel/cashierallexcel.html', context)


@login_required(login_url="/accounts/login")
def example(request):
    if request.method == 'POST':

        if request.POST['trno'] and request.POST['businessdate'] and request.POST['transaction'] and request.POST[
            'vehicle'] and request.POST['plate'] and request.POST['timein'] and request.POST['timeout'] and \
                request.POST['net_sales'] and request.POST['vat'] and request.POST['total']:

            busnessdate = request.POST['businessdate']
            trno = request.POST['trno']
            vat = request.POST['vat']
            dtype = request.POST['transaction']
            remarks = request.POST['remarks']
            plate = request.POST['plate']
            timein = request.POST['timein']
            timeout = request.POST['timeout']
            vehicle = request.POST['vehicle']
            total = request.POST['total']
            vatable = request.POST['vatable']

            vat_adjustment = request.POST['vat_adjustment']
            vat_payable = request.POST['vat_payable']
            regular_discount = request.POST['regular_discount']
            net_sales = request.POST['net_sales']
            vatexempt = request.POST['vatexempt']
            special_discount = request.POST['special_discount']

            parker_name = request.POST['parker_name']
            parker_id = request.POST['parker_id']
            operator = request.user
            date_entry = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            try:
                trans = ManualTransaction(business_date=busnessdate, operator=operator, ticket_no=trno,
                                          discount_type=dtype, plate_number=plate, time_in=timein, time_out=timeout,
                                          vehicle_type=vehicle, gross_amount=total, vatable_sale=vatable, vat=vat,
                                          net_sales=net_sales, date_entry=date_entry, remarks=remarks,
                                          parker_name=parker_name, parker_id=parker_id,
                                          regular_discount=regular_discount, vat_exempt_sale=vatexempt,
                                          special_discount=special_discount, vat_adjustment=vat_adjustment,
                                          vat_payable=vat_payable, pos_name='manual')
                trans.save()
            except IntegrityError as e:
                return render(request, 'isa/example.html', {'error': 'Ticket Number Already Exist.'})
            messages.success(request, 'Data submission successful')
            logger.info('insert new data successfully')
            return redirect('/isa/example')
        else:
            logger.info('Missing field')
            return render(request, 'isa/example.html', {'error': '* fields are required'})
    else:
        logger.info('inserting new data')
        return render(request, 'isa/example.html')


@login_required(login_url="/accounts/login")
def manualreport(request):
    tocash = ManualTransaction.objects.values('ticket_no', 'business_date', 'operator', 'plate_number', 'time_in',
                                              'parker_name', 'parker_id', 'time_out', 'vehicle_type', 'gross_amount',
                                              'vatable_sale', 'vat', 'discount_type', 'vat_exempt_sale',
                                              'regular_discount', 'special_discount', 'vat_adjustment', 'vat_payable',
                                              'net_sales', 'remarks', 'parker_name', 'parker_id',
                                              'date_entry').order_by('-date_entry')[:10]

    return render(request, 'isa/manualreport.html', {'tocash': tocash}, )


class Manual(APIView):
    def get(self, request):
        logger.info('accessing manual ticketing report')
        return render(request, 'isa/manual.html')

    def post(self):
        print("dsadasda")


@login_required(login_url="/accounts/login")
def manual(request):
    logger.info('accessing manual ticketing report')
    return render(request, 'isa/manual.html')


@login_required(login_url="/accounts/login")
def manualpdf(request):
    if request.method == 'POST':
        if request.POST['start'] and request.POST['end']:
            start_date = request.POST['start']
            end_date = request.POST['end']
            user = request.user
            # cash = ManualTransaction.objects.values('ticket_no', 'business_date', 'vat_payable', 'operator', 'plate_number', 'time_in', 'time_out', 'vehicle_type', 'gross_amount', 'vatable_sale', 'vat', 'discount_type', 'vat_exempt_sale', 'regular_discount', 'special_discount', 'vat_adjustment', 'vat_payable', 'net_sales', 'remarks', 'parker_name', 'parker_id', 'date_entry', 'operator').filter(business_date__gte=start_date, business_date__lte=end_date).order_by('date_entry')
            com = Companydb.objects.all()
            cash = ManualTransaction.objects.raw(
                'select ticket_no, vat as id, CONCAT(TIMESTAMPDIFF(day,time_in,time_out) , "  Day(s) ", MOD( TIMESTAMPDIFF(hour,time_in,time_out), 24), " Hr(s) ", MOD( TIMESTAMPDIFF(minute,time_in,time_out), 60), " Min(s) ") AS duration, business_date, vat_payable, operator, plate_number, time_in, time_out, vehicle_type, gross_amount, vatable_sale, vat, discount_type, vat_exempt_sale, regular_discount, special_discount, vat_adjustment, vat_payable, net_sales, remarks, parker_name, parker_id, date_entry, operator from manual_transaction where business_date between %s and %s;',
                [start_date, end_date])
            tocash = ManualTransaction.objects.filter(
                business_date__gte=start_date, business_date__lte=end_date).aggregate(
                gross=Sum('gross_amount'), vatsales=Sum('vatable_sale'), vatamount=Sum('vat'),
                vatexemptsales=Sum('vat_exempt_sale'),
                specialdiscount=Sum('special_discount'), discount=Sum('regular_discount'), netsales=Sum('net_sales'),
                orstart=Min('ticket_no'), max_date=Max('business_date'), min_date=Min('business_date'),
                orend=Max('ticket_no'), txncount=Count('ticket_no'),
                timein=Min('time_in'), timeout=Max('time_out'), vat_payable=Sum('vat_payable'),
                vat_special=Sum('vat_adjustment'))

            context = {
                'start_date': start_date,
                'end_date': end_date,
                'cash': cash,
                'com': com,
                'tocash': tocash,
                'user': user,
            }

        else:
            logger.info('Missing field')
            return render(request, 'isa/manual.html', {'error': 'All fields required'})

    # Rendered

    html_string = render_to_string('isa/pdf/manualpdf.html', context)
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=cash_report.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())
    logger.info('manual ticketing pdfreport generated successfully')
    return response


@login_required(login_url="/accounts/login")
def manualxl(request):
    logger.info('accessing manual ticketing report')
    return render(request, 'isa/excel/manualxl.html', )


@login_required(login_url="/accounts/login")
def manualexcel(request):
    if request.method == 'POST':
        if request.POST['start'] and request.POST['end']:
            start_date = request.POST['start']
            end_date = request.POST['end']
            com = Companydb.objects.all()
            user = request.user

            cash = ManualTransaction.objects.values('ticket_no', 'business_date', 'operator', 'plate_number', 'time_in',
                                                    'time_out', 'vehicle_type', 'gross_amount', 'vatable_sale', 'vat',
                                                    'discount_type', 'vat_exempt_sale', 'regular_discount',
                                                    'special_discount', 'vat_adjustment', 'vat_payable', 'net_sales',
                                                    'remarks', 'parker_name', 'parker_id', 'date_entry',
                                                    'operator').filter(business_date__gte=start_date,
                                                                       business_date__lte=end_date).order_by(
                'date_entry')

            tocash = ManualTransaction.objects.filter(
                business_date__gte=start_date, business_date__lte=end_date).aggregate(
                gross=Sum('gross_amount'), vatsales=Sum('vatable_sale'), vatamount=Sum('vat'),
                vatexemptsales=Sum('vat_exempt_sale'),
                specialdiscount=Sum('special_discount'), discount=Sum('regular_discount'), netsales=Sum('net_sales'),
                orstart=Min('ticket_no'), orend=Max('ticket_no'), txncount=Count('ticket_no'),
                timein=Min('time_in'), timeout=Max('time_out'), vat_payable=Sum('vat_payable'),
                vat_special=Sum('vat_adjustment'))

            context = {
                'start_date': start_date,
                'end_date': end_date,
                'cash': cash,
                'com': com,
                'tocash': tocash,
                'user': user,
            }

        else:
            logger.info('Missing field')
            return render(request, 'isa/excel/manualxl.html', {'error': 'All fields required'})

    return render(request, 'isa/excel/manualexcel.html', context)


def occupancy(request):
    return render(request, 'isa/occupancy.html')


def occupancypdf(request):
    com = Companydb.objects.all()
    context = {
        'com': com,
    }

    html_string = render_to_string('isa/pdf/occupancypdf.html', context)
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=occupancy_report.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())
    logger.info('occupancy pdfreport generated successfully')
    return response


@login_required(login_url="/accounts/login")
def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        try:
            validate_email(email)
        except ValidationError as e:
            return render(request, 'isa/register.html', {'error': 'Invalid Email'})

        exists = User.objects.filter(email=email)

        if exists:
            return render(request, 'isa/register.html', {'error': 'Email already exist.'})

        exists_user = User.objects.filter(username=username)

        if exists_user:
            return render(request, 'isa/register.html', {'error': 'Username already exist.'})

        if request.POST['password'] == request.POST['confirm-password']:
            user = User.objects.create_user(request.POST['username'], password=request.POST['password'],
                                            email=request.POST['email'])
            auth.login(request, user)
            return redirect('/')
        else:
            return render(request, 'isa/register.html', {'error': 'Password must match'})
    else:
        return render(request, 'isa/register.html')


@login_required(login_url="/accounts/login")
def register_done(request):
    user = request.user
    return render(request, 'isa/register_done.html', {'user': user})


@login_required(login_url="/accounts/login")
def operator_reg(request):
    return render(request, 'isa/operator_reg.html')


def hash_password(password):
    # uuid is used to generate a random number
    salt = os.urandom(16)  # A new salt for this user
    salts = base64.b64encode(salt)
    key = hashlib.pbkdf2_hmac('sha1', password.encode('utf-8'), salt, iterations=1000, dklen=20)
    keys = base64.b64encode(key)
    return f"1000:{salts.decode('utf-8')}:{keys.decode('utf-8')}"


def on_publish(client, userdata, result):  # create function for callback
    print("data published \n")


@login_required(login_url="/accounts/login")
def operator_done(request):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['confirm-password']:
            if request.POST['username'] and request.POST['password'] and request.POST['firstname'] and request.POST[
                'lastname'] and request.POST['status'] and request.POST['role']:
                username = request.POST['username']
                # custom_pbkdf2 = pbkdf2_sha256.using(rounds=30000)
                password = hash_password(request.POST['password'])
                firstname = request.POST['firstname']
                lastname = request.POST['lastname']
                nickname = request.POST['nickname']
                status = request.POST['status']
                role = request.POST['role']

                client = mqtt.Client()
                # client.on_connect = on_connect
                client.on_message = on_message
                client.on_publish = on_publish
                client.connect("127.0.0.1", 1883, 60)
                payload = {"username": username,
                           "password": password,
                           "firstname": firstname,
                           "lastname": lastname,
                           "nickname": nickname,
                           "status": status,
                           "role": role}

                client.loop_start()
                clean_payload = json.dumps(payload)
                client.publish('user_reg', clean_payload)
                try:
                    cursor = connections['default'].cursor()
                    cursor.execute(
                        'INSERT INTO users(username, salted_hash, firstname, lastname, nickname, status, user_roles) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                        [username, password, firstname, lastname, nickname, status, role])
                except IntegrityError as e:
                    return render(request, 'isa/operator_reg.html', {'error': 'Username Already Exist.'})
                return render(request, 'isa/operator_done.html')
            else:
                return render(request, 'isa/operator_reg.html', {'error': 'All fields are required'})
        else:
            return render(request, 'isa/operator_reg.html', {'error': 'Password must match'})


@login_required(login_url="/accounts/login")
def change_password(request):
    users = Users.objects.values("username").distinct()

    return render(request, 'isa/change_password.html', {'users': users})


def check_password(has_password, user_password):
    salt = has_password[5:29]
    salts = base64.b64decode(salt)
    key = has_password[30:]
    new_key = hashlib.pbkdf2_hmac('sha1', user_password.encode('utf-8'), salts, iterations=1000)
    keys = base64.b64decode(key)
    return keys == new_key


@login_required(login_url="/accounts/login")
def change_password_done(request):
    if request.method == 'POST':
        user = request.POST['username']
        password = request.POST['oldpassword']
        new_password = request.POST['newpassword']

        get_password = Users.objects.values_list('salted_hash', flat=True).values('salted_hash').get(username=user)
        get_old_password = get_password.get('salted_hash')
        return_password = check_password(get_old_password, password)

        if request.POST['newpassword'] != request.POST['confpassword']:
            return render(request, 'isa/change_password.html',
                          {'error': 'New Password and Confirm Password must match'}, )

        if return_password != True:
            return render(request, 'isa/change_password.html', {'error': 'Wrong Old Password'}, )

        if new_password == request.POST['confpassword'] and return_password == True:
            user = request.POST['username']
            hash_new_password = hash_password(new_password)
            Users.objects.filter(username=user).update(salted_hash=hash_new_password)

            return render(request, 'isa/change_password_done.html', )
    else:
        return render(request, 'isa/change_password.html', )


def on_connect(client, userdata, flags, rc):
    print("Connected with Code :" + str(rc))
    # Subscribe Topic from here
    # client.subscribe("arduino")
    # print(m.get())
    # print(t.get())
    # x = client.subscribe("arduino")


def on_message(client, userdata, msg):
    # data_for = "{'" + str(msg.payload) + "', " + str(msg.topic) + "}"
    # print(str(msg.payload))
    # global glob
    pay = msg.payload
    # print(msg.topic)
    # ad = yaml.safe_load(pay)
    # s = json.dumps(ad, indent=4, sort_keys=True)
    global sub_message
    sub_message = pay
    print(sub_message)
    # glob = s
    # print(glob)
    # print(s)


def connection_true():
    client = mqtt.Client()
    # client.on_connect = on_connect
    client.on_message = on_message
    client.on_publish = on_publish
    client.connect("127.0.0.1", 1883, 60)
    client.loop_start()
    # payload = {"logs": "realtime", "value": var2}
    # clean_payload = json.dumps(payload)
    client.publish('oki', 'messagesssesa')


sub_message = ''


def sub():
    client = mqtt.Client()
    # client.on_connect = on_connect
    client.on_message = on_message
    client.connect("127.0.0.1", 1883, 60)
    client.loop_start()
    client.subscribe("test")
