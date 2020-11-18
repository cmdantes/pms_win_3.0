from django.contrib import admin
from .models import *

@admin.register(ChargingRule)
class ChargingRuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'vehicle', 'minimum_minutes', 'minimum_amount', 'succeeding_amount', 'flat_rate', 'overnight_amount', 'lost_card', 'overnight_start', 'overnight_end', 'ov_24', 'status')
    list_filter = ('name', 'vehicle')
    search_fields = ('name', 'vehicle')
    ordering = ('status',)
    def has_delete_permission(self, request, obj=None):
        #Disable delete
        return False

@admin.register(FlatRateDays)
class FlatRateDaysAdmin(admin.ModelAdmin):
    list_display = ('rule_name', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'holiday')
    search_fields = ('rule_name',)

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('discount_type', 'vat_exempt', 'percentage', 'is_free', 'status')
    search_fields = ('discount_type',)

@admin.register(DiscountFix)
class DiscountFixAdmin(admin.ModelAdmin):
    list_display = ('discount_type', 'vat_exempt', 'percentage', 'is_free', 'status')
    search_fields = ('discount_type',)

@admin.register(Vouchers)
class VouchersAdmin(admin.ModelAdmin):
    list_display = ('voucher_type', 'amount_value', 'status')
    search_fields = ('voucher_type',)

@admin.register(NonCash)
class NonCashAdmin(admin.ModelAdmin):
    list_display = ('name', 'status')
    search_fields = ('name',)

@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
    list_display = ('holiday_date', 'name')
    search_fields = ('name',)