from .crawler import ParariusCrawler

base_url = "https://www.pararius.com/"


def crawl_pararius(location, price_min, price_max, living_size, interior):
    """
    Crawls pararius.com with specified parameters and returns extracted data.

    Args:
        location (str): Desired location for search.
        price_min (int, optional): Minimum price (inclusive).
        price_max (int, optional): Maximum price (inclusive).
        living_size (int, optional): Minimum living size in sqm.
        interior (str, optional): Desired interior type (e.g., "gemeubileerd").

    Returns:
        list: Extracted data from the crawled pages.
    """

    print(
        123,
        price_min,
        price_max,
    )

    crawler = ParariusCrawler(
        base_url=base_url,
        location=location,
        price_min=price_min,
        price_max=price_max,
        living_size=living_size,
        interior=interior,
        use_browser=True,
        
    )
    results = crawler.crawl()
    return results
