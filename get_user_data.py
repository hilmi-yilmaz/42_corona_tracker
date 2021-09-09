import os
import json
import requests
import yaml
import time

class API42:
    """
    Connect to the API and send requests.
    """
    def __init__(self):
        """
        Reads the config file and saves the data as attributes.
        Requests token with the request_token function below.
        """
        with open("config.yaml", "r") as stream:
            config = yaml.load(stream, Loader=yaml.FullLoader)
            self.client_id = config["client_id"]
            self.client_secret = config["client_secret"]
            self.token_uri = config["token_uri"]
            self.endpoint = config["endpoint"]

        self.token = self.request_token()

    def request_token(self):
        """
        Requests the access token from the 42API. This token is needed to make use of the API.

        Arguments:
            None

        Returns:
            access_token
        """
        query = {"client_id": self.client_id, "client_secret": self.client_secret, "grant_type": "client_credentials"}
        response = requests.post(self.token_uri, query)
        if response.status_code != 200:
            print(f"Can't get token --> {response.status_code}: {response.reason}. Check your client ID and client secret.")
            exit(1)
        return (response.json()["access_token"])

    def get(self, name, params):
        """
        The get function returns the response (json) asked for by the name parameter.
        It loops over all pages.

        Arguments:
            name: part of the api you want to ask.
            params: the payload to send with the request.
        """
        endpoint = os.path.join(self.endpoint, name)
        params["access_token"] = self.token
        params["page[number]"] = 1
        data = []
        while True:
            response = requests.get(endpoint, params)
            if response.status_code != 200:
                print(f"{endpoint} --> {response.status_code}: {response.reason}")
                exit(1)
            if len(response.json()) == 0:
                break
            params["page[number]"] += 1
            data.extend(response.json())
            time.sleep(1)

        return (data)


if __name__ == "__main__":
    api = API42()
    payload = {"filter[campus_id]":14, "filter[active]": "true", "page[size]": 50}#, "filter[id]": 13024171}
    data = api.get("locations", payload)

    i = 0
    for element in data:
        print(element)
        print("")
        i += 1
    print(i)