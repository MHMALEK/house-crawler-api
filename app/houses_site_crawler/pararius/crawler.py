from app.utils.scrapper import BaseCrawler
from .query_creator_service import generate_pararius_query

base_url = "https://www.pararius.com/"


class ParariusCrawler(BaseCrawler):
    def __init__(
        self,
        base_url=None,
        location=None,
        price_min=None,
        price_max=None,
        living_size=None,
        interior=None,
        use_browser=True,
    ):
        super().__init__(
            base_url=base_url or base_url, use_browser=use_browser
        )  # Call BaseCrawler's __init__
        self.base_url = base_url or base_url  # Default base URL
        self.location = location
        self.price_min = price_min
        self.price_max = price_max
        self.living_size = living_size
        self.interior = interior
        self.current_page = 1
        self.use_browser = use_browser

        print(self.price_max, self.price_min)

    def get_url(self, page):
        url_params = {
            "page": page,
            "price_min": self.price_min,
            "price_max": self.price_max,
            "living_size": self.living_size,
            "interior": self.interior,
        }

        print(
            "url_params",
            generate_pararius_query(
                base_url=self.base_url, location=self.location, **url_params
            ),
        )

        return generate_pararius_query(
            base_url=self.base_url, location=self.location, **url_params
        )  # Pass parameters to the function

    def extract_house_data(self, elements):
        extracted_data = []
        for house_element in elements:
            data = {}

            # Image URL
            image_element = house_element.find("img", class_="picture__image")
            data["image_url"] = image_element["src"] if image_element else None

            # Main URL
            main_url_element = house_element.find(
                "a", class_="listing-search-item__link--title"
            )
            data["main_url"] = main_url_element["href"] if main_url_element else None

            # Price
            price_element = house_element.find(
                "div", class_="listing-search-item__price"
            )
            data["price"] = price_element.text.strip() if price_element else None

            # Size
            size_element = house_element.find(
                "li", class_="illustrated-features__item--surface-area"
            )
            data["size"] = size_element.text.strip() if size_element else None

            # Number of rooms
            num_rooms_element = house_element.find(
                "li", class_="illustrated-features__item--number-of-rooms"
            )
            data["num_rooms"] = (
                num_rooms_element.text.strip() if num_rooms_element else None
            )

            # Interior
            interior_element = house_element.find(
                "li", class_="illustrated-features__item--interior"
            )
            data["interior"] = (
                interior_element.text.strip() if interior_element else None
            )

            # Agency
            agency_element = house_element.find("a", class_="listing-search-item__link")
            data["agency"] = agency_element.text.strip() if agency_element else None

            extracted_data.append(data)

        return extracted_data

    def process_page(self, soup):
        print("soup", soup)
        elements = soup.find_all(class_="search-list__item search-list__item--listing")
        print("asdas", elements)
        extracted_data = self.extract_house_data(elements)
        return extracted_data
