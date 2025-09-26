from .models import *

def Movie(request):
    return{'MoviesTicket':MovieTicket.objects.all()}

def Music(request):
    return{'MusicConsert':MusicConsert.objects.all()}

def Sports(request):
    return{'SportsEvent':SportsEvent.objects.all()}

def Comedy(request):
    return{'ComedyShow':ComedyShow.objects.all()}


def movie_detail(request, mname):
    movie = MovieTicket.objects.filter(name=mname).first()
    if movie:
        # Split the discription field by '|' into a list
        description_list = movie.discription.split('|') if movie.discription else []
        return {(request, 'movie_detials.html', {'movie': movie, 'description_list': description_list})}
   