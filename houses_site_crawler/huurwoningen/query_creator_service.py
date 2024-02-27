from urllib.parse import urlencode

interior_type = {
    "furnished": "gestoffeerd",
    "unfurnished": "kaal",
    "bald": "kaal",  # Map "bald" to the same as "uninterior_type"
}


def generate_huurwoningen_query(
    base_url="https://www.huurwoningen.com/",
    location="",
    page=1,
    num_rooms=None,
    living_size=None,
    price_min=None,
    price_max=None,
    interior=None,
    api_key=False,
):
    """Generates a query URL for searching huurwoningen.com.

    Args:
        base_url (str, optional): The base URL of huurwoningen.com. Defaults to https://www.huurwoningen.com/.
        location (str): The desired location for the search.
        num_rooms (int, optional): The number of rooms (must be a string like "1").
        living_size (int, optional): The minimum apartment living_size in sqm (must be a string like "25").
        price_min (int, optional): The minimum price (must be a string like "200").
        price_max (int, optional): The maximum price (must be a string like "6000").
        interior (bool, optional): Whether to search for interior apartments (must be a string like "True" or "False").
        api_key (bool, optional): Whether to skip adding the API key (for testing purposes). Defaults to False.

    Returns:
        str: The generated query URL.

    Raises:
        ValueError: If a required parameter is missing or has an invalid type.
    """

    if not location:
        raise ValueError("Location is required.")

    # Validate data types and convert to strings for huurwoningen.com formatting
    try:
        num_rooms = str(num_rooms) if num_rooms else None
        living_size = str(living_size) if living_size else None
        price_min = str(price_min) if price_min else None
        price_max = str(price_max) if price_max else None
        interior = str(interior).lower() if interior else None  # Convert to lowercase

        # Additional validations specific to huurwoningen.com parameters (if needed)
    except ValueError:
        raise ValueError(
            "Invalid data types: num_rooms (str), living_size (str), price_min/max (str), interior (str)."
        )

    # Construct the query URL based on huurwoningen.com's URL structure:
    query_url = base_url + "in/" + location + "/"

    query_params = {}
    if num_rooms:
        query_params["bedrooms"] = num_rooms
    if living_size:
        query_params["living_living_size"] = living_size
    if price_min:
        query_params["price"] = f"{price_min}-{price_max}" if price_max else price_min
    if interior:
        query_params["interior"] = interior_type.get(interior, None)
    if page:
        query_params["page"] = page

    # Add query parameters (skip API key if specified)
    if api_key:
        # Insert your API key here:
        query_params["api_key"] = "<YOUR_API_KEY>"  # Placeholder for your API key

    query_url += "?" + urlencode(query_params)

    return query_url
