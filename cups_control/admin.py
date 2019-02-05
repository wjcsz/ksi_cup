from django.contrib import admin
from .models import CupOwner, Cup
# Register your models here.
class CupsInline(admin.TabularInline):
    model = Cup
    extra = 0


class CupOwnerAdmin(admin.ModelAdmin):
    inlines = [CupsInline]


admin.site.register(CupOwner, CupOwnerAdmin)
# admin.site.register(Cup)