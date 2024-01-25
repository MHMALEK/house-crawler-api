from flask import (
    Blueprint,
    request
)
from bs4 import BeautifulSoup
import requests
import logging
import json
import string
from fake_useragent import UserAgent



available_to_book_code = 179
available_to_lottary_code = 336
base_url = "https://holland2stay.com/residences.html"

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
    "6088": "Zoetermeer"
}

ua = UserAgent()
headers = {'User-Agent':str(ua.chrome)}

def fetch_city_names_service():
    
    response = requests.get(base_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')



    city_dropdown = soup.find('select', class_='s-city') 
    city_options = city_dropdown.find_all('option')

    cities = {option.get('value'): option.text for option in city_options if option.get('value') != ''}
    return cities


def check_houses_service(available_to_lottary, city_code):
   
    # If available_to_lottary is None, do not include it in the request
    if available_to_lottary is None:
        response = requests.get(f"{base_url}?available_to_book={available_to_book_code}&city={city_code}", headers=headers)
    else:
        response = requests.get(f"{base_url}?available_to_book={available_to_lottary},{available_to_book_code}&city={city_code}", headers=headers)
        

    soup = BeautifulSoup(response.text, "html.parser")
    houses = soup.find_all('div', class_='regi-item')
    no_house_message = soup.find("div", class_="empty")

    data = []

    def has_calendar_icon(tag):
        return tag.name == 'li' and tag.find('i', class_='fas fa-calendar')

    def has_map_icon(tag):
        return tag.name == 'li' and tag.find('i', class_='fas fa-map-marker-alt')

    for item in houses:
        name_element = item.find('h4', class_='regularbold')
        name = name_element.text.strip() if name_element else None

        available_date_element = item.find(has_calendar_icon)
        available_date = available_date_element.find('strong').text.strip().replace('Available from ', '') if available_date_element else None

        price_element = item.find('div', class_='price regularbold')
        price = price_element.text.strip().replace('\u20ac', '') if price_element else None

        city_element = item.find(has_map_icon)
        city = city_element.text.strip() if city_element else None

        url = item.get('data-url', None)
        services = [li.text for li in item.find_all('li') if li.text]

        data.append({
            'name': name,
            'available_date': available_date,
            'price': price,
            'city': city,
            'url': url,
            'services': services
        })

    if no_house_message:
        return "no house found"
    else:
        return data
    
    
def fetch_all_cities_results(available_to_lottary, city_code_dic):
    results = []
    for city_code in city_code_dic:
        city_results = check_houses_service(available_to_lottary, city_code)
        results.append({
            'city_name': city_code_dic[city_code], 
            'city_code': city_code,
            'results': city_results
        })
    return results



def fetch_city_list_and_all_available_houses():
    city_code_dic = fetch_city_names_service()
    available_to_lottary = None  #enable this to also fetch houses available to lottary
    results = fetch_all_cities_results(available_to_lottary, city_code_dic)
    return results

def generateEmailBodyFromResult(cities_result):
    
    
    # Prepare the email body
    email_body = ''

    for city in cities_result:
        if city['results'] != "no house found":
            email_body += f"\n\nCity: {city['city_name']}\n"
            email_body += f"City Code: {city['city_code']}\n"
            email_body += "Houses found:\n"

            for house in city['results']:
                house_info = string.Template("""
                    House Name: ${name}
                    Price: ${price}
                    Available Date: ${available_date}
                    Services: ${services}
                    URL: ${url}
                    -----------------------------
                    """)

                email_body += house_info.substitute(house)

    return email_body
