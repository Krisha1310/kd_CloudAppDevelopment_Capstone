from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.csrf import csrf_exempt
# from .models import related models
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    return render(request, "djangoapp/about.html")


# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, "djangoapp/contact.html")

# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_request(request):
    context = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return redirect('djangoapp:index')
        else:
            # If not, return to login page again
            return render(request, 'djangoapp:login', context)
    else:
        return render(request, 'djangoapp:login', context)


# Create a `logout_request` view to handle sign out request
@csrf_exempt
def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
@csrf_exempt
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.debug("{} is new user".format(username))
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:login")
        else:
            return render(request, 'djangoapp/registration.html', context)


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "https://apikey-v2-2d53dn1z4iboxkuoffup1yaa9zepi6ko7310090uaenq:97bae6185a04aa9e89b680aa6ecfffea@28a85d67-812f-4064-a904-1402dd101f30-bluemix.cloudantnosqldb.appdomain.cloud/dealerships/dealer-get"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        url = "https://apikey-v2-2d53dn1z4iboxkuoffup1yaa9zepi6ko7310090uaenq:97bae6185a04aa9e89b680aa6ecfffea@28a85d67-812f-4064-a904-1402dd101f30-bluemix.cloudantnosqldb.appdomain.cloud/reviews/review-get"
        # Get dealers from the URL
        dealerships = get_dealer_reviews_from_cf(url, dealer_id)
        # Concat all dealer's short name
        dealer_reviews = ' '.join([dealer.review for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_reviews)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_review(request, dealer_id):
     if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        url = "https://apikey-v2-2d53dn1z4iboxkuoffup1yaa9zepi6ko7310090uaenq:97bae6185a04aa9e89b680aa6ecfffea@28a85d67-812f-4064-a904-1402dd101f30-bluemix.cloudantnosqldb.appdomain.cloud/reviews/review-post"
        if user is not None:
            review = dict()
            review["time"] = datetime.utcnow().isoformat()
            review["dealership"] = 11
            review["review"] = "This is a great car dealer"
            review["car_make"] = "BMW"
            json_payload["review"] = review
            
            ResponsePost = post_request(url, json_payload, dealerId=dealer_id)

            return HttpResponse(ResponsePost)
