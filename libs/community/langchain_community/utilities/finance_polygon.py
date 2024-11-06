"""
Util that calls several of Polygon's REST APIs.
Docs: https://polygon.io/docs/stocks/getting-started
"""

import json
from typing import Any, Dict, Optional

import requests
from langchain_core.utils import get_from_dict_or_env
from pydantic import BaseModel, model_validator

POLYGON_BASE_URL = "https://api.polygon.io/"


class FinancePolygonAPIWrapper(BaseModel):
    """Wrapper for Polygon Finance API."""

    polygon_api_key: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def validate_environment(cls, values: Dict) -> Any:
        """Validate that api key in environment."""
        polygon_api_key = get_from_dict_or_env(
            values, "polygon_api_key", "POLYGON_API_KEY"
        )
        values["polygon_api_key"] = polygon_api_key

        return values

    def get_crypto_aggregates(self, ticker: str, **kwargs: Any) -> Optional[dict]:
        """
        Get aggregate bars for a cryptocurrency over a given date range
        in custom time window sizes.

        /v2/aggs/ticker/{cryptoTicker}/range/{multiplier}/{timespan}/{from}/{to}
        """
        timespan = kwargs.get("timespan", "day")
        multiplier = kwargs.get("timespan_multiplier", 1)
        from_date = kwargs.get("from_date", None)
        to_date = kwargs.get("to_date", None)
        adjusted = kwargs.get("adjusted", True)
        sort = kwargs.get("sort", "asc")

        url = (
            f"{POLYGON_BASE_URL}v2/aggs"
            f"/ticker/{ticker}"
            f"/range/{multiplier}"
            f"/{timespan}"
            f"/{from_date}"
            f"/{to_date}"
            f"?apiKey={self.polygon_api_key}"
            f"&adjusted={adjusted}"
            f"&sort={sort}"
        )
        response = requests.get(url)
        data = response.json()

        status = data.get("status", None)
        if status not in ("OK"):
            raise ValueError(f"API Error: {data}")

        return data.get("results", None)
    
    def get_ipos(self, **kwargs: Any) -> Optional[dict]:
        """
        Get IPOs for a specific ticker or other criteria.
        
        /vX/reference/ipos?limit={limit}&apiKey={apiKey}
        """
        ticker = kwargs.get("ticker", None)
        us_code = kwargs.get("us_code", None)
        isin = kwargs.get("isin", None)
        listing_date = kwargs.get("listing_date", None)
        ipo_status = kwargs.get("ipo_status", None)
        order = kwargs.get("order", "asc")
        limit = kwargs.get("limit", 10)
        sort = kwargs.get("sort", "listing_date")

        url = POLYGON_BASE_URL

        if ticker is not None:
            url = url +"vX/reference/ipos?" + f"ticker={ticker}&"
        
        if us_code is not None:
            url = url + f"us_code={us_code}&"
        
        if isin is not None:
            url = url + f"isin={isin}&"
        
        if listing_date is not None:
            url = url + f"listing_date={listing_date}&"
        
        if ipo_status is not None:
            url = url + f"ipo_status={ipo_status}&"
        
        url = url + f"order={order}&limit={limit}&sort={sort}&apiKey={self.polygon_api_key}"
        
        response = requests.get(url)
        data = response.json()

        status = data.get("status", None)
        if status not in ("OK"):
            raise ValueError(f"API Error: {data}")

        return data.get("results", None)
    
    def get_related_companies(self, ticker: str) -> Optional[dict]:
        """
        Get a list of tickers related to the queried ticker based on News
        and Returns data.

        /v1/related-companies/{ticker}?apiKey={apiKey}
        """

        url = (
            f"{POLYGON_BASE_URL}v1/related-companies"
            f"/{ticker}"
            f"?apiKey={self.polygon_api_key}"
        )
        response = requests.get(url)
        data = response.json()

        status = data.get("status", None)
        if status not in ("OK"):
            raise ValueError(f"API Error: {data}")

        return data.get("results", None)
    

    def get_exchanges(self, **kwagrs: Any) -> Optional[dict]:
        """
        Get a list of exchanges that Polygon.io knows about.

        v3/reference/exchanges?asset_class={asset_class}&apiKey={apiKey}
        """
        
        asset_class = kwagrs.get("asset_class", "stocks")
        locale = kwagrs.get("locale", None)

        url = POLYGON_BASE_URL + "v3/reference/exchanges?" + f"asset_class={asset_class}&"

        if locale is not None:
            url = url + f"locale={locale}&"
        
        url = url + f"apiKey={self.polygon_api_key}"

        response = requests.get(url)
        data = response.json()

        status = data.get("status", None)
        if status not in ("OK"):
            raise ValueError(f"API Error: {data}")

        return data.get("results", None)
    
    def get_conditions(self, **kwargs: Any) -> Optional[dict]:
        """
        Get a list of conditions that Polygon.io uses.

        /v3/reference/conditions?asset_class={asset_class}&limit={limit}&apiKey={apiKey}
        """

        asset_class = kwargs.get("asset_class", "stocks")
        data_type = kwargs.get("data_type", None)
        id = kwargs.get("id", None)
        sip = kwargs.get("sip", None)
        order = kwargs.get("order", None)
        limit = kwargs.get("limit", 10)
        sort = kwargs.get("sort", None)

        url = POLYGON_BASE_URL + "v3/reference/conditions?" + f"asset_class={asset_class}&"

        if data_type is not None:
            url = url + f"data_type={data_type}&"
        
        if id is not None:
            url = url + f"id={id}&"
        
        if sip is not None:
            url = url + f"sip={sip}&"
        
        if order is not None:
            url = url + f"order={order}&"
        
        url = url + f"limit={limit}&"

        if sort is not None:
            url = url + f"sort={sort}&"
        
        url = url + f"apiKey={self.polygon_api_key}"

        response = requests.get(url)
        data = response.json()

        status = data.get("status", None)
        if status not in ("OK"):
            raise ValueError(f"API Error: {data}")
        
        return data.get("results", None)
    
    def get_stock_splits(self, **kwargs: Any) -> Optional[dict]:
        """
        Get a list of historical stock splits for a specific ticker.

        /v3/reference/splits?limit={limit}&apiKey={apiKey}
        """

        ticker = kwargs.get("ticker", None)
        execution_date = kwargs.get("execution_date", None)
        reverse_split = kwargs.get("reverse_split", None)
        order = kwargs.get("order", None)
        limit = kwargs.get("limit", 10)
        sort = kwargs.get("sort", None)

        url = POLYGON_BASE_URL + "v3/reference/splits?"

        if ticker is not None:
            url = url + f"ticker={ticker}&"
        
        if execution_date is not None:
            url = url + f"execution_date={execution_date}&"
        
        if reverse_split is not None:
            url = url + f"reverse_split={reverse_split}&"
        
        if order is not None:
            url = url + f"order={order}&"

        url = url + f"limit={limit}&"
        
        if sort is not None:
            url = url + f"sort={sort}&"
        
        url = url + f"apiKey={self.polygon_api_key}"

        response = requests.get(url)
        data = response.json()

        status = data.get("status", None)
        if status not in ("OK"):
            raise ValueError(f"API Error: {data}")

        return data.get("results", None)
    
    def get_stocks_financials(self, **kwargs: Any) -> Optional[dict]:
        """
        Get a list of historical financial data for a stock ticker.

        /vX/reference/financials?limit={limit}&apiKey={apiKey}
        """

        ticker = kwargs.get("ticker", None)
        cik = kwargs.get("cik", None)
        company_name = kwargs.get("company_name", None)
        sic = kwargs.get("sic", None)
        filing_date = kwargs.get("filing_date", None)
        period_of_report_date = kwargs.get("period_of_report_date", None)
        timeframe = kwargs.get("timeframe", None)
        include_sources = kwargs.get("include_sources", None)
        order = kwargs.get("order", None)
        limit = kwargs.get("limit", 10)
        sort = kwargs.get("sort", None)

        url = POLYGON_BASE_URL + "vX/reference/financials?"

        if ticker is not None:
            url = url + f"ticker={ticker}&"

        if cik is not None:
            url = url + f"cik={cik}&"
        
        if company_name is not None:
            url = url + f"company_name={company_name}&"
        
        if sic is not None:
            url = url + f"sic={sic}&"
        
        if filing_date is not None:
            url = url + f"filing_date={filing_date}&"

        if period_of_report_date is not None:
            url = url + f"period_of_report_date={period_of_report_date}&"

        if timeframe is not None:
            url = url + f"timeframe={timeframe}&"

        if include_sources is not None:
            url = url + f"include_sources={include_sources}&"

        if order is not None:
            url = url + f"order={order}&"

        url = url + f"limit={limit}&"

        if sort is not None:
            url = url + f"sort={sort}&"

        url = url + f"apiKey={self.polygon_api_key}"

        response = requests.get(url)
        data = response.json()

        status = data.get("status", None)
        if status not in ("OK"):
            raise ValueError(f"API Error: {data}")
        
        return data.get("results", None)

    def get_last_trade(self, ticker: str) -> Optional[dict]:
        """
        Get the last trade data for a given stock.

        /v2/last/trade/{ticker}?apiKey={apiKey}
        """
        url = (
            f"{POLYGON_BASE_URL}v2/last/trade"
            f"/{ticker}"
            f"?apiKey={self.polygon_api_key}"
        )
        response = requests.get(url)
        data = response.json()

        status = data.get("status", None)
        if status not in ("OK"):
            raise ValueError(f"API Error: {data}")

        return data.get("results", None)

    def run(self, mode: str, ticker: str, **kwargs: Any) -> str:
        if mode == "get_crypto_aggregate":
            return json.dumps(self.get_crypto_aggregates(ticker))
        elif mode == "get_ipos":
            return json.dumps(self.get_ipos(**kwargs))
        elif mode == "get_related_companies":
            return json.dumps(self.get_related_companies(ticker))
        elif mode == "get_exchanges":
            return json.dumps(self.get_exchanges(**kwargs))
        elif mode == "get_conditions":
            return json.dumps(self.get_conditions(**kwargs))
        elif mode == "get_stock_splits":
            return json.dumps(self.get_stock_splits(**kwargs))
        elif mode == "get_stocks_financials":
            return json.dumps(self.get_stocks_financials(**kwargs))
        elif mode == "get_last_trade":
            return json.dumps(self.get_last_trade(ticker))
        else:
            raise ValueError(f"Invalid mode {mode} for Polygon API.")
