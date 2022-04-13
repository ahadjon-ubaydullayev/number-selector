from django.contrib import admin

from number.models import *



@admin.register(UserAction)
class UserActionAdmin(admin.ModelAdmin):
    pass


@admin.register(SimOrder)
class SimOrderAdmin(admin.ModelAdmin):
    pass