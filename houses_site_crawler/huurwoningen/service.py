from .crawler import HuurwoningenCrawler

base_url = "https://www.huurwoningen.com/"
def crawl_huurwoningen(location, price_min, price_max, living_size, interior):
    """
    Crawls huurwoningen.com with specified parameters and returns extracted data.

    Args:
        location (str): Desired location for search.
        price_min (int, optional): Minimum price (inclusive).
        price_max (int, optional): Maximum price (inclusive).
        living_size (int, optional): Minimum living size in sqm.
        interior (str, optional): Desired interior type (e.g., "gemeubileerd").

    Returns:
        list: Extracted data from the crawled pages.
    """

    crawler = HuurwoningenCrawler(
        base_url=base_url,
        location=location,
        price_min=price_min,
        price_max=price_max,
        living_size=living_size,
        interior=interior,
    )
    results = crawler.crawl()
    return results
