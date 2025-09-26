
from django.contrib import admin


from .models import *
admin.site.register(Category)
admin.site.register(MovieTicket)
admin.site.register(MusicConsert)
admin.site.register(ComedyShow)
admin.site.register(SportsEvent)
admin.site.register(Sports_Ticket)
admin.site.register(Music_Ticket)
admin.site.register(Ticket)