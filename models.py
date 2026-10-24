from config import DEFAULT_THRESHOLD

Earthquake = dict
Filter = tuple
SearchResult = tuple
AppState = dict


def new_state() -> AppState:
    return {
        "loaded": False,
        "records": [],
        "filters": [],
        "threshold": DEFAULT_THRESHOLD,
        "ratings": {},
        "last_ids": set(),
        "last_output": None,
    }
