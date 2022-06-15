from django.contrib import admin
from website.models import Account
from website.models import Truck
from website.models import Helper
from website.models import Truck_Part
from website.models import Payment
#  Register your models here.


class AccountAdmin(admin.ModelAdmin):
    list_display = ["username",'payrate','outstanding_balance']
    search_fields = ['username' ]


admin.site.register(Account,AccountAdmin)
admin.site.register(Truck)
admin.site.register(Helper)
admin.site.register(Truck_Part)
admin.site.register(Payment)


