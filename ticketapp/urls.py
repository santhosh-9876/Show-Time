from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('music/', music, name='music'),
    path('sports/', sports, name='sports'),
    path('comedy/', comedy, name='comedy'),
    path('movie/', movie, name='movie'),   
    
    # Screen URLs
    # path('screen/<int:movie_id>/', screen, name='screen'),  
    # path('screen/<int:movie_id>/', screen, name='screen_with_id'), 
    
    path('screensita/', screensita, name='screensita'),
    
    # Details URLs
    path('movie_detail/<str:mname>', movie_detail, name='movie_detail'),
    path('music_detail/<str:muname>', music_detail, name='music_detail'),
    path('comedy_detail/<str:cname>', comedy_detail, name='comedy_detail'),
    path('sport_detail/<str:sname>', sports_detail, name='sport_detail'),
    
    # Ticket URLs
    path('sport_ticket/', sport_ticket, name='sport_ticket'),
    path('music_ticket/', music_ticket, name='music_ticket'),
    path('comedy_ticket/', comedy_ticket, name='comedy_ticket'),
    path('ticket_show/', ticket_show, name='ticket_show'),
    
    # Auth URLs
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('forgot_password/', forgot_password, name='forgot_password'),
    path('reset_password/<uid64>/<token>', reset_password, name='reset_password'),

    # **Seats page URL**
    # urls.py
    # path('movie/<int:movie_id>/seats/', seat_selection, name='seat_selection'),
    # path('movie/<int:movie_id>/book/', book_ticket, name='book_ticket'),


     path('movie/<int:movie_id>/seats/', seat_selection, name='seat_selection'),
    path('movie/<int:movie_id>/book_ticket/', book_ticket, name='book_ticket'),

]
