DEFAULT_THRESHOLD = 0.8
RESULT_LIMIT = 10

FIELD_TYPES = {
    "id": str,
    "title": str,
    "kind": str,
    "network": str,
    "time": str,
    "magnitude": float,
    "depth_km": float,
    "latitude": float,
    "longitude": float,
    "reviewed": bool,
    "url": str,
}

SEARCH_FIELDS = ("id", "title", "kind", "network", "time", "url")

FILTER_OPERATORS = {
    str: ("eq", "ne", "contains"),
    float: ("eq", "ne", "lt", "le", "gt", "ge"),
    bool: ("eq", "ne"),
}
