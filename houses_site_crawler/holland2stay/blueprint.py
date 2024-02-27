from flask import Blueprint, request


from .services import (
    fetch_city_names_service,
    houses_site_crawler_service,
    fetch_city_list_and_all_available_houses,
    generateEmailBodyFromResult,
)


bp = Blueprint("holland2stay", __name__, url_prefix="/holland2stay")


@bp.route("/city_names", methods=["GET"])
def fetch_city_names():
    response = fetch_city_names_service()
    return response


@bp.route("/houses_site_crawler", methods=["GET"])
def houses_site_crawler():
    city_code = request.args.get("city_code")
    available_to_lottary = request.args.get("available_to_lottary")
    city_codes = fetch_city_names_service()

    # # If city is not in city_codes, return an error
    # if city_code not in city_codes:
    #     return f"No city found with name {city_codes[city_code]}.", 404
    response = houses_site_crawler_service(available_to_lottary, city_code)
    print(response)
    return response


@bp.route("/list/all", methods=["GET"])
def list_all():
    response = fetch_city_list_and_all_available_houses()
    body = generateEmailBodyFromResult(response)

    return {"list": response, "text": body}
