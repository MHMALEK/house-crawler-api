from urllib.parse import urlencode

interior_type = {
    "furnished": "gestoffeerd",
    "unfurnished": "kaal",
    "bald": "kaal",  # Map "bald" to the same as "uninterior_type"
}


def generate_pararius_query(
    base_url="https://www.pararius.com/",
    location="",
    page=1,
    num_rooms=None,
    living_size=None,
    price_min=None,
    price_max=None,
    interior=None,
    api_key=None,
):
    """Generates a query URL for searching pararius.com.

    Args:
        base_url (str, optional): The base URL of pararius.com. Defaults to https://www.pararius.com/.
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

    # Validate data types and convert to strings for pararius.com formatting
    try:
        num_rooms = str(num_rooms) if num_rooms else None
        living_size = str(living_size) if living_size else None
        price_min = str(price_min) if price_min else None
        price_max = str(price_max) if price_max else None
        interior = str(interior).lower() if interior else None  # Convert to lowercase

        # Additional validations specific to pararius.com parameters (if needed)
    except ValueError:
        raise ValueError(
            "Invalid data types: num_rooms (str), living_size (str), price_min/max (str), interior (str)."
        )

    query_url = base_url + "apartments/" + location + "/"

    print(price_min, price_max)

    # Add the price range to the URL
    if price_min and price_max:
        query_url += f"{price_min}-{price_max}/"
    elif price_min:
        query_url += f"{price_min}-6000/"
    elif price_max:
        query_url += f"300-{price_max}/"

    # Add the number of bedrooms to the URL
    if num_rooms:
        query_url += f"{num_rooms}/"

    # Add the interior type to the URL
    if interior:
        query_url += f"{interior}/"

    # Add the living size to the URL
    if living_size:
        query_url += f"{living_size}m2/"

    # Add the page to the URL
    if page:
        query_url += f"page-{page}/"

    # Add the API key to the URL (if it is not to be skipped)
    if api_key:
        # Insert your API key here:
        query_url += "?api_key=" + "<YOUR_API_KEY>"  # Placeholder for your API key

    return query_url
