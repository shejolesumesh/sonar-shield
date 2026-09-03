"""GPS validation helpers - never invent coordinates."""
import math


def is_valid_gps(lat, lon) -> bool:
    if lat is None or lon is None:
        return False
    if isinstance(lat, float) and math.isnan(lat):
        return False
    return -90.0 <= lat <= 90.0 and -180.0 <= lon <= 180.0


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))
