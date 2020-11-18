# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class BirAcountdb(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(db_column='Name', max_length=50, blank=True, null=True)  # Field name made lowercase.
    idno = models.CharField(db_column='IDNo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    username = models.CharField(db_column='Username', max_length=20, blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bir_acountdb'


class BirPrintLog(models.Model):
    bir_user = models.CharField(db_column='BIR_User', max_length=30, blank=True, null=True)  # Field name made lowercase.
    bir_id = models.CharField(db_column='BIR_ID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    log_date = models.DateTimeField(db_column='Log_Date', blank=True, null=True)  # Field name made lowercase.
    or_num = models.CharField(db_column='OR_Num', max_length=255, blank=True, null=True)  # Field name made lowercase.
    t_num = models.BigIntegerField(db_column='T_Num', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bir_print_log'


class Birdate(models.Model):
    id = models.BigAutoField(primary_key=True)
    lastdate = models.DateField(db_column='LastDate', blank=True, null=True)  # Field name made lowercase.
    generateby = models.CharField(db_column='GenerateBy', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'birdate'


class Card(models.Model):
    id = models.BigAutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    cardcode = models.CharField(db_column='CardCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    owneridno = models.CharField(db_column='OwnerIdNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ownername = models.CharField(db_column='OwnerName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    position = models.CharField(db_column='Position', max_length=30, blank=True, null=True)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=100, blank=True, null=True)  # Field name made lowercase.
    contact = models.CharField(db_column='Contact', max_length=50, blank=True, null=True)  # Field name made lowercase.
    plate = models.CharField(db_column='Plate', max_length=255, blank=True, null=True)  # Field name made lowercase.
    vehicletype = models.CharField(db_column='VehicleType', max_length=20, blank=True, null=True)  # Field name made lowercase.
    privilege = models.CharField(db_column='Privilege', max_length=10, blank=True, null=True)  # Field name made lowercase.
    dateenrolled = models.DateField(db_column='DateEnrolled', blank=True, null=True)  # Field name made lowercase.
    expiratiodate = models.DateField(db_column='ExpiratioDate', blank=True, null=True)  # Field name made lowercase.
    graceperiod = models.DateField(db_column='GracePeriod', blank=True, null=True)  # Field name made lowercase.
    cardmode = models.CharField(db_column='CardMode', max_length=2, blank=True, null=True)  # Field name made lowercase.
    pic1 = models.TextField(db_column='Pic1', blank=True, null=True)  # Field name made lowercase.
    deptname = models.CharField(db_column='DeptName', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'card'


class Companydb(models.Model):
    company = models.CharField(db_column='Company', max_length=255, blank=True, null=True)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=255, blank=True, null=True)  # Field name made lowercase.
    tel = models.CharField(db_column='Tel', max_length=255, blank=True, null=True)  # Field name made lowercase.
    tin = models.CharField(db_column='TIN', max_length=255, blank=True, null=True)  # Field name made lowercase.
    permit = models.CharField(db_column='Permit', max_length=255, blank=True, null=True)  # Field name made lowercase.
    parkingslot = models.BigIntegerField(db_column='ParkingSlot', blank=True, null=True)  # Field name made lowercase.
    parkingarea = models.CharField(db_column='ParkingArea', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'companydb'


class DevicesDevices(models.Model):
    name = models.CharField(max_length=50)
    status = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'devices_devices'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DrsAwlpt(models.Model):
    id = models.BigAutoField(primary_key=True)
    cid = models.CharField(db_column='CID', max_length=100, blank=True, null=True)  # Field name made lowercase.
    lpt = models.FloatField(db_column='LPT', blank=True, null=True)  # Field name made lowercase.
    trno = models.CharField(db_column='TRNO', max_length=240, blank=True, null=True)  # Field name made lowercase.
    station = models.CharField(db_column='Station', max_length=100, blank=True, null=True)  # Field name made lowercase.
    operator = models.CharField(db_column='Operator', max_length=100, blank=True, null=True)  # Field name made lowercase.
    docnum = models.CharField(db_column='Docnum', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'drs_awlpt'


class DrsComp(models.Model):
    di = models.BigAutoField(primary_key=True)
    docnum = models.CharField(db_column='Docnum', max_length=250, blank=True, null=True)  # Field name made lowercase.
    cid = models.CharField(db_column='Cid', max_length=100, blank=True, null=True)  # Field name made lowercase.
    cname = models.CharField(db_column='Cname', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ornum = models.CharField(db_column='ORnum', max_length=254, blank=True, null=True)  # Field name made lowercase.
    operator = models.CharField(db_column='Operator', max_length=100, blank=True, null=True)  # Field name made lowercase.
    pos = models.CharField(db_column='POS', max_length=100, blank=True, null=True)  # Field name made lowercase.
    tdate = models.DateTimeField(db_column='Tdate', blank=True, null=True)  # Field name made lowercase.
    tval = models.FloatField(db_column='Tval', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'drs_comp'


class DrsLpr(models.Model):
    id = models.BigAutoField(primary_key=True)
    docnum = models.CharField(db_column='DocNum', max_length=250, blank=True, null=True)  # Field name made lowercase.
    cname = models.CharField(db_column='Cname', max_length=100, blank=True, null=True)  # Field name made lowercase.
    tdate = models.DateTimeField(db_column='Tdate', blank=True, null=True)  # Field name made lowercase.
    operator = models.CharField(db_column='Operator', max_length=100, blank=True, null=True)  # Field name made lowercase.
    station = models.CharField(db_column='Station', max_length=100, blank=True, null=True)  # Field name made lowercase.
    tval = models.FloatField(db_column='Tval', blank=True, null=True)  # Field name made lowercase.
    ornum = models.CharField(db_column='ORnum', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'drs_lpr'


class Enrolledcards(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    cardcode = models.CharField(db_column='Cardcode', max_length=100, blank=True, null=True)  # Field name made lowercase.
    timeenrolled = models.DateTimeField(db_column='TimeEnrolled', blank=True, null=True)  # Field name made lowercase.
    admin = models.CharField(db_column='Admin', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'enrolledcards'


class FlatrateSchedule(models.Model):
    day = models.IntegerField(db_column='Day', blank=True, null=True)  # Field name made lowercase.
    starttime = models.TimeField(db_column='StartTime', blank=True, null=True)  # Field name made lowercase.
    isstart = models.IntegerField(db_column='IsStart', blank=True, null=True)  # Field name made lowercase.
    isend = models.IntegerField(db_column='IsEnd', blank=True, null=True)  # Field name made lowercase.
    graceex = models.BigIntegerField(db_column='GraceEX', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'flatrate_schedule'


class Historydb(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    cardcode = models.CharField(db_column='CardCode', max_length=255, blank=True, null=True)  # Field name made lowercase.
    plate = models.CharField(db_column='Plate', max_length=255, blank=True, null=True)  # Field name made lowercase.
    dtime = models.DateTimeField(db_column='DTime', blank=True, null=True)  # Field name made lowercase.
    lane = models.CharField(db_column='Lane', max_length=30, blank=True, null=True)  # Field name made lowercase.
    pic = models.TextField(db_column='PIC', blank=True, null=True)  # Field name made lowercase.
    pic2 = models.TextField(db_column='PIC2', blank=True, null=True)  # Field name made lowercase.
    zone = models.CharField(db_column='Zone', max_length=30, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'historydb'


class Hourlydb(models.Model):
    id = models.BigAutoField(primary_key=True)
    vehicle = models.CharField(db_column='Vehicle', max_length=255, blank=True, null=True)  # Field name made lowercase.
    mark = models.CharField(db_column='Mark', max_length=255, blank=True, null=True)  # Field name made lowercase.
    grace = models.BigIntegerField(blank=True, null=True)
    firstminutes = models.BigIntegerField(db_column='FirstMinutes', blank=True, null=True)  # Field name made lowercase.
    firstamount = models.FloatField(db_column='firstAmount', blank=True, null=True)  # Field name made lowercase.
    intamount = models.FloatField(db_column='IntAmount', blank=True, null=True)  # Field name made lowercase.
    flatrate = models.FloatField(db_column='Flatrate', blank=True, null=True)  # Field name made lowercase.
    overnight = models.FloatField(db_column='OverNight', blank=True, null=True)  # Field name made lowercase.
    lostcard = models.FloatField(db_column='LostCard', blank=True, null=True)  # Field name made lowercase.
    command = models.CharField(db_column='Command', max_length=10, blank=True, null=True)  # Field name made lowercase.
    ov_start = models.TimeField(db_column='OV_Start', blank=True, null=True)  # Field name made lowercase.
    ov_end = models.TimeField(db_column='OV_End', blank=True, null=True)  # Field name made lowercase.
    status = models.IntegerField(db_column='Status', blank=True, null=True)  # Field name made lowercase.
    ov24 = models.IntegerField(db_column='OV24', blank=True, null=True)  # Field name made lowercase.
    inttime = models.IntegerField(db_column='IntTime', blank=True, null=True)  # Field name made lowercase.
    istf = models.IntegerField(db_column='isTF')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'hourlydb'


class InOutLogs(models.Model):
    rfid = models.CharField(max_length=45, blank=True, null=True)
    lpr = models.CharField(max_length=45, blank=True, null=True)
    face_recognition = models.CharField(max_length=45, blank=True, null=True)
    fingerprint = models.CharField(max_length=45, blank=True, null=True)
    beacon = models.CharField(max_length=45, blank=True, null=True)
    zone_in = models.CharField(max_length=45, blank=True, null=True)
    zone_out = models.CharField(max_length=45, blank=True, null=True)
    time_stay = models.CharField(max_length=45, blank=True, null=True)
    time_in = models.DateTimeField(blank=True, null=True)
    time_out = models.DateTimeField(blank=True, null=True)
    vehicle_type = models.CharField(max_length=45, blank=True, null=True)
    plate_num = models.CharField(max_length=45, blank=True, null=True)
    img_plate_filename = models.CharField(max_length=45, blank=True, null=True)
    img_parker_filename = models.CharField(max_length=45, blank=True, null=True)
    transacted = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'in_out_logs'


class Incomereport(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    trno = models.CharField(db_column='TRno', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cardcode = models.CharField(db_column='Cardcode', max_length=255, blank=True, null=True)  # Field name made lowercase.
    plate = models.CharField(db_column='Plate', max_length=255, blank=True, null=True)  # Field name made lowercase.
    operator = models.CharField(db_column='Operator', max_length=255, blank=True, null=True)  # Field name made lowercase.
    pc = models.CharField(db_column='PC', max_length=255, blank=True, null=True)  # Field name made lowercase.
    timein = models.DateTimeField(db_column='Timein', blank=True, null=True)  # Field name made lowercase.
    timeout = models.DateTimeField(db_column='TimeOut', blank=True, null=True)  # Field name made lowercase.
    busnessdate = models.DateField(db_column='BusnessDate', blank=True, null=True)  # Field name made lowercase.
    total = models.FloatField(db_column='Total')  # Field name made lowercase.
    vat = models.FloatField(db_column='Vat')  # Field name made lowercase.
    nonvat = models.FloatField(db_column='NonVat')  # Field name made lowercase.
    vatexemp = models.FloatField(db_column='VatExemp')  # Field name made lowercase.
    nad = models.FloatField(db_column='NAD')  # Field name made lowercase.
    sbv = models.FloatField(db_column='SBV')  # Field name made lowercase.
    type = models.CharField(db_column='TYPE', max_length=255, blank=True, null=True)  # Field name made lowercase.
    tender = models.FloatField(db_column='Tender')  # Field name made lowercase.
    change = models.FloatField(db_column='Change')  # Field name made lowercase.
    regular = models.FloatField(db_column='Regular')  # Field name made lowercase.
    overnight = models.FloatField(db_column='Overnight')  # Field name made lowercase.
    lostcard = models.FloatField(db_column='Lostcard')  # Field name made lowercase.
    payment = models.CharField(db_column='Payment', max_length=100, blank=True, null=True)  # Field name made lowercase.
    discounttype = models.CharField(db_column='DiscountType', max_length=255, blank=True, null=True)  # Field name made lowercase.
    discountamount = models.FloatField(db_column='DiscountAmount')  # Field name made lowercase.
    discountreference = models.CharField(db_column='DiscountReference', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cash = models.FloatField(db_column='Cash')  # Field name made lowercase.
    credit = models.FloatField(db_column='Credit')  # Field name made lowercase.
    creditcardid = models.CharField(db_column='CreditCardid', max_length=255, blank=True, null=True)  # Field name made lowercase.
    creditcardtype = models.CharField(db_column='CreditCardType', max_length=255, blank=True, null=True)  # Field name made lowercase.
    voucheramount = models.FloatField(db_column='VoucherAmount')  # Field name made lowercase.
    gpref = models.CharField(db_column='GPRef', max_length=255, blank=True, null=True)  # Field name made lowercase.
    gpdiscount = models.FloatField(db_column='GPDiscount')  # Field name made lowercase.
    gpoint = models.FloatField(db_column='GPoint')  # Field name made lowercase.
    complitype = models.CharField(db_column='CompliType', max_length=100, blank=True, null=True)  # Field name made lowercase.
    compli = models.FloatField(db_column='Compli')  # Field name made lowercase.
    compliref = models.CharField(db_column='CompliRef', max_length=100, blank=True, null=True)  # Field name made lowercase.
    prepaidtype = models.CharField(db_column='PrepaidType', max_length=100, blank=True, null=True)  # Field name made lowercase.
    prepaid = models.FloatField(db_column='Prepaid')  # Field name made lowercase.
    prepaidref = models.CharField(db_column='PrepaidRef', max_length=100, blank=True, null=True)  # Field name made lowercase.
    lostcarddetails = models.TextField(db_column='LostCardDetails', blank=True, null=True)  # Field name made lowercase.
    remarks = models.CharField(db_column='Remarks', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'incomereport'


class MIncomereport(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    trno = models.CharField(db_column='TRno', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cardcode = models.CharField(db_column='Cardcode', max_length=255, blank=True, null=True)  # Field name made lowercase.
    plate = models.CharField(db_column='Plate', max_length=255, blank=True, null=True)  # Field name made lowercase.
    operator = models.CharField(db_column='Operator', max_length=255, blank=True, null=True)  # Field name made lowercase.
    pc = models.CharField(db_column='PC', max_length=255, blank=True, null=True)  # Field name made lowercase.
    timein = models.DateTimeField(db_column='Timein', blank=True, null=True)  # Field name made lowercase.
    timeout = models.DateTimeField(db_column='TimeOut', blank=True, null=True)  # Field name made lowercase.
    busnessdate = models.DateField(db_column='BusnessDate', blank=True, null=True)  # Field name made lowercase.
    total = models.FloatField(db_column='Total', blank=True, null=True)  # Field name made lowercase.
    vat = models.FloatField(db_column='Vat', blank=True, null=True)  # Field name made lowercase.
    nonvat = models.FloatField(db_column='NonVat', blank=True, null=True)  # Field name made lowercase.
    vatexemp = models.FloatField(db_column='VatExemp', blank=True, null=True)  # Field name made lowercase.
    nad = models.FloatField(db_column='NAD', blank=True, null=True)  # Field name made lowercase.
    sbv = models.FloatField(db_column='SBV', blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(db_column='TYPE', max_length=255, blank=True, null=True)  # Field name made lowercase.
    tender = models.FloatField(db_column='Tender', blank=True, null=True)  # Field name made lowercase.
    change = models.FloatField(db_column='Change', blank=True, null=True)  # Field name made lowercase.
    regular = models.FloatField(db_column='Regular', blank=True, null=True)  # Field name made lowercase.
    overnight = models.FloatField(db_column='Overnight', blank=True, null=True)  # Field name made lowercase.
    lostcard = models.FloatField(db_column='Lostcard', blank=True, null=True)  # Field name made lowercase.
    payment = models.CharField(db_column='Payment', max_length=100, blank=True, null=True)  # Field name made lowercase.
    discounttype = models.CharField(db_column='DiscountType', max_length=255, blank=True, null=True)  # Field name made lowercase.
    discountamount = models.FloatField(db_column='DiscountAmount', blank=True, null=True)  # Field name made lowercase.
    discountreference = models.CharField(db_column='DiscountReference', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cash = models.FloatField(db_column='Cash', blank=True, null=True)  # Field name made lowercase.
    credit = models.FloatField(db_column='Credit', blank=True, null=True)  # Field name made lowercase.
    creditcardid = models.CharField(db_column='CreditCardid', max_length=255, blank=True, null=True)  # Field name made lowercase.
    creditcardtype = models.CharField(db_column='CreditCardType', max_length=255, blank=True, null=True)  # Field name made lowercase.
    voucheramount = models.FloatField(db_column='VoucherAmount', blank=True, null=True)  # Field name made lowercase.
    gpref = models.CharField(db_column='GPRef', max_length=255, blank=True, null=True)  # Field name made lowercase.
    gpdiscount = models.FloatField(db_column='GPDiscount', blank=True, null=True)  # Field name made lowercase.
    gpoint = models.FloatField(db_column='GPoint', blank=True, null=True)  # Field name made lowercase.
    complitype = models.CharField(db_column='CompliType', max_length=100, blank=True, null=True)  # Field name made lowercase.
    compli = models.FloatField(db_column='Compli', blank=True, null=True)  # Field name made lowercase.
    compliref = models.CharField(db_column='CompliRef', max_length=100, blank=True, null=True)  # Field name made lowercase.
    prepaidtype = models.CharField(db_column='PrepaidType', max_length=100, blank=True, null=True)  # Field name made lowercase.
    prepaid = models.FloatField(db_column='Prepaid', blank=True, null=True)  # Field name made lowercase.
    prepaidref = models.CharField(db_column='PrepaidRef', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'm_incomereport'


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
    pos_name = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'manual_transaction'


class Operators(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=255, blank=True, null=True)  # Field name made lowercase.
    username = models.CharField(db_column='Username', max_length=255, blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=255, blank=True, null=True)  # Field name made lowercase.
    nickname = models.CharField(db_column='NickName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    status = models.IntegerField(db_column='Status', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'operators'


class PosReport(models.Model):
    id = models.BigAutoField(primary_key=True)
    tr = models.BigIntegerField(db_column='TR', blank=True, null=True)  # Field name made lowercase.
    dt = models.DateField(db_column='DT', blank=True, null=True)  # Field name made lowercase.
    or_from = models.CharField(db_column='OR_From', max_length=100, blank=True, null=True)  # Field name made lowercase.
    or_to = models.CharField(db_column='OR_To', max_length=100, blank=True, null=True)  # Field name made lowercase.
    vat = models.FloatField(db_column='VAT', blank=True, null=True)  # Field name made lowercase.
    vat_sale = models.FloatField(db_column='VAT_Sale', blank=True, null=True)  # Field name made lowercase.
    total = models.FloatField(db_column='Total', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'pos_report'


class Security(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=60, blank=True, null=True)  # Field name made lowercase.
    username = models.CharField(db_column='Username', max_length=60, blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=60, blank=True, null=True)  # Field name made lowercase.
    r_name = models.CharField(db_column='R_name', max_length=100, blank=True, null=True)  # Field name made lowercase.
    status = models.IntegerField(db_column='Status', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'security'


class Taxdb(models.Model):
    tax = models.FloatField(db_column='Tax', blank=True, null=True)  # Field name made lowercase.
    taxlp = models.FloatField(db_column='TaxLp', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'taxdb'


class TblDrsset(models.Model):
    drs_date = models.DateField(db_column='DRS_Date', blank=True, null=True)  # Field name made lowercase.
    drs_shift = models.BigIntegerField(db_column='DRS_Shift', blank=True, null=True)  # Field name made lowercase.
    drs_cutoff = models.TimeField(db_column='DRS_CutOff', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_drsset'


class TblMoneylogs(models.Model):
    id = models.BigAutoField(primary_key=True)
    ornum = models.CharField(db_column='ORnum', max_length=255, blank=True, null=True)  # Field name made lowercase.
    moneytype = models.CharField(db_column='MoneyType', max_length=100, blank=True, null=True)  # Field name made lowercase.
    amount = models.FloatField(db_column='Amount', blank=True, null=True)  # Field name made lowercase.
    mcount = models.BigIntegerField(db_column='MCount', blank=True, null=True)  # Field name made lowercase.
    busnessdate = models.DateField(db_column='BusnessDate', blank=True, null=True)  # Field name made lowercase.
    timeout = models.DateTimeField(db_column='TimeOut', blank=True, null=True)  # Field name made lowercase.
    station = models.CharField(db_column='Station', max_length=100, blank=True, null=True)  # Field name made lowercase.
    mode = models.CharField(db_column='Mode', max_length=100, blank=True, null=True)  # Field name made lowercase.
    totalsale = models.FloatField(db_column='TotalSale', blank=True, null=True)  # Field name made lowercase.
    timein = models.DateTimeField(db_column='Timein', blank=True, null=True)  # Field name made lowercase.
    cardcode = models.CharField(db_column='CardCode', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_moneylogs'


class Tblblacklist(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    plate = models.CharField(db_column='Plate', max_length=100, blank=True, null=True)  # Field name made lowercase.
    adminname = models.CharField(db_column='AdminName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    dt = models.DateTimeField(db_column='DT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tblblacklist'


class Tblbusnessdate(models.Model):
    busnessdate = models.DateField(db_column='BusnessDate', primary_key=True)  # Field name made lowercase.
    adminname = models.CharField(db_column='AdminName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    dtlogs = models.DateTimeField(db_column='DTlogs', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tblbusnessdate'


class Tblcardschedule(models.Model):
    id = models.BigAutoField(primary_key=True)
    deptname = models.CharField(db_column='DeptName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    dayname = models.CharField(db_column='DayName', max_length=10, blank=True, null=True)  # Field name made lowercase.
    timefrom = models.TimeField(db_column='TimeFrom', blank=True, null=True)  # Field name made lowercase.
    timeto = models.TimeField(db_column='TimeTo', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tblcardschedule'


class Tblcashiersales(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    cashiername = models.CharField(db_column='CashierName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    location = models.CharField(db_column='Location', max_length=255, blank=True, null=True)  # Field name made lowercase.
    terminal = models.CharField(db_column='Terminal', max_length=255, blank=True, null=True)  # Field name made lowercase.
    time_login = models.DateTimeField(db_column='Time_Login', blank=True, null=True)  # Field name made lowercase.
    time_logout = models.DateTimeField(db_column='Time_Logout', blank=True, null=True)  # Field name made lowercase.
    saledate = models.DateField(db_column='SaleDate', blank=True, null=True)  # Field name made lowercase.
    cashfund = models.FloatField(db_column='CashFund', blank=True, null=True)  # Field name made lowercase.
    receiptcount = models.BigIntegerField(db_column='ReceiptCount', blank=True, null=True)  # Field name made lowercase.
    totalamount = models.FloatField(db_column='TotalAmount', blank=True, null=True)  # Field name made lowercase.
    cashindrawer = models.FloatField(db_column='CashInDrawer', blank=True, null=True)  # Field name made lowercase.
    partialcashout = models.FloatField(db_column='PartialCashOut', blank=True, null=True)  # Field name made lowercase.
    openbarrier = models.BigIntegerField(db_column='OpenBarrier', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tblcashiersales'


class Tblclearcard(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    cardcode = models.CharField(db_column='CardCode', max_length=100, blank=True, null=True)  # Field name made lowercase.
    vehicle = models.CharField(db_column='Vehicle', max_length=100, blank=True, null=True)  # Field name made lowercase.
    plate = models.CharField(db_column='Plate', max_length=100, blank=True, null=True)  # Field name made lowercase.
    timein = models.DateTimeField(db_column='Timein', blank=True, null=True)  # Field name made lowercase.
    operator = models.CharField(db_column='Operator', max_length=100, blank=True, null=True)  # Field name made lowercase.
    pc = models.CharField(db_column='PC', max_length=100, blank=True, null=True)  # Field name made lowercase.
    pic = models.TextField(db_column='PIC', blank=True, null=True)  # Field name made lowercase.
    pic2 = models.TextField(db_column='PIC2', blank=True, null=True)  # Field name made lowercase.
    lane = models.CharField(db_column='Lane', max_length=100, blank=True, null=True)  # Field name made lowercase.
    useraccount = models.CharField(db_column='UserAccount', max_length=100, blank=True, null=True)  # Field name made lowercase.
    reason = models.CharField(db_column='Reason', max_length=255, blank=True, null=True)  # Field name made lowercase.
    datecleared = models.DateTimeField(db_column='DateCleared', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tblclearcard'


class Tblcompli(models.Model):
    id = models.BigAutoField(primary_key=True)
    complitype = models.CharField(db_column='CompliType', max_length=100, blank=True, null=True)  # Field name made lowercase.
    compliamount = models.FloatField(db_column='CompliAmount', blank=True, null=True)  # Field name made lowercase.
    compliall = models.IntegerField(db_column='CompliAll', blank=True, null=True)  # Field name made lowercase.
    complivat = models.IntegerField(db_column='CompliVat', blank=True, null=True)  # Field name made lowercase.
    valetfee = models.FloatField(db_column='ValetFee', blank=True, null=True)  # Field name made lowercase.
    status = models.IntegerField(db_column='Status', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tblcompli'


class Tblcreditcard(models.Model):
    id = models.BigAutoField(primary_key=True)
    creditcardtype = models.CharField(db_column='CreditCardType', max_length=255, blank=True, null=True)  # Field name made lowercase.
    status = models.IntegerField(db_column='Status', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tblcreditcard'


class Tbldays(models.Model):
    id = models.BigAutoField(primary_key=True)
    deptname = models.CharField(db_column='DeptName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    mon = models.IntegerField(db_column='Mon', blank=True, null=True)  # Field name made lowercase.
    tue = models.IntegerField(db_column='Tue', blank=True, null=True)  # Field name made lowercase.
    wed = models.IntegerField(db_column='Wed', blank=True, null=True)  # Field name made lowercase.
    thu = models.IntegerField(db_column='Thu', blank=True, null=True)  # Field name made lowercase.
    fri = models.IntegerField(db_column='Fri', blank=True, null=True)  # Field name made lowercase.
    sat = models.IntegerField(db_column='Sat', blank=True, null=True)  # Field name made lowercase.
    sun = models.IntegerField(db_column='Sun', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbldays'


class Tbldepartment(models.Model):
    id = models.BigAutoField(primary_key=True)
    departmentname = models.CharField(db_column='DepartmentName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    chargeamt = models.FloatField(db_column='ChargeAMT', blank=True, null=True)  # Field name made lowercase.
    earlyamt = models.FloatField(db_column='EarlyAMT', blank=True, null=True)  # Field name made lowercase.
    notamt = models.FloatField(db_column='NotAMT', blank=True, null=True)  # Field name made lowercase.
    graceperiod = models.BigIntegerField(db_column='GracePeriod', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbldepartment'


class Tbldiscount(models.Model):
    id = models.BigAutoField(primary_key=True)
    discounttype = models.CharField(db_column='DiscountType', max_length=255, blank=True, null=True)  # Field name made lowercase.
    vatexempt = models.IntegerField(db_column='VatExempt', blank=True, null=True)  # Field name made lowercase.
    percentage = models.FloatField(db_column='Percentage', blank=True, null=True)  # Field name made lowercase.
    isfree = models.IntegerField(db_column='isFree', blank=True, null=True)  # Field name made lowercase.
    status = models.IntegerField(db_column='Status', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbldiscount'


class Tbldiscountfix(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    discounttype = models.CharField(db_column='DiscountType', max_length=255, blank=True, null=True)  # Field name made lowercase.
    vatexempt = models.IntegerField(db_column='VatExempt', blank=True, null=True)  # Field name made lowercase.
    percentage = models.FloatField(db_column='Percentage', blank=True, null=True)  # Field name made lowercase.
    isfree = models.IntegerField(db_column='isFree', blank=True, null=True)  # Field name made lowercase.
    status = models.IntegerField(db_column='Status', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbldiscountfix'


class Tbldrscancel(models.Model):
    canceltype = models.CharField(db_column='CancelType', max_length=100, blank=True, null=True)  # Field name made lowercase.
    busnessdate = models.DateField(db_column='BusnessDate', blank=True, null=True)  # Field name made lowercase.
    dt = models.DateTimeField(db_column='DT', blank=True, null=True)  # Field name made lowercase.
    operator = models.CharField(db_column='Operator', max_length=100, blank=True, null=True)  # Field name made lowercase.
    admin = models.CharField(db_column='Admin', max_length=100, blank=True, null=True)  # Field name made lowercase.
    docnum = models.CharField(db_column='Docnum', max_length=255, blank=True, null=True)  # Field name made lowercase.
    station = models.CharField(db_column='Station', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ornum = models.CharField(db_column='ORnum', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cid = models.CharField(db_column='Cid', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbldrscancel'


class Tblemp(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    acno = models.CharField(db_column='ACno', max_length=24, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=80, blank=True, null=True)  # Field name made lowercase.
    gender = models.CharField(db_column='Gender', max_length=20, blank=True, null=True)  # Field name made lowercase.
    plate = models.CharField(db_column='Plate', max_length=50, blank=True, null=True)  # Field name made lowercase.
    vehicle = models.CharField(db_column='Vehicle', max_length=20, blank=True, null=True)  # Field name made lowercase.
    contactno = models.CharField(db_column='ContactNo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=100, blank=True, null=True)  # Field name made lowercase.
    dateenrolled = models.DateField(db_column='DateEnrolled', blank=True, null=True)  # Field name made lowercase.
    dateexpired = models.DateField(db_column='DateExpired', blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(db_column='Type', max_length=20, blank=True, null=True)  # Field name made lowercase.
    accessstatus = models.IntegerField(db_column='AccessStatus', blank=True, null=True)  # Field name made lowercase.
    picpath = models.TextField(db_column='PicPath', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tblemp'


class Tblemplogs(models.Model):
    id = models.BigAutoField(primary_key=True)
    empcardcode = models.CharField(db_column='EmpCardCode', max_length=200, blank=True, null=True)  # Field name made lowercase.
    logtime = models.DateTimeField(db_column='LogTime', blank=True, null=True)  # Field name made lowercase.
    location = models.CharField(db_column='Location', max_length=200, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tblemplogs'


class Tblemployee(models.Model):
    id = models.BigAutoField(primary_key=True)
    empname = models.CharField(db_column='EmpName', max_length=200, blank=True, null=True)  # Field name made lowercase.
    empcardcode = models.CharField(db_column='EmpCardCode', max_length=200, blank=True, null=True)  # Field name made lowercase.
    status = models.IntegerField(db_column='Status', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tblemployee'


class Tblemployeerecords(models.Model):
    emplid = models.CharField(db_column='Emplid', primary_key=True, max_length=100)  # Field name made lowercase.
    employeename = models.CharField(db_column='EmployeeName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    empf = models.CharField(db_column='EmpF', max_length=100, blank=True, null=True)  # Field name made lowercase.
    department = models.CharField(db_column='Department', max_length=100, blank=True, null=True)  # Field name made lowercase.
    employeec = models.CharField(db_column='EmployeeC', max_length=100, blank=True, null=True)  # Field name made lowercase.
    dep = models.CharField(db_column='Dep', max_length=100, blank=True, null=True)  # Field name made lowercase.
    employeeid = models.CharField(db_column='EmployeeID', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tblemployeerecords'


class Tblflatratedays(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    rulename = models.CharField(db_column='RuleName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    monday = models.IntegerField(db_column='Monday', blank=True, null=True)  # Field name made lowercase.
    tuesday = models.IntegerField(db_column='Tuesday', blank=True, null=True)  # Field name made lowercase.
    wednesday = models.IntegerField(db_column='Wednesday', blank=True, null=True)  # Field name made lowercase.
    thursday = models.IntegerField(db_column='Thursday', blank=True, null=True)  # Field name made lowercase.
    friday = models.IntegerField(db_column='Friday', blank=True, null=True)  # Field name made lowercase.
    saturday = models.IntegerField(db_column='Saturday', blank=True, null=True)  # Field name made lowercase.
    sunday = models.IntegerField(db_column='Sunday', blank=True, null=True)  # Field name made lowercase.
    holiday = models.CharField(db_column='Holiday', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tblflatratedays'


class Tblholiday(models.Model):
    id = models.BigAutoField(primary_key=True)
    holidaydate = models.DateField(db_column='HolidayDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tblholiday'


class Tblid(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    ornumber = models.CharField(db_column='ORNumber', max_length=255, blank=True, null=True)  # Field name made lowercase.
    idnumber = models.CharField(db_column='IDNumber', max_length=255, blank=True, null=True)  # Field name made lowercase.
    idname = models.CharField(db_column='IDName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    idaddress = models.TextField(db_column='IDAddress', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tblid'


class Tbllengthstay(models.Model):
    id = models.BigAutoField(primary_key=True)
    lengthstay = models.CharField(db_column='LengthStay', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cnt = models.BigIntegerField(db_column='CNT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbllengthstay'


class Tbllogsrec(models.Model):
    idlog = models.BigAutoField(db_column='Idlog', primary_key=True)  # Field name made lowercase.
    cardcode = models.CharField(db_column='CardCode', max_length=30, blank=True, null=True)  # Field name made lowercase.
    plateno = models.CharField(db_column='PlateNo', max_length=255, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100, blank=True, null=True)  # Field name made lowercase.
    department = models.CharField(db_column='Department', max_length=255, blank=True, null=True)  # Field name made lowercase.
    timein = models.DateTimeField(db_column='TimeIn', blank=True, null=True)  # Field name made lowercase.
    timeout = models.DateTimeField(db_column='TimeOut', blank=True, null=True)  # Field name made lowercase.
    picent = models.TextField(db_column='PicEnt', blank=True, null=True)  # Field name made lowercase.
    picext = models.TextField(db_column='PicExt', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=20, blank=True, null=True)  # Field name made lowercase.
    earlytotal = models.FloatField(db_column='EarlyTotal', blank=True, null=True)  # Field name made lowercase.
    succeedingtotal = models.FloatField(db_column='SucceedingTotal', blank=True, null=True)  # Field name made lowercase.
    wrongparktotal = models.FloatField(db_column='WrongParkTotal', blank=True, null=True)  # Field name made lowercase.
    totalamount = models.FloatField(db_column='TotalAmount', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbllogsrec'


class Tblnotyet(models.Model):
    id = models.BigAutoField(primary_key=True)
    cardcode = models.CharField(db_column='CardCode', max_length=100, blank=True, null=True)  # Field name made lowercase.
    location = models.CharField(db_column='Location', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tblnotyet'


class Tbloccupancy(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    busnessdate = models.DateField(db_column='BusnessDate', blank=True, null=True)  # Field name made lowercase.
    timeframe = models.CharField(db_column='TimeFrame', max_length=255, blank=True, null=True)  # Field name made lowercase.
    totalin = models.BigIntegerField(db_column='TotalIN', blank=True, null=True)  # Field name made lowercase.
    totalout = models.BigIntegerField(db_column='TotalOUT', blank=True, null=True)  # Field name made lowercase.
    occupancy = models.BigIntegerField(db_column='Occupancy', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbloccupancy'


class Tblov(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    chargingrule = models.CharField(db_column='ChargingRule', max_length=100, blank=True, null=True)  # Field name made lowercase.
    flatratedays = models.IntegerField(db_column='FlatrateDays', blank=True, null=True)  # Field name made lowercase.
    regulardays = models.IntegerField(db_column='RegularDays', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tblov'


class Tblpartial(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    adminname = models.CharField(db_column='AdminName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    dt = models.DateTimeField(db_column='DT', blank=True, null=True)  # Field name made lowercase.
    saledate = models.DateField(db_column='SaleDate', blank=True, null=True)  # Field name made lowercase.
    amount = models.FloatField(db_column='Amount', blank=True, null=True)  # Field name made lowercase.
    station = models.CharField(db_column='Station', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cashier = models.CharField(db_column='Cashier', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tblpartial'


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
        managed = False
        db_table = 'tblpermit'


class Tblpmsmsg(models.Model):
    entryzone = models.CharField(db_column='EntryZone', primary_key=True, max_length=30)  # Field name made lowercase.
    msg = models.CharField(db_column='Msg', max_length=30, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tblpmsmsg'


class Tblprepaid(models.Model):
    id = models.BigAutoField(primary_key=True)
    prepaidtype = models.CharField(db_column='PrepaidType', max_length=100, blank=True, null=True)  # Field name made lowercase.
    prepaidamount = models.FloatField(db_column='PrepaidAmount', blank=True, null=True)  # Field name made lowercase.
    prepaidall = models.IntegerField(db_column='PrepaidAll', blank=True, null=True)  # Field name made lowercase.
    prepaidvat = models.IntegerField(db_column='PrepaidVAT', blank=True, null=True)  # Field name made lowercase.
    status = models.IntegerField(db_column='Status', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tblprepaid'


class Tbltemp(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    trno = models.CharField(db_column='TRno', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cardcode = models.CharField(db_column='Cardcode', max_length=255, blank=True, null=True)  # Field name made lowercase.
    plate = models.CharField(db_column='Plate', max_length=255, blank=True, null=True)  # Field name made lowercase.
    operator = models.CharField(db_column='Operator', max_length=255, blank=True, null=True)  # Field name made lowercase.
    pc = models.CharField(db_column='PC', max_length=255, blank=True, null=True)  # Field name made lowercase.
    timein = models.DateTimeField(db_column='Timein', blank=True, null=True)  # Field name made lowercase.
    timeout = models.DateTimeField(db_column='TimeOut', blank=True, null=True)  # Field name made lowercase.
    busnessdate = models.DateField(db_column='BusnessDate', blank=True, null=True)  # Field name made lowercase.
    total = models.FloatField(db_column='Total', blank=True, null=True)  # Field name made lowercase.
    vat = models.FloatField(db_column='Vat', blank=True, null=True)  # Field name made lowercase.
    nonvat = models.FloatField(db_column='NonVat', blank=True, null=True)  # Field name made lowercase.
    vatexemp = models.FloatField(db_column='VatExemp', blank=True, null=True)  # Field name made lowercase.
    nad = models.FloatField(db_column='NAD')  # Field name made lowercase.
    sbv = models.FloatField(db_column='SBV')  # Field name made lowercase.
    type = models.CharField(db_column='TYPE', max_length=255, blank=True, null=True)  # Field name made lowercase.
    tender = models.FloatField(db_column='Tender', blank=True, null=True)  # Field name made lowercase.
    change = models.FloatField(db_column='Change', blank=True, null=True)  # Field name made lowercase.
    regular = models.FloatField(db_column='Regular', blank=True, null=True)  # Field name made lowercase.
    overnight = models.FloatField(db_column='Overnight', blank=True, null=True)  # Field name made lowercase.
    lostcard = models.FloatField(db_column='Lostcard', blank=True, null=True)  # Field name made lowercase.
    payment = models.CharField(db_column='Payment', max_length=100, blank=True, null=True)  # Field name made lowercase.
    discounttype = models.CharField(db_column='DiscountType', max_length=255, blank=True, null=True)  # Field name made lowercase.
    discountamount = models.FloatField(db_column='DiscountAmount', blank=True, null=True)  # Field name made lowercase.
    discountreference = models.CharField(db_column='DiscountReference', max_length=255)  # Field name made lowercase.
    cash = models.FloatField(db_column='Cash')  # Field name made lowercase.
    credit = models.FloatField(db_column='Credit', blank=True, null=True)  # Field name made lowercase.
    creditcardid = models.CharField(db_column='CreditCardid', max_length=255)  # Field name made lowercase.
    creditcardtype = models.CharField(db_column='CreditCardType', max_length=255)  # Field name made lowercase.
    voucheramount = models.FloatField(db_column='VoucherAmount')  # Field name made lowercase.
    gpref = models.CharField(db_column='GPRef', max_length=255)  # Field name made lowercase.
    gpdiscount = models.FloatField(db_column='GPDiscount')  # Field name made lowercase.
    gpoint = models.FloatField(db_column='GPoint')  # Field name made lowercase.
    complitype = models.CharField(db_column='CompliType', max_length=100)  # Field name made lowercase.
    compli = models.FloatField(db_column='Compli', blank=True, null=True)  # Field name made lowercase.
    compliref = models.CharField(db_column='CompliRef', max_length=100)  # Field name made lowercase.
    prepaidtype = models.CharField(db_column='PrepaidType', max_length=100)  # Field name made lowercase.
    prepaid = models.FloatField(db_column='Prepaid', blank=True, null=True)  # Field name made lowercase.
    prepaidref = models.CharField(db_column='PrepaidRef', max_length=100, blank=True, null=True)  # Field name made lowercase.
    lostcarddetails = models.TextField(db_column='LostCardDetails', blank=True, null=True)  # Field name made lowercase.
    remarks = models.CharField(db_column='Remarks', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbltemp'


class Tbltimeframe(models.Model):
    id = models.BigAutoField(primary_key=True)
    chname = models.CharField(db_column='CHname', max_length=255, blank=True, null=True)  # Field name made lowercase.
    starttime = models.TimeField(db_column='StartTime', blank=True, null=True)  # Field name made lowercase.
    endtime = models.TimeField(db_column='EndTime', blank=True, null=True)  # Field name made lowercase.
    succeed = models.FloatField(db_column='Succeed', blank=True, null=True)  # Field name made lowercase.
    fixrate = models.FloatField(db_column='FixRate', blank=True, null=True)  # Field name made lowercase.
    status = models.IntegerField(db_column='Status', blank=True, null=True)  # Field name made lowercase.
    overnight = models.FloatField(db_column='Overnight', blank=True, null=True)  # Field name made lowercase.
    lostcard = models.FloatField(db_column='LostCard', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbltimeframe'


class Tbltimein(models.Model):
    idlog = models.BigAutoField(db_column='IDLog', primary_key=True)  # Field name made lowercase.
    cardcode = models.CharField(db_column='CardCode', max_length=30, blank=True, null=True)  # Field name made lowercase.
    plateno = models.CharField(db_column='PlateNo', max_length=255, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100, blank=True, null=True)  # Field name made lowercase.
    department = models.CharField(db_column='Department', max_length=255, blank=True, null=True)  # Field name made lowercase.
    timein = models.DateTimeField(db_column='TimeIn', blank=True, null=True)  # Field name made lowercase.
    picpath = models.TextField(db_column='PicPath', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=20, blank=True, null=True)  # Field name made lowercase.
    upperentrance = models.IntegerField(db_column='UpperEntrance', blank=True, null=True)  # Field name made lowercase.
    lowerentrance = models.IntegerField(db_column='LowerEntrance', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbltimein'


class Tbltimein1(models.Model):
    idlog = models.BigAutoField(db_column='IdLog', primary_key=True)  # Field name made lowercase.
    idnumber = models.CharField(db_column='Idnumber', max_length=50, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=50, blank=True, null=True)  # Field name made lowercase.
    timein = models.DateTimeField(db_column='TimeIn', blank=True, null=True)  # Field name made lowercase.
    entpic1 = models.TextField(db_column='EntPic1', blank=True, null=True)  # Field name made lowercase.
    foldername = models.CharField(db_column='FolderName', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbltimein1'


class Tbltimein2(models.Model):
    idlog = models.BigAutoField(db_column='IdLog', primary_key=True)  # Field name made lowercase.
    idnumber = models.CharField(db_column='Idnumber', max_length=30, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=50, blank=True, null=True)  # Field name made lowercase.
    timein1 = models.DateTimeField(db_column='TimeIn1', blank=True, null=True)  # Field name made lowercase.
    timein2 = models.DateTimeField(db_column='TimeIn2', blank=True, null=True)  # Field name made lowercase.
    timediff = models.IntegerField(db_column='TimeDiff', blank=True, null=True)  # Field name made lowercase.
    graceperiod = models.IntegerField(db_column='GracePeriod', blank=True, null=True)  # Field name made lowercase.
    entpic1 = models.TextField(db_column='EntPic1', blank=True, null=True)  # Field name made lowercase.
    entpic2 = models.TextField(db_column='EntPic2', blank=True, null=True)  # Field name made lowercase.
    foldername = models.CharField(db_column='FolderName', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbltimein2'


class Tbltimeout(models.Model):
    idlog = models.BigAutoField(db_column='IdLog', primary_key=True)  # Field name made lowercase.
    cardcode = models.CharField(db_column='CardCode', max_length=30, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100, blank=True, null=True)  # Field name made lowercase.
    department = models.CharField(db_column='Department', max_length=255, blank=True, null=True)  # Field name made lowercase.
    plateno = models.CharField(db_column='PlateNo', max_length=255, blank=True, null=True)  # Field name made lowercase.
    timeout = models.DateTimeField(db_column='TimeOut', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=20, blank=True, null=True)  # Field name made lowercase.
    picpath = models.TextField(db_column='PicPath', blank=True, null=True)  # Field name made lowercase.
    lowerexit = models.IntegerField(db_column='LowerExit', blank=True, null=True)  # Field name made lowercase.
    upperexit = models.IntegerField(db_column='UpperExit', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbltimeout'


class Tbltimeout1(models.Model):
    idlog = models.BigAutoField(db_column='IdLog', primary_key=True)  # Field name made lowercase.
    idnumber = models.CharField(db_column='IDnumber', max_length=30, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=50, blank=True, null=True)  # Field name made lowercase.
    timein1 = models.DateTimeField(db_column='Timein1', blank=True, null=True)  # Field name made lowercase.
    timein2 = models.DateTimeField(db_column='Timein2', blank=True, null=True)  # Field name made lowercase.
    timediff = models.IntegerField(db_column='TimeDiff', blank=True, null=True)  # Field name made lowercase.
    graceperiod = models.IntegerField(db_column='GracePeriod', blank=True, null=True)  # Field name made lowercase.
    timeout1 = models.DateTimeField(db_column='TimeOut1', blank=True, null=True)  # Field name made lowercase.
    entpic1 = models.TextField(db_column='EntPic1', blank=True, null=True)  # Field name made lowercase.
    entpic2 = models.TextField(db_column='EntPic2', blank=True, null=True)  # Field name made lowercase.
    extpic1 = models.TextField(db_column='ExtPic1', blank=True, null=True)  # Field name made lowercase.
    foldername = models.CharField(db_column='FolderName', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbltimeout1'


class Tbltimeout2(models.Model):
    idlog = models.BigAutoField(db_column='IdLog', primary_key=True)  # Field name made lowercase.
    idnumber = models.CharField(db_column='IDnumber', max_length=30, blank=True, null=True)  # Field name made lowercase.
    timein1 = models.DateTimeField(db_column='Timein1', blank=True, null=True)  # Field name made lowercase.
    timein2 = models.DateTimeField(db_column='Timein2', blank=True, null=True)  # Field name made lowercase.
    timediff = models.IntegerField(db_column='TimeDiff', blank=True, null=True)  # Field name made lowercase.
    graceperiod = models.IntegerField(db_column='GracePeriod', blank=True, null=True)  # Field name made lowercase.
    timeout1 = models.DateTimeField(db_column='Timeout1', blank=True, null=True)  # Field name made lowercase.
    timeout2 = models.DateTimeField(db_column='Timeout2', blank=True, null=True)  # Field name made lowercase.
    exttimediff = models.IntegerField(db_column='ExtTimeDiff', blank=True, null=True)  # Field name made lowercase.
    extgraceperiod = models.IntegerField(db_column='ExtGraceperiod', blank=True, null=True)  # Field name made lowercase.
    entpic1 = models.TextField(db_column='EntPic1', blank=True, null=True)  # Field name made lowercase.
    entpic2 = models.TextField(db_column='EntPic2', blank=True, null=True)  # Field name made lowercase.
    extpic1 = models.TextField(db_column='ExtPic1', blank=True, null=True)  # Field name made lowercase.
    extpic2 = models.TextField(db_column='ExtPic2', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbltimeout2'


class Tbluseracc(models.Model):
    username = models.CharField(db_column='UserName', primary_key=True, max_length=12)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=12, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=40, blank=True, null=True)  # Field name made lowercase.
    designation = models.CharField(db_column='Designation', max_length=15, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbluseracc'


class Tblvipcardnumber(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    plate = models.CharField(db_column='Plate', max_length=100, blank=True, null=True)  # Field name made lowercase.
    vipcard = models.CharField(db_column='VIPCard', max_length=255, blank=True, null=True)  # Field name made lowercase.
    timeout = models.DateTimeField(db_column='Timeout', blank=True, null=True)  # Field name made lowercase.
    bd = models.DateField(db_column='BD', blank=True, null=True)  # Field name made lowercase.
    location = models.CharField(db_column='Location', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cashier = models.CharField(db_column='Cashier', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tblvipcardnumber'


class Tblviprecords(models.Model):
    id = models.BigAutoField(primary_key=True)
    cardcode = models.CharField(db_column='CardCode', max_length=100, blank=True, null=True)  # Field name made lowercase.
    timein = models.DateTimeField(db_column='Timein', blank=True, null=True)  # Field name made lowercase.
    timeout = models.DateTimeField(db_column='Timeout', blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100, blank=True, null=True)  # Field name made lowercase.
    picfront1 = models.TextField(db_column='PICFront1', blank=True, null=True)  # Field name made lowercase.
    picface1 = models.TextField(db_column='PICFace1', blank=True, null=True)  # Field name made lowercase.
    picfront2 = models.TextField(db_column='PICFront2', blank=True, null=True)  # Field name made lowercase.
    picface2 = models.TextField(db_column='PICFace2', blank=True, null=True)  # Field name made lowercase.
    area = models.CharField(db_column='Area', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tblviprecords'


class Tblviptimein(models.Model):
    cardcode = models.CharField(db_column='CardCode', max_length=100, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100, blank=True, null=True)  # Field name made lowercase.
    timein = models.DateTimeField(db_column='TimeIn', blank=True, null=True)  # Field name made lowercase.
    lane = models.CharField(db_column='Lane', max_length=100, blank=True, null=True)  # Field name made lowercase.
    picface = models.TextField(db_column='PicFace', blank=True, null=True)  # Field name made lowercase.
    picfront = models.TextField(db_column='PicFront', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tblviptimein'


class Tblvoucherincome(models.Model):
    ids = models.BigAutoField(primary_key=True)
    trno = models.CharField(db_column='TRno', max_length=255)  # Field name made lowercase.
    busnessdate = models.DateField(db_column='BusnessDate', blank=True, null=True)  # Field name made lowercase.
    vouchertype = models.CharField(db_column='VoucherType', max_length=255, blank=True, null=True)  # Field name made lowercase.
    voucherref = models.CharField(db_column='VoucherRef', max_length=255, blank=True, null=True)  # Field name made lowercase.
    voucheramount = models.FloatField(db_column='VoucherAmount', blank=True, null=True)  # Field name made lowercase.
    operator = models.CharField(db_column='Operator', max_length=255, blank=True, null=True)  # Field name made lowercase.
    timeout = models.DateTimeField(blank=True, null=True)
    pos = models.CharField(db_column='POS', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tblvoucherincome'
        unique_together = (('ids', 'trno'),)


class Tblvouchers(models.Model):
    id = models.BigAutoField(primary_key=True)
    vouchertype = models.CharField(db_column='VoucherType', max_length=255, blank=True, null=True)  # Field name made lowercase.
    amountvalue = models.FloatField(db_column='AmountValue', blank=True, null=True)  # Field name made lowercase.
    status = models.IntegerField(db_column='Status', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tblvouchers'


class Tblz(models.Model):
    id = models.BigAutoField(primary_key=True)
    zcount = models.BigIntegerField(blank=True, null=True)
    lasttime = models.DateTimeField(blank=True, null=True)
    adminname = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tblz'


class Terminal(models.Model):
    serial_num = models.CharField(max_length=45, blank=True, null=True)
    machine_id_num = models.CharField(max_length=45, blank=True, null=True)
    bir_ptu_num = models.CharField(max_length=45, blank=True, null=True)
    bir_ptu_issued = models.DateField(blank=True, null=True)
    bir_ptu_until = models.DateField(blank=True, null=True)
    mac_address = models.CharField(max_length=45, blank=True, null=True)
    ip_address = models.CharField(max_length=45, blank=True, null=True)
    header = models.CharField(max_length=45, blank=True, null=True)
    cash_fund = models.IntegerField(blank=True, null=True)
    entry_zone = models.CharField(max_length=45, blank=True, null=True)
    zone_enable = models.IntegerField(blank=True, null=True)
    parking_slot = models.IntegerField(blank=True, null=True)
    pos_number = models.IntegerField(blank=True, null=True)
    server_ip = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'terminal'


class TfSchedule(models.Model):
    id = models.BigAutoField(primary_key=True)
    promo_name = models.CharField(max_length=45, blank=True, null=True)
    tf_name = models.CharField(max_length=45, blank=True, null=True)
    succeding_rules = models.CharField(max_length=45)
    entry_from = models.TimeField(blank=True, null=True)
    entry_to = models.TimeField(blank=True, null=True)
    exit_from = models.TimeField(blank=True, null=True)
    exit_to = models.TimeField(blank=True, null=True)
    monday = models.IntegerField(blank=True, null=True)
    tuesday = models.IntegerField(blank=True, null=True)
    wednesday = models.IntegerField(blank=True, null=True)
    thursday = models.IntegerField(blank=True, null=True)
    friday = models.IntegerField(blank=True, null=True)
    saturday = models.IntegerField(blank=True, null=True)
    sunday = models.IntegerField(blank=True, null=True)
    holiday = models.IntegerField(blank=True, null=True)
    tf_type = models.IntegerField(blank=True, null=True)
    promo_amount = models.FloatField(db_column='Promo_Amount', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tf_schedule'


class TimeFrame(models.Model):
    id = models.BigAutoField(primary_key=True)
    charging_rule = models.CharField(max_length=45, blank=True, null=True)
    entry_from = models.TimeField(blank=True, null=True)
    entry_to = models.TimeField(blank=True, null=True)
    exit_from = models.TimeField(blank=True, null=True)
    exit_to = models.TimeField(blank=True, null=True)
    base_amount = models.FloatField(blank=True, null=True)
    fix_rate = models.FloatField(blank=True, null=True)
    succ_amount = models.FloatField(blank=True, null=True)
    overnight = models.FloatField(blank=True, null=True)
    lostcard = models.FloatField(blank=True, null=True)
    isbetween = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'time_frame'


class Timeindb(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    cardcode = models.CharField(db_column='CardCode', max_length=100, blank=True, null=True)  # Field name made lowercase.
    vehicle = models.CharField(db_column='Vehicle', max_length=100, blank=True, null=True)  # Field name made lowercase.
    plate = models.CharField(db_column='Plate', max_length=100, blank=True, null=True)  # Field name made lowercase.
    timein = models.DateTimeField(db_column='Timein', blank=True, null=True)  # Field name made lowercase.
    operator = models.CharField(db_column='Operator', max_length=100, blank=True, null=True)  # Field name made lowercase.
    pc = models.CharField(db_column='PC', max_length=100, blank=True, null=True)  # Field name made lowercase.
    pic = models.TextField(db_column='PIC', blank=True, null=True)  # Field name made lowercase.
    pic2 = models.TextField(db_column='PIC2', blank=True, null=True)  # Field name made lowercase.
    lane = models.CharField(db_column='Lane', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'timeindb'


class Timeoutdb(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    cardcode = models.CharField(db_column='CardCode', max_length=100, blank=True, null=True)  # Field name made lowercase.
    vehicle = models.CharField(db_column='Vehicle', max_length=100, blank=True, null=True)  # Field name made lowercase.
    plate = models.CharField(db_column='Plate', max_length=100, blank=True, null=True)  # Field name made lowercase.
    timeout = models.DateTimeField(db_column='Timeout', blank=True, null=True)  # Field name made lowercase.
    operator = models.CharField(db_column='Operator', max_length=100, blank=True, null=True)  # Field name made lowercase.
    pc = models.CharField(db_column='PC', max_length=100, blank=True, null=True)  # Field name made lowercase.
    pic = models.TextField(db_column='PIC', blank=True, null=True)  # Field name made lowercase.
    pic2 = models.TextField(db_column='PIC2', blank=True, null=True)  # Field name made lowercase.
    lane = models.CharField(db_column='Lane', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'timeoutdb'


class Transaction(models.Model):
    pos_name = models.CharField(max_length=45, blank=True, null=True)
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
        managed = False
        db_table = 'transaction'


class TransactionZeroAmount(models.Model):
    transaction_date = models.DateTimeField(blank=True, null=True)
    business_date = models.DateField(blank=True, null=True)
    time_in = models.DateTimeField(blank=True, null=True)
    time_out = models.DateTimeField(blank=True, null=True)
    pos_name = models.CharField(max_length=45, blank=True, null=True)
    username = models.CharField(max_length=45, blank=True, null=True)
    parker_type = models.CharField(max_length=45, blank=True, null=True)
    parker_name = models.CharField(max_length=45, blank=True, null=True)
    parker_address = models.CharField(max_length=45, blank=True, null=True)
    parker_ref_id = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'transaction_zero_amount'


class Usercontroldb(models.Model):
    id = models.BigAutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    rulename = models.CharField(db_column='RuleName', max_length=30, blank=True, null=True)  # Field name made lowercase.
    serverset = models.IntegerField(db_column='ServerSet', blank=True, null=True)  # Field name made lowercase.
    userset = models.IntegerField(db_column='UserSet', blank=True, null=True)  # Field name made lowercase.
    deviceset = models.IntegerField(db_column='DeviceSet', blank=True, null=True)  # Field name made lowercase.
    chargingset = models.IntegerField(db_column='ChargingSet', blank=True, null=True)  # Field name made lowercase.
    reportset = models.IntegerField(db_column='ReportSet', blank=True, null=True)  # Field name made lowercase.
    terminateset = models.IntegerField(db_column='TerminateSet', blank=True, null=True)  # Field name made lowercase.
    setreference = models.IntegerField(db_column='Setreference', blank=True, null=True)  # Field name made lowercase.
    cashier = models.IntegerField(db_column='Cashier', blank=True, null=True)  # Field name made lowercase.
    logreport = models.IntegerField(db_column='LogReport', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'usercontroldb'


class VipTimein(models.Model):
    id = models.BigAutoField(primary_key=True)
    cardcode = models.CharField(db_column='CardCode', max_length=100, blank=True, null=True)  # Field name made lowercase.
    plate = models.CharField(db_column='Plate', max_length=100, blank=True, null=True)  # Field name made lowercase.
    timein = models.DateTimeField(db_column='Timein', blank=True, null=True)  # Field name made lowercase.
    zone = models.CharField(db_column='Zone', max_length=100, blank=True, null=True)  # Field name made lowercase.
    parker = models.CharField(db_column='Parker', max_length=100, blank=True, null=True)  # Field name made lowercase.
    pic1 = models.TextField(db_column='Pic1', blank=True, null=True)  # Field name made lowercase.
    mode = models.CharField(db_column='Mode', max_length=100, blank=True, null=True)  # Field name made lowercase.
    pic2 = models.TextField(db_column='Pic2', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'vip_timein'


class Vipdb(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(db_column='Name', max_length=100, blank=True, null=True)  # Field name made lowercase.
    plate = models.CharField(db_column='Plate', max_length=100, blank=True, null=True)  # Field name made lowercase.
    veh = models.CharField(db_column='VEH', max_length=100, blank=True, null=True)  # Field name made lowercase.
    cardcode = models.CharField(db_column='CardCode', max_length=100, blank=True, null=True)  # Field name made lowercase.
    remarks = models.CharField(db_column='Remarks', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'vipdb'


class Voucherreport(models.Model):
    id = models.BigAutoField(primary_key=True)
    trno = models.CharField(db_column='TRno', max_length=255, blank=True, null=True)  # Field name made lowercase.
    vouchertype = models.CharField(db_column='VoucherType', max_length=255, blank=True, null=True)  # Field name made lowercase.
    voucherref = models.CharField(db_column='VoucherRef', max_length=255, blank=True, null=True)  # Field name made lowercase.
    voucheramount = models.FloatField(db_column='VoucherAmount', blank=True, null=True)  # Field name made lowercase.
    cashier = models.CharField(db_column='Cashier', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'voucherreport'
