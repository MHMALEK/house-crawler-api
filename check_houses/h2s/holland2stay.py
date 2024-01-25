from flask import (
    Blueprint,
    request
)


from .services import fetch_city_names_service, check_houses_service, fetch_city_list_and_all_available_houses, generateEmailBodyFromResult

from email_bot import service as email_services

import logging

bp = Blueprint("holland2stay", __name__, url_prefix="/h2s")


@bp.route("/city_names", methods=["GET"])
def fetch_city_names():
    response = fetch_city_names_service()
    return response


@bp.route("/check_houses", methods=["GET"])
def check_houses():
    city_code = request.args.get('city_code')
    available_to_lottary = request.args.get('available_to_lottary')
    city_codes = fetch_city_names_service()
    
     # If city is not in city_codes, return an error
    if city_code not in city_codes:
        return f"No city found with name {city_codes[city_code]}.", 404 
    response = check_houses_service(available_to_lottary, city_code)
    return response
   

@bp.route("/list/all", methods=["GET"])
def list_all():
    response = fetch_city_list_and_all_available_houses()
    body = generateEmailBodyFromResult(response)
        
    return {"list": response, "text": body}