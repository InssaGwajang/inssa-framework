from typing import Final, List, Optional, Dict
from requests import request  # pip install requests
from fake_useragent import FakeUserAgent  # pip install fake_useragent
import datetime

from ..builtins.builtins import RAISE, PARAMS
from ..trace.Trace import Trace
from ..data.OrderedDictList import OrderedDictList
from ..interval.Interval import Interval


_TRACE: Final = Trace("KRX", group="Library")

_MARKETS: Final = {
    "KOSPI": "STK",
    "KOSDAQ": "KSQ",
}


class KRX:
    @staticmethod
    def markets() -> List[str]:
        return list(_MARKETS.keys())

    @staticmethod
    def codes(market: Optional[str] = None, *, active: Optional[bool] = None) -> List[str]:
        return KRX._assets().items(PARAMS(market=market, active=active)).values("code")

    @staticmethod
    def asset(code: str) -> Optional[Dict]:
        return KRX._assets().get(code)

    @staticmethod
    def assets(market: Optional[str] = None, *, active: Optional[bool] = None) -> OrderedDictList:
        return OrderedDictList(
            "code",
            [
                {
                    "market": asset["market"],
                    "code": asset["code"],
                    "name": asset["name"],
                    "active": asset["active"],
                }
                for asset in KRX._assets().items(PARAMS(market=market, active=active))
            ],
            name="KRX.assets"
            + (f".{market}" if market else "")
            + (f".active.{'o' if active else 'x'}" if active is not None else ""),
        )

    @staticmethod
    def market_quotations(
        market: Optional[str] = None,
        *,
        target: datetime.datetime = datetime.datetime.now(),
    ) -> OrderedDictList:
        markets = [market] if market else KRX.markets()
        target = target.strftime("%Y%m%d")
        return OrderedDictList(
            "code",
            [
                {
                    "code": quotation["ISU_SRT_CD"],
                    **KRX._quotation(quotation),
                }
                for market in markets
                for quotation in KRX._request(
                    {
                        "bld": "dbms/MDC/STAT/standard/MDCSTAT01501",
                        "mktId": _MARKETS[market],
                        "trdDd": target,
                    },
                    "OutBlock_1",
                )
                if KRX._valid(quotation)
            ],
            name=f"KRX.quotations.{'&'.join(markets)}.{target}",
        )

    @staticmethod
    def asset_quotations(
        code: Optional[str] = None,
        *,
        start: datetime.datetime = datetime.datetime(1900, 1, 1),
        end: datetime.datetime = datetime.datetime.now(),
    ) -> OrderedDictList:
        start, end = start.strftime("%Y%m%d"), end.strftime("%Y%m%d")
        return OrderedDictList(
            "datetime",
            [
                {
                    "datetime": datetime.datetime.strptime(quotation["TRD_DD"], "%Y/%m/%d"),
                    **KRX._quotation(quotation),
                }
                for quotation in KRX._request(
                    {
                        "bld": "dbms/MDC/STAT/standard/MDCSTAT01701",
                        "isuCd": KRX._assets().get(code)["id"],
                        "strtDd": start,
                        "endDd": end,
                    },
                    "output",
                )
                if KRX._valid(quotation)
            ],
            name=f"KRX.quotations.{code}.start.{start}.end.{end}",
        )

    @staticmethod
    def _valid(quotation: Dict) -> bool:
        return quotation and all(
            [
                quotation[key] and quotation[key] != "0"
                for key in ("TDD_OPNPRC", "TDD_HGPRC", "TDD_LWPRC", "TDD_CLSPRC", "ACC_TRDVOL")
            ]
        )

    @staticmethod
    def _quotation(quotation: Dict) -> Dict:
        return {
            trans: int(quotation[key].replace(",", ""))
            for key, trans in {
                "TDD_OPNPRC": "open",
                "TDD_HGPRC": "high",
                "TDD_LWPRC": "low",
                "TDD_CLSPRC": "close",
                "ACC_TRDVOL": "volume",
                "ACC_TRDVAL": "expense",
                "MKTCAP": "capitalization",
            }.items()
        }

    @staticmethod
    def _assets() -> OrderedDictList:
        not hasattr(KRX, "_assets_") and setattr(
            KRX,
            "_assets_",
            OrderedDictList(
                "code",
                [
                    {
                        "market": market,
                        "code": asset["short_code"],
                        "name": asset["codeName"],
                        "active": active,
                        "id": asset["full_code"],
                    }
                    for market, code in _MARKETS.items()
                    for bld, active in {
                        "dbms/comm/finder/finder_stkisu": True,
                        "dbms/comm/finder/finder_listdelisu": False,
                    }.items()
                    for asset in KRX._request({"bld": bld, "mktsel": code, "typeNo": 0}, "block1")
                ],
                name="KRX.assets",
            ),
        )
        return KRX._assets_

    @staticmethod
    def _request(data: Dict, target: str) -> Dict:
        method = "POST"
        url = "http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd"

        not hasattr(KRX, "_intervals") and setattr(KRX, "_intervals", Interval(0.5, name="KRX"))
        KRX._intervals.leave()

        not hasattr(KRX, "_fake_user_agent") and setattr(
            KRX, "_fake_user_agent", FakeUserAgent(verify_ssl=False)
        )
        while "Android" not in (user_agent := KRX._fake_user_agent.random):
            pass

        response = request(method, url, headers={"User-Agent": user_agent}, data=data)
        (
            response.status_code != 200
            and _TRACE.CRITICAL(
                message := (
                    f"request failed, {method} "
                    + f"from {url} with {data} returns {response.status_code}"
                )
            )
            and RAISE(ValueError, message)
        )
        data = response.json()[target]
        _TRACE.DEBUG(f"request {url} respond {len(data)} {target} data")

        return data
