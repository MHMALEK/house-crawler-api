from bs4 import BeautifulSoup
import requests
import string
from fake_useragent import UserAgent
import time


available_to_book_code = 179
available_to_lottary_code = 336
base_url = "https://holland2stay.com/residences"

# If for any reason we could not fetch the city codes from the website, we can use this hard coded dictionary
city_codes_hard_coded = {
    "24": "Amsterdam",
    "320": "Arnhem",
    "619": "Capelle aan den IJssel",
    "26": "Delft",
    "28": "Den Bosch",
    "90": "Den Haag",
    "110": "Diemen",
    "620": "Dordrecht",
    "29": "Eindhoven",
    "545": "Groningen",
    "616": "Haarlem",
    "6099": "Helmond",
    "6209": "Maarssen",
    "6090": "Maastricht",
    "6217": "Nijmegen",
    "25": "Rotterdam",
    "6224": "Rijswijk",
    "6211": "Sittard",
    "6093": "Tilburg",
    "27": "Utrecht",
    "6051": "Nieuwegein",
    "6145": "Zeist",
    "6088": "Zoetermeer",
}

ua = UserAgent()
headers = {"User-Agent": str(ua.chrome)}


def fetch_city_names_service():
    return city_codes_hard_coded


def houses_site_crawler_service(available_to_lottary, city_code):

    response = requests.get(
        "https://holland2stay.com/residences?page=1&available_to_book[filter]=Available to book,179&city[filter]=Capelle aan den IJssel,619",
        headers=headers,
    )

    time_to_wait = 5

    time.sleep(time_to_wait)

    soup = BeautifulSoup(response.text, "html.parser")

    houses = soup.find_all("div", class_="residence_block")

    no_house_message = soup.find("div", class_="empty")

    data = []

    print(len(houses))


def fetch_all_cities_results(available_to_lottary, city_code_dic):
    results = []
    for city_code in city_code_dic:
        city_results = houses_site_crawler_service(available_to_lottary, city_code)
        results.append(
            {
                "city_name": city_code_dic[city_code],
                "city_code": city_code,
                "results": city_results,
            }
        )
    return results


def fetch_city_list_and_all_available_houses():
    city_code_dic = fetch_city_names_service()
    available_to_lottary = None  # enable this to also fetch houses available to lottary
    results = fetch_all_cities_results(available_to_lottary, city_code_dic)
    return results


def generateEmailBodyFromResult(cities_result):

    # Prepare the email body
    email_body = ""

    for city in cities_result:
        if city["results"] != "no house found":
            email_body += f"\n\nCity: {city['city_name']}\n"
            email_body += f"City Code: {city['city_code']}\n"
            email_body += "Houses found:\n"

            for house in city["results"]:
                house_info = string.Template(
                    """
                    House Name: ${name}
                    Price: ${price}
                    Available Date: ${available_date}
                    Services: ${services}
                    URL: ${url}
                    -----------------------------
                    """
                )

                email_body += house_info.substitute(house)

    return email_body


async def main():
    return ""
