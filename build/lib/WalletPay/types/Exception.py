import typing


class WalletPayException(Exception):
    """Base exception for WalletPay API."""
    pass


class WalletUnsuccessRequestException(WalletPayException):
    def __init__(self, raw_data, *args, **kwargs):
        self.raw_data: typing.Dict[str, typing.Any] = raw_data
        super().__init__(*args, **kwargs)


class CreateOrderException(WalletUnsuccessRequestException):
    pass


class GetOrderPreviewException(WalletUnsuccessRequestException):
    pass


class GetOrderListException(WalletUnsuccessRequestException):
    pass


class GetOrderAmountException(WalletUnsuccessRequestException):
    pass
