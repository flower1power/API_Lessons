from clients.http.dm_api_account.apis.account_api import AccountApi
from clients.http.dm_api_account.apis.login_api import LoginApi
from packages.rest_client.configuration import Configuration


class ApiDmAccount:

    def __init__(self, configuration: Configuration):
        self.configuration = configuration
        self.login_api = LoginApi(configuration=self.configuration)
        self.account_api = AccountApi(configuration=self.configuration)
