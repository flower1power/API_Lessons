from clients.http.mailhog_api.apis.mailhog_api import MailhogApi
from packages.rest_client.configuration import Configuration


class ApiMailhog:

    def __init__(self, configuration: Configuration):
        self.configuration = configuration
        self.mailhog_api = MailhogApi(configuration=self.configuration)
