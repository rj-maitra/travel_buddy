from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    return render(request, 'myapp/index.html')

def logout(request):
    request.session.clear()
    return redirect('/')

def register(request):
    
    errors = User.objects.reg_validator(request)

    if errors[1]:
        return redirect('/travels')
    else:
        for key, value in errors[0].items():
            messages.error(request, value)
        return redirect('/')

def login(request):
    
    errors = User.objects.login_validator(request)
    if errors[1]:
        return redirect('/travels')
    else:
        for key, value in errors[0].items():
            messages.error(request, value)
        return redirect('/')

def travels(request):
    
    if 'user_id' not in request.session:
        return redirect('/')
    
    else:
        user = User.objects.get(id=request.session['user_id'])
        trips = Trip.objects.all()
        myTrips = user.trips.all()
        
        joined = user.joins.all()
        notJoined = trips.difference(joined)

        joinedNotPlanner = user.joins.all().exclude(planner=user)

        context = {
            'user': user,
            'myTrips': myTrips,
            'joined' : joined,
            'notJoined' : notJoined,
            'joinedNotPlanner' : joinedNotPlanner,
        }
        return render(request, 'myapp/travels.html', context)

def add(request):
    
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        user = User.objects.get(id=request.session['user_id'])
        context = {
            'user': user
        }
        return render(request, 'myapp/create.html', context)

def join(request, trip_id):
    
    user = User.objects.get(id=request.session['user_id'])
    trip = Trip.objects.get(id=trip_id)
    user.joins.add(trip)
    return redirect('/travels')

def remove(request, trip_id):
    
    user = User.objects.get(id=request.session['user_id'])
    trip = Trip.objects.get(id=trip_id)
    user.joins.remove(trip)
    return redirect('/travels')

def destroy(request, trip_id):

    trip = Trip.objects.get(id = trip_id)
    trip.delete()
    return redirect('/travels')

def show(request, destination_id):
    
    trip = Trip.objects.get(id=destination_id)
    joined = trip.joins.all().exclude(trips = trip)
    context = {
        'trip': trip,
        'joined': joined
    }
    return render(request, 'myapp/show.html', context)

def create(request):
    
    errors = Trip.objects.trip_validator(request)

    if len(errors) < 1:
        return redirect('/travels')
    else:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/travels/add')
