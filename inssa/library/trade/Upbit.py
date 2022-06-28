from typing import Final, List, Any, Optional, Dict, Tuple
from requests import request  # pip install requests
from dateutil.relativedelta import relativedelta  # pip install python-dateutil
import datetime

from ..builtins.builtins import PARAMS, RAISE
from ..trace.Trace import Trace
from ..data.OrderedDictList import OrderedDictList
from ..interval.Intervals import Intervals


_TRACE: Final = Trace("Upbit", group="Library")


class Upbit:
    @staticmethod
    def markets() -> List[str]:
        return Upbit._markets().values()

    @staticmethod
    def candles(
        market: str,
        period: str = "day",  # month, week, day, minute
        interval: Optional[int] = None,  # for minutes, 1, 3, 5, 10, 15, 30, 60, 240
        *,
        start: Optional[datetime.datetime] = None,
        end: Optional[datetime.datetime] = None,
    ) -> OrderedDictList:
        url = (
            "https://api.upbit.com/v1/candles/"
            + f"{period}s"
            + (f"/{interval}" if period == "minute" else "")
        )
        params = PARAMS(
            market=market,
            count=200,
            to=(
                datetime.datetime.strftime(end - datetime.timedelta(hours=9), "%Y-%m-%d %H:%M:%S")
                if end
                else None
            ),
        )

        candles = []
        while (response := Upbit._request(url, params=params))[0]:
            response_candles = [Upbit._candle(quotation) for quotation in response[0]]
            if start and len(response_candles) != len(
                (
                    filtered_candles := [
                        candle for candle in response_candles if candle["datetime"] >= start
                    ]
                )
            ):
                candles.extend(filtered_candles)
                break

            candles.extend(response_candles)

            params["to"] = datetime.datetime.strftime(
                candles[-1]["datetime"] - datetime.timedelta(hours=9), "%Y-%m-%d %H:%M:%S"
            )

        candles.reverse()
        if (
            candles
            and (interval := interval if interval else 1)
            and candles[-1]["datetime"]
            > (
                response[1]  # valid_datetime
                - (
                    datetime.timedelta(days=interval)
                    if period == "day"
                    else datetime.timedelta(minutes=interval)
                    if period == "minute"
                    else datetime.timedelta(weeks=interval)
                    if period == "week"
                    else relativedelta(months=interval)
                )
            )
        ):
            candles.pop()

        return OrderedDictList(
            "datetime",
            [candle for candle in candles if Upbit._valid(candle)],
            name=f"Upbit.candles.{market}.{period}.{interval}"
            + (f".start.{start.strftime('%Y/%m/%d %H:%M:%S')}" if start else "")
            + (f".end.{end.strftime('%Y/%m/%d %H:%M:%S')}" if end else ""),
        )

    @staticmethod
    def _candle(quotation: Dict) -> Dict:
        return {
            "datetime": datetime.datetime.strptime(
                quotation["candle_date_time_kst"],
                "%Y-%m-%dT%H:%M:%S",
            ),
            "open": quotation["opening_price"],
            "high": quotation["high_price"],
            "low": quotation["low_price"],
            "close": quotation["trade_price"],
            "volume": quotation["candle_acc_trade_volume"],
        }

    @staticmethod
    def _valid(candle: Dict) -> bool:
        return candle and all([candle[key] for key in ("open", "high", "low", "close", "volume")])

    @staticmethod
    def _markets() -> OrderedDictList:
        not hasattr(Upbit, "_markets_") and setattr(
            Upbit,
            "_markets_",
            OrderedDictList(
                "market",
                [
                    {
                        "market": market["market"],
                        "name": market["english_name"],
                        "korean": market["korean_name"],
                    }
                    for market in Upbit._request("https://api.upbit.com/v1/market/all")[0]
                ],
                name="Upbit.markets",
            ),
        )
        return Upbit._markets_

    @staticmethod
    def _request(
        url: str,
        *,
        method: str = "GET",  # GET, POST, DELETE
        params: Optional[Dict] = None,
        # keys: Optional[Tuple] = None,  # TODO: for authorization
    ) -> (Any, datetime.datetime):
        not hasattr(Upbit, "_intervals") and setattr(
            Upbit, "_intervals", Intervals({1: 9, 60: 599}, name="Upbit")
        )
        Upbit._intervals.leave()

        response = request(method, url, params=params)
        (
            response.status_code != 200
            and _TRACE.CRITICAL(
                message := (
                    f"request failed, {method} "
                    + f"from {url} with {params} returns {response.status_code}"
                )
            )
            and RAISE(ValueError, message)
        )
        data = response.json()
        server = datetime.datetime.strptime(  # KST
            response.headers["Date"],
            "%a, %d %b %Y %H:%M:%S GMT",
        ) + datetime.timedelta(hours=9)
        _TRACE.DEBUG(
            f"request {url} respond {len(data)} data",
            f"and server time is {server.strftime('%Y/%m/%d %H:%M:%S')}",
        )

        return (data, server)
