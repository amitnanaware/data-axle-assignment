from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm

from .forms import UserRegisterForm, ParkingSpotForm, ReservationForm
from .models import ParkingSpot, Reservation


def view_reservations(request):
    reservations = Reservation.objects.filter(user=request.user)
    return render(request, 'parking_app/view_reservations.html', {'reservations': reservations})


def add_parking_spot(request):
    if request.method == 'POST':
        form = ParkingSpotForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_parking_spots')
    else:
        form = ParkingSpotForm()

    return render(request, 'parking_app/add_parking_spot.html', {'form': form})


def view_parking_spots(request):
    parking_spots = ParkingSpot.objects.all()
    return render(request, 'parking_app/parking_spots.html', {'parking_spots': parking_spots})


def search_nearby_parking(request):
    latitude = request.GET.get('latitude')
    longitude = request.GET.get('longitude')
    radius = request.GET.get('radius')

    if latitude and longitude and radius:
        search_point = Point(float(longitude), float(latitude))
        search_radius = Distance(m=float(radius))

        parking_spots = ParkingSpot.objects.filter(
            location__distance_lte=(search_point, search_radius),
            availability=True
        )
    else:
        parking_spots = ParkingSpot.objects.filter(availability=True)

    return render(request, 'parking_app/search_nearby.html', {'parking_spots': parking_spots})


def reserve_parking_spot(request, spot_id):
    parking_spot = get_object_or_404(ParkingSpot, id=spot_id)

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            hours = form.cleaned_data['hours']
            total_price = parking_spot.price_per_hour * hours
            reservation = Reservation.objects.create(
                user=request.user,
                parking_spot=parking_spot,
                hours=hours,
                total_price=total_price
            )
            price = reservation.calculate_price()
            parking_spot.availability = False
            parking_spot.save()
            return render(request, 'parking_app/reservation_confirm.html', {'reservation': reservation, 'price': price})

    else:
        form = ReservationForm()

    return render(request, 'parking_app/reserve_parking_spot.html', {'parking_spot': parking_spot, 'form': form})


def index(request):
    return render(request, 'parking_app/index.html', {'title': 'Parking App'})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been created ! You are now able to log in')
            return redirect('login')
        else:
            messages.error(request, form.error_messages)
    else:
        form = UserRegisterForm()
    return render(request, 'parking_app/register.html', {'form': form, 'title': 'register here'})


def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            form = login(request, user)
            messages.success(request, f' welcome {username} !!')
            return redirect('index')
        else:
            messages.info(request, f'Account does not exit please sign in')
    form = AuthenticationForm()
    return render(request, 'parking_app/login.html', {'form': form, 'title': 'log in'})
