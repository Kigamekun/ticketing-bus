from django.urls import path

app_name = 'core'

from .views import *
urlpatterns = [
    path('',index,name="index"),
    path("pesan/", pesan, name="pesan"),
    path("listbus/", listbus, name="listbus"),
    path('pesan/cari/<track1>/<track2>/<bulan>/<tanggal>/<tahun>/',cari,name="cari"),
    path("pesan/beli_tiket/", beli_tiket, name="beli_tiket"),
    path("my_ticket/", my_ticket, name="my_ticket"),
    
    path('pdf/',pdf)
]
