from urllib.parse import urlencode

interior_type = {
    "furnished": "gestoffeerd",
    "unfurnished": "kaal",
    "bald": "kaal",  # Map "bald" to the same as "uninterior_type"
}


def generate_funda_query(
    base_url="https://www.funda.nl/zoeken/huur",
    location="",
    price_min=None,
    price_max=None,
    num_rooms=None,
    living_size=None,
    availability=["available"],
    page=1,
    interior=None,
):
    """Generates a query URL for searching funda.nl.

    Args:
        base_url (str, optional): The base URL of funda.nl. Defaults to "https://www.funda.nl/zoeken/huur".
        location (str): The desired location for the search.
        price_min (int, optional): The minimum price.
        price_max (int, optional): The maximum price.
        num_rooms (int, optional): The number of rooms.
        living_size (int, optional): The minimum living_size in sqm.
        availability (list, optional): The availability options.

    Returns:
        str: The generated query URL.

    Raises:
        ValueError: If a required parameter is missing or has an invalid type.
    """

    if not location:
        raise ValueError("Location is required.")

    # Validate data types and convert to strings for funda.nl formatting
    try:
        price_min = str(price_min) if price_min else None
        price_max = str(price_max) if price_max else None
        num_rooms = str(num_rooms) if num_rooms else None
        living_size = str(living_size) if living_size else None
        # The availability parameter is expected to be a list of strings
        if availability and not all(isinstance(a, str) for a in availability):
            raise ValueError("Invalid data type: availability (list of str).")
    except ValueError:
        raise ValueError(
            "Invalid data types: price_min/max (str), num_rooms (str), living_size (str), availability (list of str)."
        )
    query_parameters = []

    # Add the location to the parameters
    query_parameters.append(f"selected_area=%5B%22{location}%22%5D")

    # Add the price range to the parameters
    if price_min and price_max:
        query_parameters.append(f"price=%22{price_min}-{price_max}%22")
    elif price_min:
        query_parameters.append(f"price=%22{price_min}-6000%22")
    elif price_max:
        query_parameters.append(f"price=%22300-{price_max}%22")

    # Add the number of rooms to the parameters
    if num_rooms:
        query_parameters.append(f"rooms=%22{num_rooms}-%22")

    # Add the living size to the parameters
    if living_size:
        query_parameters.append(f"floor_area=%22-{living_size}%22")

    # Add the availability to the parameters
    if availability:
        availability_str = ",".join(f"%22{a}%22" for a in availability)
        query_parameters.append(f"availability=%5B{availability_str}%5D")

    return base_url + "?" + "&".join(query_parameters)
