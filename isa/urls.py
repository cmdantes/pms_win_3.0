from django.conf.urls import url
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    url(r"^cashier$", views.CashierPDF.view, name='cashier'),
    url(r"^cashierpdf$", views.CashierPDF.renderPDF, name='cashierpdf'),

    url(r"^cashierExcel$", views.CashierExcel.as_view(), name='cashierxl'),

    url(r"^transaction$", views.Transactions.view, name='transaction'),
    url(r"^transactionpdf$", views.Transactions.renderPDF, name='transactionpdf'),

    url(r"^transactionxl$", views.TransactionsExcel.as_view(), name='transactionxl'),

    url(r"^manual$", views.ManualPDF.view, name='manual'),
    url(r"^manualpdf$", views.ManualPDF.renderPDF, name='manualpdf'),

    url(r"^manualtrans$", views.ManualTransPDF.view, name='manualtrans'),
    url(r"^manualtranspdf$", views.ManualTransPDF.renderPDF, name='manualtranspdf'),

    url(r"^manualxl$", views.ManualExcel.as_view(), name='manualxl'),

    url(r"^cash$", views.Cash.view, name='cash'),
    url(r"^cashpdf$", views.Cash.renderPDF, name='cashpdf'),

    url(r"^vehicle$", views.Vehicle.view, name='vehicle'),
    url(r"^vehiclepdf$", views.Vehicle.renderPDF, name='vehiclepdf'),

    url(r"^stay_in$", views.StayIn.view, name='stay_in'),
    url(r"^stay_inpdf$", views.StayIn.renderPDF, name='stay_inpdf'),

    url(r"^discount$", views.Discounts.view, name='discount'),
    url(r"^discountpdf$", views.Discounts.renderPDF, name='discountpost'),

    url(r"^birmonthly$", views.BIRMonthly.view, name='birmonthly'),
    url(r"^birmonthlypdf$", views.BIRMonthly.renderPDF, name='birmonthlypdf'),

    url(r"^occupancy$", views.Occupancies.view, name='occupancy'),
    url(r"^occupancypdf$", views.Occupancies.renderPDF, name='occupancypdf'),

    url(r"^ticket$", views.ManualTicketEncoding.as_view(), name='example'),

    url(r"^zoroamount$", views.ZeroAmount.view, name='zeramount'),
    url(r"^zoroamountpdf$", views.ZeroAmount.renderPDF, name='zeramountpdf'),

    path('manualreport', views.manualreport, name='manualreport'),

    path('register', views.register, name='register'),
    path('register_done', views.register_done, name='register_done'),

    path('operator_reg', views.operator_reg, name='operator_reg'),
    path('operator_done', views.operator_done, name='operator_done'),

    path('change_password', views.change_password, name='change_password'),
    path('change_password_done', views.change_password_done, name='change_password_done'),
]
