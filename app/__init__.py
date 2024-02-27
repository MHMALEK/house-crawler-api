from flask import jsonify
from app.main import create_app
from app.firebase import init_firebase
from fake_useragent import UserAgent


import app.houses_site_crawler.funda.service as funda_service

init_firebase()

ua = UserAgent()
headers = {"User-Agent": str(ua.chrome)}

app = create_app()

app.route("/")(
    lambda: "This is a REST API for getting houses data from rental company websites. Docs and more info: https://github.com/MHMALEK/holland-houses-crawler-api"
)


@app.route("/test")
def get_data():
    data = funda_service.crawl_funda(
        location="amsterdam",
        price_min=300,
        price_max=4000,
        living_size=200,
        interior="gemeubileerd",
    )

    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
