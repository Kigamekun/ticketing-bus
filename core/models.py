from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
import string 
from django.contrib.auth.models import User

    

class Trayek(models.Model):
    trayek = models.CharField(max_length=255)
    
    def __str__(self):
        return self.trayek
    


class Track(models.Model):
    trayek = models.ForeignKey(Trayek,on_delete=models.CASCADE)
    track1 = models.CharField(max_length=15)
    track2 = models.CharField(max_length=15)
    harga = models.IntegerField()
    
    def __str__(self):
        return 'from {} to -> {}'.format(self.track1,self.track2)
    
class Bus(models.Model):
    platNo = models.CharField(max_length=10)
    jumKursi = models.PositiveIntegerField()
    trayek = models.ForeignKey(Trayek,on_delete=models.CASCADE) 
    img = models.ImageField(upload_to="media/" , null=True,blank=True)

    def __str__(self):
        return '{}/{}'.format(self.id,self.platNo)
    
class Seat(models.Model):
    seats = models.CharField(max_length=5)
    bus = models.ForeignKey(Bus,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.seats

class Ticket(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    nama = models.CharField(max_length=255)
    tanggal = models.DateField()
    track = models.ForeignKey(Track,on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus,on_delete=models.CASCADE)
    kursi = models.CharField(max_length=255)
    harga = models.PositiveIntegerField()
    activated = models.BooleanField(default=False)
    
    def __str__(self):
        return '{}/{}'.format(self.nama,self.tanggal)
# function to create seats
@receiver(post_save, sender=Bus)
def create_seats(sender, instance, created, **kwargs):
    
    if created:
        loop = 0 
        mark = []
        solve = int(instance.jumKursi/3)
        
        buz = Bus.objects.get(platNo=instance.platNo)
        a = ''
        for i in range(1,solve+1):
            for j in range(3):
                a = str(i)
                Seat.objects.create(bus=buz,seats=str(i)+string.ascii_uppercase[j])
        
        if instance.jumKursi % 3 != 0 :
            for i in range(instance.jumKursi % 3):
                Seat.objects.create(bus=buz,seats=a + string.ascii_uppercase[i+3])     


class Bukti_pembayaran(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    bukti = models.ImageField(upload_to='bukti/',blank=True)
    accepted = models.BooleanField(default=False)
    total_harga = models.IntegerField()
    
    def __str__(self):
        return ' {} / {}'.format(self.user,self.total_harga)