from django.db import models
from datetime import datetime


class Tblpermit(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    pc = models.CharField(db_column='PC', max_length=100, blank=True, null=True)  # Field name made lowercase.
    min = models.CharField(db_column='MIN', max_length=255, blank=True, null=True)  # Field name made lowercase.
    serial = models.CharField(db_column='Serial', max_length=255, blank=True, null=True)  # Field name made lowercase.
    accred = models.CharField(db_column='Accred', max_length=255, blank=True, null=True)  # Field name made lowercase.
    dateissued = models.CharField(db_column='DateIssued', max_length=255, blank=True, null=True)  # Field name made lowercase.
    permit = models.CharField(db_column='Permit', max_length=255, blank=True, null=True)  # Field name made lowercase.
    vatreg = models.CharField(db_column='VATReg', max_length=255, blank=True, null=True)  # Field name made lowercase.
    accreddate = models.CharField(db_column='AccredDate', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
      
        db_table = 'tblpermit'


class Companydb(models.Model):
    company = models.CharField(db_column='Company', max_length=255, blank=True, null=True)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=255, blank=True, null=True)  # Field name made lowercase.
    tel = models.CharField(db_column='Tel', max_length=255, blank=True, null=True)  # Field name made lowercase.
    tin = models.CharField(db_column='TIN', max_length=255, blank=True, null=True)  # Field name made lowercase.
    permit = models.CharField(db_column='Permit', max_length=255, blank=True, null=True)  # Field name made lowercase.
    parkingslot = models.BigIntegerField(db_column='ParkingSlot', blank=True, null=True)  # Field name made lowercase.
    parkingarea = models.CharField(db_column='ParkingArea', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
      
        db_table = 'companydb'

class Transaction(models.Model):
    pos_name = models.CharField(max_length=45, blank=True, null=True)
    pos = models.ForeignKey(Tblpermit, on_delete=models.CASCADE,null=True, related_name='name_pos')
    cardcode = models.CharField(max_length=45, blank=True, null=True)
    or_number = models.CharField(max_length=45, blank=True, null=True)
    time_in = models.DateTimeField(blank=True, null=True)
    time_out = models.DateTimeField(blank=True, null=True)
    duration = models.CharField(max_length=45, blank=True, null=True)
    vehicle_type = models.CharField(max_length=45, blank=True, null=True)
    plate_num = models.CharField(max_length=45, blank=True, null=True)
    username = models.CharField(max_length=45, blank=True, null=True)
    transaction_datetime = models.DateTimeField(blank=True, null=True)
    business_date = models.DateField(blank=True, null=True)
    fee_parking = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fee_overnight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fee_lostcard = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fee_damagedcard = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    gross_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    discount_name = models.CharField(max_length=45, blank=True, null=True)
    discount_regular = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    discount_special = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    net_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    cash_tendered = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    cash_change = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    vat_sales = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    vat = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    vat_payable = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    vat_exempt_sales = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    vat_spcl_disc = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    vat_zero_rated_sales = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    vehicle_class = models.CharField(max_length=45, blank=True, null=True)
    parker_name = models.CharField(max_length=45, blank=True, null=True)
    parker_address = models.CharField(max_length=45, blank=True, null=True)
    parker_tin = models.CharField(max_length=45, blank=True, null=True)
    parker_ref_id = models.CharField(max_length=45, blank=True, null=True)
    re_print = models.IntegerField(blank=True, null=True)
    parking_class = models.CharField(max_length=45, blank=True, null=True)
    cash = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    credit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    voucher = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    coupon = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    gcash = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    beep = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    paymaya = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    succeeding_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        db_table = 'transaction'

class ManualTransaction(models.Model):
    ticket_no = models.IntegerField(unique=True)
    business_date = models.DateField()
    operator = models.CharField(max_length=40)
    plate_number = models.CharField(max_length=40, blank=True, null=True)
    time_in = models.DateTimeField()
    time_out = models.DateTimeField()
    vehicle_type = models.CharField(max_length=40, blank=True, null=True)
    gross_amount = models.DecimalField(max_digits=10, decimal_places=2)
    vatable_sale = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    vat = models.DecimalField(max_digits=10, decimal_places=2)
    discount_type = models.CharField(max_length=40)
    vat_exempt_sale = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    regular_discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    special_discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    vat_adjustment = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    vat_payable = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    net_sales = models.DecimalField(max_digits=10, decimal_places=2)
    date_entry = models.DateTimeField()
    remarks = models.CharField(max_length=40)
    parker_name = models.CharField(max_length=40, blank=True, null=True)
    parker_id = models.CharField(max_length=40, blank=True, null=True)
    pos_name = models.CharField(max_length=10, blank=True)

    class Meta:
     
        db_table = 'manual_transaction'

class ChargingRule(models.Model):
    name = models.CharField(max_length=100)
    vehicle = models.CharField(max_length=100)
    minimum_minutes = models.IntegerField()
    minimum_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    succeeding_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    flat_rate =  models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    overnight_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    lost_card = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    command = models.CharField(max_length=10)
    overnight_start = models.TimeField(null=True, blank=True)
    overnight_end = models.TimeField(null=True, blank=True)
    ov_24 = models.SmallIntegerField(null=True, blank=True)
    int_time = models.SmallIntegerField(null=True, blank=True)
    isTF = models.SmallIntegerField(null=True, blank=True)
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('disabled', 'Disabled'),
    )
    status = models.CharField(max_length=9, choices=STATUS_CHOICES, default='active')

    class Meta:

        db_table = 'charging_rule'
        verbose_name_plural = 'charging_rules'

class FlatRateDays(models.Model):

    rule_name = models.CharField(max_length=100)
    monday = models.SmallIntegerField(null=True, blank=True)
    tuesday = models.SmallIntegerField(null=True, blank=True)
    wednesday = models.SmallIntegerField(null=True, blank=True)
    thursday = models.SmallIntegerField(null=True, blank=True)
    friday = models.SmallIntegerField(null=True, blank=True)
    saturday = models.SmallIntegerField(null=True, blank=True)
    sunday = models.SmallIntegerField(null=True, blank=True)
    holiday = models.CharField(max_length=100, null=True, blank=True)

    class Meta:

        db_table = 'flatrate_days'
        verbose_name_plural = 'flatrate_days'

class Discount(models.Model):

    discount_type = models.CharField(max_length=100)
    vat_exempt = models.SmallIntegerField(null=True, blank=True)
    percentage = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    is_free = models.SmallIntegerField(null=True, blank=True)
    status = models.SmallIntegerField(null=True, blank=True)

    class Meta:

        db_table = 'discount'
        verbose_name_plural = 'discounts'

class DiscountFix(models.Model):

    discount_type = models.CharField(max_length=100)
    vat_exempt = models.SmallIntegerField(null=True, blank=True)
    percentage = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    is_free = models.SmallIntegerField(null=True, blank=True)
    status = models.SmallIntegerField(null=True, blank=True)

    class Meta:

        db_table = 'discount_fix'
        verbose_name_plural = 'discount_fix'

class Vouchers(models.Model):

    voucher_type = models.CharField(max_length=100)
    amount_value = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    status = models.SmallIntegerField(null=True, blank=True)

    class Meta:

        db_table = 'vouchers'
        verbose_name_plural = 'vouchers'

class NonCash(models.Model):

    name = models.CharField(max_length=100)
    status = models.SmallIntegerField()

    class Meta:

        db_table = 'non_cash'
        verbose_name_plural = 'non_cash'

class Holiday(models.Model):

    holiday_date = models.DateField(null=True)
    name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:

        db_table = 'holiday'
        verbose_name_plural = 'holidays'

class UserRoles(models.Model):
    rule_name = models.CharField(unique=True,max_length=50)
    server_set = models.IntegerField()
    user_set = models.IntegerField()
    device_set = models.IntegerField()
    charging_set = models.IntegerField()
    report_set = models.IntegerField()
    terminate_set = models.IntegerField()
    set_reference = models.IntegerField()
    syslog_setting = models.IntegerField()
    cashier = models.IntegerField()
    log_report = models.IntegerField()

    class Meta:
        db_table = 'user_roles'

class Users(models.Model):
    username = models.CharField(unique=True, max_length=45)
    salted_hash = models.CharField(max_length=87)
    firstname = models.CharField(max_length=45)
    lastname = models.CharField(max_length=45)
    nickname = models.CharField(max_length=45, default=0.00)
    status = models.IntegerField(blank=True, null=True)
    user_roles = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'users'

class TransactionZeroAmount(models.Model):
    transaction_datetime = models.DateTimeField(blank=True, null=True)
    business_date = models.DateField(blank=True, null=True)
    vehicle_type = models.CharField(max_length=45, blank=True, null=True)
    time_in = models.DateTimeField(blank=True, null=True)
    time_out = models.DateTimeField(blank=True, null=True)
    pos_name = models.CharField(max_length=45, blank=True, null=True)
    username = models.CharField(max_length=45, blank=True, null=True)
    parker_type = models.CharField(max_length=45, blank=True, null=True)
    parker_name = models.CharField(max_length=45, blank=True, null=True)
    parker_address = models.CharField(max_length=45, blank=True, null=True)
    parker_ref_id = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        db_table = 'transaction_zero_amount'
