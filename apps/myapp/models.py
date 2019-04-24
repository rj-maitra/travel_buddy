from django.db import models
from datetime import datetime
import bcrypt

# All models dot managers must be first so the program knows what to do when it runs into that code!

class UserManager(models.Manager):

    def reg_validator(self, request):

        errors = {}

        is_logged_in = False

        user = User.objects.filter(username = request.POST['username'])

        if len(user) > 0:
            errors['username'] = "Username already in use"

        if len(request.POST['name']) < 3:
            errors['name'] = "Name must be at least 3 characters"

        if len(request.POST['username']) < 3:
            errors['username'] = "Username must be at least 3 characters"

        if len(request.POST['password']) < 8:
            errors['password'] = "Password must be at least 8 characters"

        elif request.POST['password'] != request.POST['password_confirmation']:
            errors['password'] = "Passwords do not match"

        if len(errors) < 1:
            hashedpw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            user = User.objects.create(name=request.POST['name'],username=request.POST['username'],password=hashedpw.decode())
            request.session['user_id'] = user.id
            is_logged_in = True

        info = [errors, is_logged_in]
        return info

        # return errors
    
    def login_validator(self, request):

        errors = {}
        
        is_logged_in = False
        
        user = User.objects.filter(username = request.POST['username'])

        if len(user) < 1:
            errors['username'] = "Please register with us before trying to log in"
        
        else:
            if not bcrypt.checkpw(request.POST['password'].encode(), User.objects.get(username = request.POST['username']).password.encode()):
                errors['password'] = "Incorrect password"

        # else:
        #     if not bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
        #         errors['password'] = "Incorrect password"

        if len(errors) < 1:
            user = User.objects.get(username=request.POST['username'])
            request.session['user_id'] = user.id
            is_logged_in = True

        info = [errors, is_logged_in]
        return info

        # return errors

    # def login_validator(self, request):

    #     errors = {}

    #     if len(request.POST['email']) < 1:
    #         errors['email'] = "Email cannot be blank"
    #     elif len(User.objects.filter(email = request.POST['email'])) < 1:
    #         errors['email']  = "Please register with us before trying to log in"
    #     else:
    #         user = User.objects.get(email = request.POST['email'])
    #         if not bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
    #             errors['password'] = "Incorrect password"
    #         else:
    #             request.session['user_id'] = user.id
    #     return errors
    
class TripManager(models.Manager):

    def trip_validator(self, request):

        errors = {}

        user = User.objects.get(id = request.session['user_id'])
        now = datetime.now()
        yesterday = datetime.today()

        if len(request.POST['destination']) < 1:
            errors['destination'] = "Please tell us where you are going"

        if len(request.POST['description']) < 1:
            errors['description'] = "Please give us a description of the trip"

        if len(request.POST['start']) < 10 or len(request.POST['end']) < 10:
            errors['date'] = "Date(s) missing from date field(s)"
        
        else:
            start = datetime.strptime(request.POST['start'], "%Y-%m-%d")
            end = datetime.strptime(request.POST['end'], "%Y-%m-%d")
            
            if start < now:
                errors['date'] = "The trip must begin in the future."
            
            elif end < now:
                errors['date'] = "The trip cannot end in the past"
            else:
                if end < start:
                    errors['date'] = "The trip must begin before it can end... unless you forget your passport!"
        
        if len(errors) < 1:
            trip = Trip.objects.create(destination = request.POST['destination'], description = request.POST['description'], travel_from = request.POST['start'], travel_to = request.POST['end'], planner = user)
            user.joins.add(trip)

        return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = UserManager()

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    travel_from = models.DateField()
    travel_to = models.DateField()
    planner = models.ForeignKey(User, related_name="trips", on_delete=models.CASCADE)
    joins = models.ManyToManyField(User, related_name="joins")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = TripManager()