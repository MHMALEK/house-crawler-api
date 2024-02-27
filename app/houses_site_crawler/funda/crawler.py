from app.utils.scrapper import BaseCrawler
from .query_creator_service import generate_funda_query

base_url = "https://www.funda.nl/zoeken/huur"


class FundaCrawler(BaseCrawler):
    def __init__(
        self,
        base_url=None,
        location=None,
        price_min=None,
        price_max=None,
        living_size=None,
        interior=None,
        use_browser=False,
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
            generate_funda_query(
                base_url=self.base_url, location=self.location, **url_params
            ),
        )

        return generate_funda_query(
            base_url=self.base_url, location=self.location, **url_params
        )  # Pass parameters to the function

    def extract_house_data(self, elements):
        extracted_data = []

        for house_element in elements:
            data = {}

            # Image URL
            image_element = house_element.find("img")
            data["image_url"] = image_element["srcset"] if image_element else None

            # Main URL
            main_url_element = house_element.find(
                "a", {"data-test-id": "object-image-link"}
            )
            data["main_url"] = main_url_element["href"] if main_url_element else None

            # Price
            price_element = house_element.find("p", {"data-test-id": "price-rent"})
            data["price"] = price_element.text.strip() if price_element else None

            # Size
            size_element = house_element.find(
                "li", {"class": "mr-4 flex flex-[0_0_auto]"}
            )
            data["size"] = size_element.text.strip() if size_element else None

            # Info
            info = {}
            num_rooms_element = house_element.find(
                "li", {"class": "mr-4 flex flex-[0_0_auto]"}
            )
            info["num_rooms"] = (
                num_rooms_element.text.strip() if num_rooms_element else None
            )

            # Energy label
            energy_label_element = house_element.find(
                "li", {"class": "flex flex-[0_0_auto]"}
            )
            info["energy_label"] = (
                energy_label_element.text.strip() if energy_label_element else None
            )

            data["info"] = info

            extracted_data.append(data)

        return extracted_data

    def process_page(self, soup):
        # print(soup)
        elements = soup.find_all("div", {"data-test-id": "search-result-item"})
        print("elements", len(elements))
        extracted_data = self.extract_house_data(elements)
        return extracted_data
