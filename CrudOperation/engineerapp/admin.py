from calendar import c
import imp
from django.contrib import admin
from engineerapp.models import *

#adminde görünmesi için registerlıyorsun, modeldeki parametrelere göre django kendi CRUD appini yapıyor zaten ellemene gerek yok
admin.site.register(EngModel)

@admin.register(LPModel)
class LPModelAdmin(admin.ModelAdmin):
    list_display = ("description",)

@admin.register(LPStepsModel)
class LPStepsModelAdmin(admin.ModelAdmin):
    list_display = ("name","learningpath_id", "lp_step_id")

@admin.register(MIPModel)
class MIPModelAdmin(admin.ModelAdmin):
    list_display = ("mip_name","mip_id")