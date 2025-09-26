from django.shortcuts import render,redirect
from . models import *
from django.contrib import messages
from .form import *
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail

import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

def index(request):
    Categorys = Category.objects.all()
    movies = MovieTicket.objects.all()   # fetch all movies

    return render(request, 'index.html', {
        'Category': Categorys,
        'movies': movies,
    })


def music(request):
    Music =MusicConsert.objects.all()
    return render(request,'music.html',{'MusicConsert':Music})


def sports(request):
    sports =SportsEvent.objects.all()
    return render(request,'sports.html',{'SportsEvent':sports})


def comedy(request):
    ComedyShows = ComedyShow.objects.all()
    return render(request,'comedy.html',{'ComedyShow':ComedyShows})



def screensita(request):
    return render(request, 'screensita.html')


# def screen(request):
#     return render(request, 'screen.html')

def movie(request):
    movie =MovieTicket.objects.all()
    return render(request, 'movies.html',{'MoviesTicket':movie})


def movie_detail(request, mname):
    movie = MovieTicket.objects.filter(name=mname).first()
    if movie:
        # Split the discription field by '|' into a list
        description_list = movie.discription.split('|') if movie.discription else []
        return render(request, 'movie_detials.html', {'movie': movie, 'description_list': description_list})
    else:
        return redirect('movie')
    

def music_detail(request,muname):
    music =MusicConsert.objects.filter(name=muname).first()
    if music:
        description_list = music.discription.split('|') if music.discription else []
        return render(request,'music_detail.html',{'music':music, 'description_list': description_list})
    

def comedy_detail(request,cname):
    comedy = ComedyShow.objects.filter(name=cname).first()
    if comedy:
        description_list =comedy.discription.split('|') if comedy.discription else []
        return render(request,'comedy_detail.html',{'comedy':comedy ,'description_list': description_list})

def sports_detail(request,sname):
    sport =SportsEvent.objects.filter(name=sname).first()
    if sport:
        description_list =sport.discription.split('|') if sport.discription else []
        return render(request, 'sport_detail.html', {'sport': sport,'description_list': description_list})
   

def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user= form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request,'Registeration successfull. You can log in ')
            return redirect('login')
            
    return render (request,'register.html',{'form':form})

def login (request):
    form = LoginForm()
    if request.method == 'POST':
        form =LoginForm(request.POST)
        if form.is_valid():
            username =form.cleaned_data['username']
            password =form.cleaned_data['password']
            User =authenticate(username=username,password=password)
            if User is not None:
                auth_login(request, User)
                return redirect('index')
            print('Success')


    return render (request,'login.html',{'form': form})

def logout(request):
    auth_logout(request)
    return redirect('login')

def forgot_password(request):
    form = ForgotPasswordForm()
    if request.method == "POST":
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)

            # Generate token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            current_site = get_current_site(request)
            domain = current_site.domain

            # Render email template
            message = render_to_string('reset_password_email.html', {
                'domain': domain,
                'uid': uid,
                'token': token
            })

            # Send email
            send_mail(
                subject='Reset Password Requested',
                message=message,
                from_email='noreply@escobar.com',
                recipient_list=[email],
                fail_silently=False
            )

            messages.success(request, 'An email has been sent with password reset instructions.')
            return redirect('forgot_password')  # or redirect somewhere else

    return render(request, 'forgot_password.html', {'form': form})

def reset_password(request):
    pass





import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import SportsEvent, Sports_Ticket

def sport_ticket(request):
    
    if request.method == "POST" and request.headers.get("x-requested-with") == "XMLHttpRequest":
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'Please login to book tickets!'}, status=401)

        try:
            data = json.loads(request.body)
            
            sheet_count = int(data.get('sheet', 0))
            sport_id = int(data.get('id', 0))

            if sheet_count <= 0:
                return JsonResponse({'status': 'Please select at least 1 ticket!'}, status=400)

            try:
                sport_event = SportsEvent.objects.get(id=sport_id)
                
            except SportsEvent.DoesNotExist:
                return JsonResponse({'status': 'Sports event not found!'}, status=404)

            if sport_event.Available_sheet < sheet_count:
                return JsonResponse({'status': 'Not enough available tickets!'}, status=400)
            

            total_price = sheet_count * (sport_event.Premium_price or 0)

            # Save the ticket
            Sports_Ticket.objects.create(
                user=request.user,
                sport=sport_event,
                Total_ticket=sheet_count,
                Total_price=total_price
            )

            # Update available sheets
            sport_event.Available_sheet -= sheet_count
            sport_event.save()

            return JsonResponse({
                'status': f'Ticket booked successfully for {sheet_count} seat(s)!',
                'total_price': total_price
            }, status=200)

        except ValueError:
            return JsonResponse({'status': 'Invalid input!'}, status=400)
        except Exception as e:
            return JsonResponse({'status': f'Error: {str(e)}'}, status=400)

    return JsonResponse({'status': 'Invalid request!'}, status=400)





# music Ticket

def music_ticket(request):
    # Check if AJAX POST request
    if request.method == "POST" and request.headers.get("x-requested-with") == "XMLHttpRequest":
        
        # Check if user is logged in
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'Please login to book tickets!'}, status=401)

        try:
            # Parse JSON from request body
            data = json.loads(request.body)
            seat_count = int(data.get('sheet', 0))
            music_id = int(data.get('id'))

            if seat_count <= 0:
                return JsonResponse({'status': 'Please select at least 1 seat!'}, status=400)

            # Get the music event
            try:
                music_event = MusicConsert.objects.get(id=music_id)
            except MusicConsert.DoesNotExist:
                return JsonResponse({'status': 'Music event not found!'}, status=404)

            # Check availability
            if music_event.Available_sheet < seat_count:
                return JsonResponse({'status': 'Not enough available seats!'}, status=400)

            # Calculate total price (optional)
            total_price = seat_count * (music_event.Premium_price or 0)

            # Save ticket booking
            Music_Ticket.objects.create(
                user=request.user,
                music=music_event,
                Total_ticket=seat_count,
                Total_price=total_price
            )

            # Reduce available seats
            music_event.Available_sheet -= seat_count
            music_event.save()

            # Return success response
            return JsonResponse({
                'status': f'Ticket booked successfully for {seat_count} seat(s)!',
                'total_price': total_price
            }, status=200)

        except Exception as e:
            return JsonResponse({'status': f'Error: {str(e)}'}, status=400)

    # Invalid request
    return JsonResponse({'status': 'Invalid request!'}, status=400)



# comedy Ticket


def comedy_ticket(request):
    if request.method == "POST" and request.headers.get("x-requested-with") == "XMLHttpRequest":
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'Please login to book tickets!'}, status=401)
        try:
            data = json.loads(request.body)
            sheet_count = int(data.get('sheet', 0))
            comedy_id = int(data.get('id', 0))

            if sheet_count <= 0:
                return JsonResponse({'status': 'Please select at least 1 seat!'}, status=400)

            comedy_event = ComedyShow.objects.get(id=comedy_id)

            if comedy_event.Available_sheet < sheet_count:
                return JsonResponse({'status': 'Not enough available sheets!'}, status=400)

            total_price = sheet_count * (comedy_event.Premium_price or 0)

            Comedy_Ticket.objects.create(
                user=request.user,
                comedy=comedy_event,
                Total_ticket=sheet_count,
                Total_price=total_price
            )

            comedy_event.Available_sheet -= sheet_count
            comedy_event.save()

            return JsonResponse({
                'status': f'Ticket booked successfully for {sheet_count} seat(s)!',
                'total_price': total_price
            }, status=200)

        except ComedyShow.DoesNotExist:
            return JsonResponse({'status': 'Event not found!'}, status=404)
        except Exception as e:
            return JsonResponse({'status': f'Error: {str(e)}'}, status=400)

    return JsonResponse({'status': 'Invalid request!'}, status=400)



def ticket_show(request):
    if request.user.is_authenticated:
        sport_ticket = Sports_Ticket.objects.filter(user=request.user)
        music_tickets = Music_Ticket.objects.filter(user=request.user)
        comedy_tickets = Comedy_Ticket.objects.filter(user=request.user)
        movie_tickets = Ticket.objects.filter(user=request.user)
        context = {
            'sport_ticket': sport_ticket,
            'music_tickets': music_tickets,
            'comedy_tickets':comedy_tickets,
            'movie_tickets': movie_tickets
        }
        return render(request, 'ticket_show.html', context)
    else:
        return redirect('index')








# Movie Ticket

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import MovieTicket, Ticket, MovieTiming
import json

# -----------------------------------
# View: Seat selection page
# -----------------------------------
def seat_selection(request, movie_id):
    movie = get_object_or_404(MovieTicket, id=movie_id)
    date = request.GET.get('date')
    time = request.GET.get('time')

    # Get the corresponding MovieTiming object
    timing_obj = None
    if date and time:
        try:
            timing_obj = MovieTiming.objects.get(movie=movie, date=date, time=time)
        except MovieTiming.DoesNotExist:
            timing_obj = None

    # Fetch booked seats for this movie
    booked_seats = []
    tickets = Ticket.objects.filter(movie=movie)
    for ticket in tickets:
        booked_seats.extend(ticket.seats)

    context = {
        'movie': movie,
        'selected_date': date,
        'selected_time': time,
        'timing_obj': timing_obj,
        'booked_seats': booked_seats,  # passed to JS
    }
    return render(request, 'screen.html', context)

# -----------------------------------
# View: Book ticket (AJAX POST)
# -----------------------------------
@csrf_exempt  # For testing; use CSRF token in production


def book_ticket(request, movie_id):
    if request.method == "POST":
        data = json.loads(request.body)
        date = data.get("date")
        time = data.get("time")
        seats = data.get("seats", [])

        movie = get_object_or_404(MovieTicket, id=movie_id)

        # Validate seats: check if already booked
        booked_seats = Ticket.get_booked_seats(movie_id)
        for seat in seats:
            if seat in booked_seats:
                return JsonResponse({"success": False, "error": f"Seat {seat} is already booked"})

        # Determine total price
        try:
            timing_obj = MovieTiming.objects.get(movie=movie, date=date, time=time)
            total_price = timing_obj.price * len(seats)
        except MovieTiming.DoesNotExist:
            total_price = 200 * len(seats)  # fallback default price

        # Create booking
        ticket = Ticket.objects.create(
            user=request.user,
            movie=movie,
            seats=seats,
            total_price=total_price,
            show_date=date,
            show_time=time,
        )

        # ✅ Return ticket ID for redirect
        return JsonResponse({
            "success": True,
            "ticket_id": ticket.id,  # this is the key part
            "total_price": total_price,
            "seats": seats
        })

    return JsonResponse({"success": False, "error": "Invalid request"})