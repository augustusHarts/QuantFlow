class YahooProviderError(Exception):
    pass


class YahooFetchError(Exception):
    pass


class YahooRateLimitError(YahooProviderError):
    pass


class YahooInvalidResponseError(YahooProviderError):
    pass
