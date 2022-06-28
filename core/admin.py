from django.contrib import admin
from admin_object_actions.admin import ModelAdminObjectActionsMixin
# Register your models here.
from .models import *

class BusAdmin(admin.ModelAdmin):
    list_display = ['platNo','jumKursi','trayek']
    search_fields = ['platNo']
    list_per_page = 15
    empty_value_display = 'kosong nih'

admin.site.register(Bus,BusAdmin)

class SeatAdmin(admin.ModelAdmin):
    list_display = ['seats','bus']
    search_fields = ['bus']
    list_filter = ['bus']
    list_per_page = 16
    empty_value_display = 'ada yang error keknya'
admin.site.register(Seat,SeatAdmin)

class TrackAdmin(admin.ModelAdmin):
    list_display = ['trayek','track1','track2','harga']
    search_fields = ['trayek']
    list_filter = ['trayek']
    list_per_page = 15
    empty_value_display = 'kosong nih'
admin.site.register(Track,TrackAdmin)


class TicketAdmin(ModelAdminObjectActionsMixin,admin.ModelAdmin):
    list_display = ['nama','tanggal','track','bus','kursi','harga']
    search_fields = ['nama','tanggal']
    list_filter = ['tanggal','track']
    list_per_page = 15
    empty_value_display = 'Error need backup'
    
    # object_actions = [
    #     {
    #         'slug': 'print',
    #         'verbose_name': 'Print',
    #         'form_method': 'GET',
    #         'view': 'print_view',
    #     },
    # ]

    # def setuju(self,request,queryset):
    #     print('a')

    # def print_view(self, request, object_id, form_url='', extra_context=None, action=None):
    #     from django.template.response import TemplateResponse
    #     obj = self.get_object(request, object_id)
    #     return TemplateResponse(request, 'print.html', {'obj': obj})
    
    
admin.site.register(Ticket,TicketAdmin)

admin.site.register(Trayek)

admin.site.register(Bukti_pembayaran)
