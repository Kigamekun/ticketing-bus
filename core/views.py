from django.shortcuts import render,redirect
from .models import *
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.
from datetime import datetime
from datetime import date
import json

from django.db.models import Sum
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None



def index(request):
    data = Bus.objects.all()
    context = {
        "data":data
    }
    if request.method == "POST":
        print(request.POST['name'],request.POST['message'])
    return render(request,'index.html',context)


def pesan(request):
    data = Bus.objects.all()
    track = Track.objects.all()
    track1 = []
    track2 = []
    for tk in track:
        if tk.track1 in track1:
            pass
        else :
            track1.append(tk.track1)
            
    for tk in track:
        if tk.track2 in track2:
            pass
        else :
            track2.append(tk.track2)
    
    
    
    context = {
        "data":data,
        "track1":track1,
        "track2":track2
    }
    return render(request,'pesan.html',context)


def cari(request,track1,track2,bulan,tanggal,tahun):
    tanggal = date(year=int(tahun), month=int(bulan),day=int(tanggal))
    # print(tanggal)
    jalur = Track.objects.get(track1=track1,track2=track2)
    dataBus = Bus.objects.filter(trayek=jalur.trayek)
    
    out = "<div id='busList' style='width:250px;height:500px;display: flex; flex-flow: row wrap;'>"
    
    for data in dataBus:
        out += '<div title="supir" style="width: 208px;height: 50px ;margin:8px;" class="btn btn-danger">Supir ('+data.platNo+')</div>'
        solve = Bus.objects.get(platNo=data.platNo)
        solved = Seat.objects.filter(bus=solve)
        # out += '<div id="ck-button">'
        for i in solved:
            if Ticket.objects.filter(bus=solve,tanggal=tanggal,kursi=i,track=jalur).exists():
                # print('ada',i)
                out +=  '<div class="ck-button1" id="ck-button1"><center><label><div>'+str(i)+'</div></label></center></div>'
            else :
                out +=  '<div class="ck-button" id="ck-button"><label><input type="checkbox" value="'+ str(i) +' '+ data.platNo+'"><span>'+ str(i) +'</span></label></div>'
        # out += '</div>'
    out += "</div>"
    print(out)
    return HttpResponse(out)


# <div title="'+ str(i) + '" style="width: 50px;height: 50px ;margin:2px;" class="btn btn-success"></div>



def beli_tiket(request):
    if request.method == "POST":
        listTic = request.POST.getlist('selected[]')
        # print(list(request.POST.items()))
        for i in listTic:
            y = i.split()
            tgl = request.POST['tanggal'].split('/')
            print(tgl)
            tanggal = datetime(year=int(tgl[2]), month=int(tgl[0]),day=int(tgl[1]))
            jalur = Track.objects.get(track1=request.POST['track1'],track2=request.POST['track2'])
            bus = Bus.objects.get(platNo=y[1])
            x = Ticket.objects.create(user=request.user,bus=bus,nama=request.POST['nama'],tanggal=tanggal,track=jalur,kursi=y[0],harga=jalur.harga)
        x.save()

        
        payment,created = Bukti_pembayaran.objects.get_or_create(user=request.user,accepted=False)
        Total_all = Ticket.objects.filter(user=request.user).aggregate(total=Sum('harga'))
        payment.total_harga = Total_all['total']
        payment.save()
        response = {'status': 1, 'message': "Ok"}
        return HttpResponse(json.dumps(response), content_type='application/json')



def listbus(request):
    bus = Bus.objects.all()
    context = {
        'bus':bus,
        
    }
    return render(request,'list.html',context)


def pdf(request):
    #Retrieve data or whatever you need
    template = get_template('mytemplate.html')
    context = {
            "invoice_id": 123,
            "customer_name": "John Cooper",
            "amount": 1399.99,
            "today": "Today",
        }
    html = template.render(context)
    pdf = render_to_pdf('mytemplate.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Invoice_%s.pdf" %("12341231")
        content = "inline; filename='%s'" %(filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")    


def my_ticket(request):
    data = Bukti_pembayaran.objects.get(user=request.user)
    inDay = datetime.now().date()
    remain = []
    solve = Ticket.objects.filter(user=request.user)
    for x in solve:
        if x.tanggal < inDay:
            remain.append('Expire')
        else :
            remaining = str(x.tanggal - inDay)
            remaining = remaining.split(',')
            remaining = remaining[0].split()
            remain.append(int(remaining[0]))
    context = {'solve':zip(solve,remain),'data':data}
    return render(request,'my_ticket.html',context)