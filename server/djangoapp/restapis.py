import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    params = dict()
    params["text"] = kwargs["text"]
    params["version"] = kwargs["version"]
    params["features"] = kwargs["features"]
    params["return_analyzed_text"] = kwargs["return_analyzed_text"]
    params["dealerId"] = kwargs["dealerId"]
    try:
        if api_key:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=params, auth=HTTPBasicAuth('apikey', api_key))
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=params)
    except:
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    return requests.post(url, params=kwargs, json=json_payload)

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(url, dealerId):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url,  dealerId=dealerId)
    if json_result:
        # Get the row list in JSON as dealers
        reviews = json_result["rows"]
        # For each dealer object
        for review in reviews:
            # Get its content in `doc` object
            review_obj = review["doc"]
            # Create a CarDealer object with values in `doc` object
            review_obj = DealerReview(dealership=dealer_doc["dealership"], name=dealer_doc["name"], purchase=dealer_doc["purchase"],
                                   review=dealer_doc["review"], purchase_date=dealer_doc["purchase_date"], car_make=dealer_doc["car_make"],
                                   car_model=dealer_doc["car_model"],
                                   car_year=dealer_doc["car_year"], id=dealer_doc["id"])
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)

            results.append(review_obj)
    return render(request, 'djangoapp/dealer_details.html', results)

# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_by_id_from_cf(url, dealerId):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url,  dealerId=dealerId)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(dealerreview):
    url = "https://api.us-east.natural-language-understanding.watson.cloud.ibm.com/instances/2535d66e-b637-4748-b099-862c281558b8/v1/analyze?version=2023-10-25"
    sentiment_req = dict()
    sentiment_req["text"] = dealerreview
    sentiment_req["features"]["sentiment"]["targets"] = ["positive", "neutral", "negative"]
    sentiment_req["features"]["keywords"] = {"emotion": true}
    
    return post_request(url, sentiment_req)


