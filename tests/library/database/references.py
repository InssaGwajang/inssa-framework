from copy import deepcopy
from datetime import datetime


def members():
    return deepcopy(
        [
            {"id": "izd842jk", "name": "Theodore", "email": "theodore@email.com"},
            {"id": "hlk4sxtg", "name": "Justin", "email": "justin@email.com"},
            {"id": "atk4ahtj", "name": "Chris", "email": "chris@email.com"},
            {"id": "bd8zriu8", "name": "Christin", "email": "christin@email.com"},
            {"id": "8gbedsz3", "name": "Grace", "email": "grace@email.com"},
        ]
    )


def candles():
    return deepcopy(
        [
            {"datetime": datetime(2020, 1, 1), "close": 5000, "high": 5600},
            {"datetime": datetime(2020, 2, 1), "close": 6500, "high": 6600},
            {"datetime": datetime(2020, 3, 1), "close": 6000, "high": 6200},
            {"datetime": datetime(2020, 4, 1), "close": 7000, "high": 7400},
            {"datetime": datetime(2020, 5, 1), "close": 8000, "high": 8100},
            {"datetime": datetime(2020, 6, 1), "close": 6800, "high": 6900},
        ]
    )


def half_day_candles():
    return deepcopy(
        [
            {"datetime": datetime(2020, 1, 1, 00), "close": 5000, "high": 5200, "low": 4700},
            {"datetime": datetime(2020, 1, 1, 12), "close": 6200, "high": 6400, "low": 5200},
            {"datetime": datetime(2020, 2, 1, 00), "close": 6500, "high": 6500, "low": 6400},
            {"datetime": datetime(2020, 2, 1, 12), "close": 6100, "high": 6100, "low": 5900},
            {"datetime": datetime(2020, 3, 1, 00), "close": 6000, "high": 6100, "low": 5900},
        ]
    )
