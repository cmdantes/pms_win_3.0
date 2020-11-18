from django.conf.urls import url
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('income', views.income, name='income'),
    path('bir', views.bir, name='bir'),

    path('cash', views.cash, name='cash'),
    path('cashpdf', views.cashpdf, name='cashpdf'),
    path('cashallpdf', views.cashallpdf, name='cashallpdf'),
    path('cashpospdf', views.cashpospdf, name='cashpospdf'),

    path('vehicle', views.vehicle, name='vehicle'),

    path('vehiclepdf', views.vehiclepdf, name='vehiclepdf'),
    path('vehiclepdfbdate', views.vehiclepdfbdate, name='vehiclepdfbdate'),

    path('cashier', views.cashier, name='cashier'),
    path('cashierpdf', views.cashierpdf, name='cashierpdf'),
    path('cashierpospdf', views.cashierpospdf, name='cashierpospdf'),
    path('cashierallpdf', views.cashierallpdf, name='cashierallpdf'),

    path('transaction', views.transaction, name='transaction'),
    path('transactionpdf', views.transactionpdf, name='transactionpdf'),

    path('cashierxl', views.cashierxl, name='cashierxl'),
    path('excel', views.excel, name='excel'),
    path('cashierposexcel', views.cashierposexcel, name='cashierposexcel'),
    path('cashierallexcel', views.cashierallexcel, name='cashierallexcel'),

    path('transactionxl', views.transactionxl, name='transactionxl'),
    path('transactionexcel', views.transactionexcel, name='transactionexcel'),

    path('stay_in', views.stay_in, name='stay_in'),
    path('stay_inpdf', views.stay_inpdf, name='stay_inpdf'),
    path('birmonthly', views.birmonthly, name='birmonthly'),

    path('discountpos', views.discountpos, name='discountpos'),
    path('seniorpospdf', views.seniorpospdf, name='seniorpospdf'),

    path('example', views.example, name='example'),

    path('manual', views.manual, name='manual'),
    path('manualpdf', views.manualpdf, name='manualpdf'),
    path('manualxl', views.manualxl, name='manualxl'),
    path('manualexcel', views.manualexcel, name='manualexcel'),
    path('manualreport', views.manualreport, name='manualreport'),

    path('occupancy', views.occupancy, name='occupancy'),
    path('occupancypdf', views.occupancypdf, name='occupancypdf'),

    path('register', views.register, name='register'),
    path('register_done', views.register_done, name='register_done'),

    path('operator_reg', views.operator_reg, name='operator_reg'),
    path('operator_done', views.operator_done, name='operator_done'),

    path('change_password', views.change_password, name='change_password'),
    path('change_password_done', views.change_password_done, name='change_password_done'),
]
