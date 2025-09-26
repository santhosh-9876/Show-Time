
from django.db import models
import datetime
import os
from django.contrib.auth.models import User




def getFileName(request,filename):
    now_time=datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")
    new_filename='%s%s'%(now_time,filename)
    return os.path.join('uploads/',new_filename)

class Category(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False)
    link_name = models.CharField(max_length=150, null=False, blank=False, default='default-link')
    image = models.ImageField(upload_to=getFileName, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name




class MovieTicket(models.Model):
    Quality=[
        ('2D','2D'),
        ('3D','3D')
    ]
    name=models.CharField(max_length=150,null=False,blank=False)
    image=models.ImageField(upload_to=getFileName,null=True,blank=True)
    showing_or_IMDB=models.CharField(max_length=100, default="Upcomming...")
    nowShowing=models.BooleanField(default=False,help_text="1-show,0-Hidden")
    upcoming=models.BooleanField(default=False,help_text="1-show,0-Hidden")
    created_at=models.DateTimeField(auto_now_add=True)
    timing = models.CharField(max_length=150,null=True,blank=True)
    D_quality =models.CharField(max_length=2,choices=Quality,null=True,blank=True)
    discription = models.TextField(max_length=1000,null=True,blank=True,default=None)
    carosel_image=models.ImageField(upload_to=getFileName,null=True,blank=True)
    upcoming_date = models.CharField(max_length=100,null=True,blank=True)
    upcoming_language =models.CharField(max_length=150,null=True,blank=True)

    def __str__(self):
        return self.name



class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(MovieTicket, on_delete=models.CASCADE)
    seats = models.JSONField()
    total_price = models.FloatField()
    booked_at = models.DateTimeField(auto_now_add=True)

    show_date = models.DateField(null=True, blank=True)   # allows nulls
    show_time = models.TimeField(null=True, blank=True)   # allows nulls

    def __str__(self):
        return f"{self.user.username} - {self.movie.name} - {', '.join(self.seats)}"



    
    # Fetch booked seats for a specific movie
    @staticmethod
    def get_booked_seats(movie_id):
        tickets = Ticket.objects.filter(movie_id=movie_id)
        booked_seats = []
        for ticket in tickets:
            booked_seats.extend(ticket.seats)
        return booked_seats
    

# Optional: Model for showing multiple time slots per movie
class MovieTiming(models.Model):
    movie = models.ForeignKey(MovieTicket, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    price = models.FloatField(default=200)  # default ticket price

    def __str__(self):
        return f"{self.movie.name} - {self.date} {self.time}"
    

    

class MusicConsert(models.Model):
    name=models.CharField(max_length=150,null=False,blank=False)
    image=models.ImageField(upload_to=getFileName,null=True,blank=True)
    showing_time=models.CharField(max_length=100, default="comming soon..")
    created_at=models.DateTimeField(auto_now_add=True)
    nowShowing=models.BooleanField(default=False,help_text='1-Show,0-Hidden')
    upcoming =models.BooleanField(default=False,help_text='1-Show,0-Hidden')
    Date =models.CharField(max_length=150,null=True,blank=True)
    Time =models.CharField(max_length=150,null=True,blank=True)
    Duration =models.CharField(max_length=150,null=True,blank=True)
    Age=models.CharField(max_length=150,null=True,blank=True)
    Location =models.CharField(max_length=150,null=True,blank=True)
    discription=models.TextField(max_length=1000,null=False,blank=False,default=None)
    Available_sheet=models.IntegerField(null=True,blank=True)
    Premium_price =models.FloatField(null=True,blank=True)
    

    def __str__(self):
        return self.name


class ComedyShow(models.Model):
    name=models.CharField(max_length=150,null=False,blank=False)
    image=models.ImageField(upload_to=getFileName,null=True,blank=True)
    showing_time=models.CharField(max_length=100, default="comming soon..")
    created_at=models.DateTimeField(auto_now_add=True)
    nowShowing =models.BooleanField(default=False,help_text='1-show,0-Hidden')
    upcoming =models.BooleanField(default=False,help_text='1-show,0-Hidden')
    Date =models.CharField(max_length=150,null=True,blank=True)
    Time =models.CharField(max_length=150,null=True,blank=True)
    Duration =models.CharField(max_length=150,null=True,blank=True)
    Age=models.CharField(max_length=150,null=True,blank=True)
    Location =models.CharField(max_length=150,null=True,blank=True)
    discription=models.TextField(max_length=1000,null=False,blank=False,default=None)
    Available_sheet=models.IntegerField(null=True,blank=True)
    Premium_price =models.FloatField(null=True,blank=True)
    



    def __str__(self):
        return self.name

class SportsEvent(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False)
    image = models.ImageField(upload_to='sports/', null=True, blank=True)
    showing_time = models.CharField(max_length=100, default="coming soon..")
    created_at = models.DateTimeField(auto_now_add=True)
    nowShowing = models.BooleanField(default=False)
    upcoming = models.BooleanField(default=False)
    Date = models.CharField(max_length=150, null=True, blank=True)
    Time = models.CharField(max_length=150, null=True, blank=True)
    Duration = models.CharField(max_length=150, null=True, blank=True)
    Age = models.CharField(max_length=150, null=True, blank=True)
    Location = models.CharField(max_length=150, null=True, blank=True)
    discription = models.TextField(max_length=1000, null=False, blank=False, default="")
    Available_sheet = models.IntegerField(default=0)
    Premium_price = models.FloatField(default=0.0)

    def __str__(self):
        return self.name

class Sports_Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sport = models.ForeignKey(SportsEvent, on_delete=models.CASCADE,null=True,blank=True)
    Total_ticket = models.IntegerField(default=1)
    Total_price = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.sport} - {self.Total_ticket}"

class Music_Ticket(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    music = models.ForeignKey(MusicConsert, on_delete=models.CASCADE, null=True, blank=True)

    Total_ticket=models.IntegerField(null=True,blank=True)
    Total_price = models.FloatField(default=0)

    created_at=models.DateTimeField(auto_now_add=True)



class Comedy_Ticket(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    comedy = models.ForeignKey(ComedyShow, on_delete=models.CASCADE, null=True, blank=True)

    Total_ticket=models.IntegerField(null=True,blank=True)
    Total_price =models.FloatField(null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)