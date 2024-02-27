from app.houses_site_crawler.pararius.service import crawl_pararius

search_params = {
    "location": "amsterdam",
    "price_min": 500,
    "price_max": 1500,
    "living_size": 25,
    "interior": "shell",
}

extracted_data = crawl_pararius(**search_params)

print(extracted_data)