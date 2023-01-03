from OSMPythonTools.nominatim import Nominatim
import pandas as pd


def osm_find_location(latitude: float, longitude: float) -> tuple[str, str]:
    """
    Returns a voivedeship (state) name and city/town/municipality name for a given latitude and longitude input.\n
    This function uses OpenStreetMap Nominatim API to perfom reverse query on the supplied coordinates.\n
    Checked only for values confined to the area of Poland, but should work reasonably well for the rest of the world.

    Args:
        latitude (float): latitude coordinate (north-south position of a point)
        longitude (float): longitude coordinate (east-west position of a point)

    Returns:
        tuple[str, str]: tuple of voivodeship (state) and city names
    """

    nominatim = Nominatim()

    query = nominatim.query(latitude, longitude, reverse=True, zoom=10)
    address = query.toJSON()[0]["address"]
    state = address["state"]
    state_name = state.split(" ")[-1]

    try:
        location = address["city"]
    except KeyError:
        try:
            location = address["town"]
        except KeyError:
            try:
                location = address["municipality"]
            except KeyError:
                location = None

    return state_name, location


def split_coordinates(row: pd.Series) -> pd.Series:
    """Splits the coordinates column into latidute and longitude columns.

    Args:
        row (pd.Series): current row

    Returns:
        pd.Series: current row
    """

    longitude, latitude = row["coordinates"]
    row["latitude"] = latitude
    row["longitude"] = longitude

    return row


def assign_state_city(row: pd.Series) -> pd.Series:
    """_summary_
    Helper function to create two rows: state and location and be used with pandas apply function.

    Args:
        row (pd.Series): current pd.DataFrame row


    Returns:
        pd.Series: pd.DataFrame row with two new rows
    """

    state, location = osm_find_location(row["latitude"], row["longitude"])

    row["state"] = state
    row["location"] = location

    return row
