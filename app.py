from flask import Flask
from create_app import create_app
from firebase import init_firebase

init_firebase()

app = create_app()

app.route("/")(lambda: "This is a REST API for getting houses data from rental company websites. Docs and more info: https://github.com/MHMALEK/holland-houses-crawler-api")

if __name__ == "__main__":
    app.run()
