# Uncomment the required imports before adding the code

from django.contrib.auth.models import User
from django.contrib.auth import logout

from django.http import JsonResponse
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.contrib.auth import login, authenticate
import logging
import json
from urllib.parse import quote
from django.views.decorators.csrf import csrf_exempt
from .populate import initiate
from .models import CarModel
from .restapis import get_request, analyze_review_sentiments, post_review


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    # Get username and password from request.POST dictionary
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    # Try to check if provide credential can be authenticated
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        # If user is valid, call login method to login current user
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    data = {"userName": ""}
    return JsonResponse(data)


# Create a `registration` view to handle sign up request
@csrf_exempt
def registration(request):
    if request.method != "POST":
        return JsonResponse(
            {"error": "Method not allowed"}, status=405
        )
    try:
        data = json.loads(request.body)
        username = data["userName"].strip()
        password = data["password"]
        first_name = data["firstName"].strip()
        last_name = data["lastName"].strip()
        email = data["email"].strip()
        if not all((username, password, first_name, last_name, email)):
            return JsonResponse(
                {"error": "All fields are required"}, status=400
            )
        if User.objects.filter(username=username).exists():
            return JsonResponse(
                {"error": "Already Registered"}, status=409
            )
        user = User(
            username=username, first_name=first_name,
            last_name=last_name, email=email,
        )
        validate_email(email)
        user.full_clean(exclude=["password"])
        validate_password(password, user)
        user.set_password(password)
        user.save()
    except IntegrityError:
        return JsonResponse(
            {"error": "Already Registered"}, status=409
        )
    except ValidationError as exc:
        return JsonResponse(
            {"error": " ".join(exc.messages)}, status=400
        )
    except (ValueError, KeyError, TypeError, AttributeError):
        return JsonResponse(
            {"error": "Invalid registration data"}, status=400
        )
    login(request, user)
    return JsonResponse({"userName": username, "status": "Authenticated"})


def get_dealerships(request, state="All"):
    endpoint = "/fetchDealers"
    if state and state.lower() != "all":
        endpoint += "/" + quote(state, safe="")
    dealers = get_request(endpoint)
    if not isinstance(dealers, list):
        return JsonResponse(
            {"status": 502, "message": "Unable to retrieve dealerships"}, status=502
        )
    return JsonResponse({"status": 200, "dealers": dealers})


def get_dealer_details(request, dealer_id):
    dealer = get_request("/fetchDealer/" + str(dealer_id))
    if not isinstance(dealer, list):
        return JsonResponse(
            {"status": 502, "message": "Unable to retrieve dealer"}, status=502
        )
    if not dealer:
        return JsonResponse(
            {"status": 404, "dealer": [], "message": "Dealer not found"}, status=404
        )
    return JsonResponse({"status": 200, "dealer": dealer})


def get_dealer_reviews(request, dealer_id):
    reviews = get_request("/fetchReviews/dealer/" + str(dealer_id))
    if not isinstance(reviews, list):
        return JsonResponse(
            {"status": 502, "message": "Unable to retrieve reviews"}, status=502
        )
    for review in reviews:
        result = analyze_review_sentiments(review.get("review", ""))
        review["sentiment"] = (
            result.get("sentiment", "unknown")
            if isinstance(result, dict) else "unknown"
        )
    return JsonResponse({"status": 200, "reviews": reviews})


# Create a `add_review` view to submit a review
def add_review(request):
    if not request.user.is_authenticated:
        return JsonResponse(
            {"status": 403, "message": "Unauthorized"}, status=403
        )
    if request.method != "POST":
        return JsonResponse(
            {"status": 405, "message": "Method not allowed"}, status=405
        )
    try:
        data = json.loads(request.body)
        required = ("name", "dealership", "review", "purchase", "purchase_date",
                    "car_make", "car_model", "car_year")
        if not isinstance(data, dict) or any(
            key not in data for key in required
        ):
            return JsonResponse(
                {"status": 400, "message": "Missing review fields"}, status=400
            )
    except (ValueError, TypeError):
        return JsonResponse(
            {"status": 400, "message": "Invalid JSON"}, status=400
        )

    response = post_review(data)
    if (not isinstance(response, dict) or "id" not in response
            or response.get("error")):
        return JsonResponse(
            {"status": 502, "message": "Error in posting review"}, status=502
        )
    return JsonResponse({
        "status": 200, "message": "Review posted successfully"
    })


def get_cars(request):
    if not CarModel.objects.exists():
        initiate()
    car_models = CarModel.objects.select_related('car_make').order_by('id')
    cars = [
        {"CarModel": car_model.name, "CarMake": car_model.car_make.name}
        for car_model in car_models
    ]
    return JsonResponse({"CarModels": cars})
