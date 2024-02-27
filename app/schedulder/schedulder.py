import schedule
import time
from ...houses_site_crawler.holland2stay.services import fetch_all_cities_results, fetch_city_names_service



def scheduled_job_to_fetch_city_list_and_send_it_to_email():
    city_code_dic = fetch_city_names_service()
    available_to_lottary = None  #enable this to also fetch houses available to lottary
    results = fetch_all_cities_results(available_to_lottary, city_code_dic)
    
    
schedule.every().day.at("10:30").do(scheduled_job_to_fetch_city_list_and_send_it_to_email)

while True:
    schedule.run_pending()
    time.sleep(1)