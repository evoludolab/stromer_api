from urllib.parse import urlencode, parse_qs, splitquery

import requests
import logging

class Connection:
    __url = "https://stromer-portal.ch/mobile/v4/login/"
    __token_url = "https://stromer-portal.ch/mobile/v4/o/token/"
    __api_url = "https://api3.stromer-portal.ch/rapi/mobile/v4.1/"

    def __init__(self, username: str, password: str, client_id: str) -> None:
        self.__session = requests.session()
        self.__session.get(self.__url)
        self.__access_token = None

        try:
            qs = urlencode(
                {
                    "client_id": client_id,
                    "response_type": "code",
                    "redirect_url": "stromerauth://auth",
                    "scope": "bikeposition bikestatus bikeconfiguration bikelock biketheft "
                             "bikedata bikepin bikeblink userprofile"
                }
            )

            data = {
                "password": password,
                "username": username,
                "csrfmiddlewaretoken": self.__session.cookies.get("csrftoken"),
                "next": "/mobile/v4/o/authorize/?" + qs
            }

            res = self.__session.post(self.__url, data=data, headers={"Referer": self.__url}, allow_redirects=False)
            res = self.__session.send(res.next, allow_redirects=False)

            _, qs = splitquery(res.headers["Location"])
            query = parse_qs(qs)
            code = query["code"][0]
            params = {
                "grant_type": "authorization_code",
                "client_id": client_id,
                "code": code,
                "redirect_uri": "stromer://auth"
            }

            res = requests.post(self.__token_url, params=params)
            self.__access_token = res.json()["access_token"]

        except:
            raise Exception("Authentication failed")

    def get_endpoint(self, endpoint: str, params: dict = None, full_list: bool = False):
        try:
            if params is None:
                params = {}

            res = requests.get(self.__api_url + endpoint,
                               headers={"Authorization": "Bearer %s" % self.__access_token},
                               params=params)
            resj = res.json()
            if res.status_code != 200:
                logging.warning("Problem in request: %s" % resj["result"])
                return None

            data = resj["data"]
            if isinstance(data, list):
                if full_list:
                    return data
                else:
                    return data[0]
            else:
                return data

        except:
            raise Exception("Error in request parameters")

    def set_endpoint(self, endpoint: str, settings: dict = None, full_list: bool = False):
        try:
            if settings is None:
                return None

            resp = requests.post(self.__api_url + endpoint,
                               headers={"authorization": "Bearer %s" % self.__access_token},
                               json=settings)
            data = resp.json()["data"]
            if resp.status_code != 200:
                logging.warning("Problem in request: %s" % data["result"])
                return None
            return data

        except:
            raise Exception("Error in request parameters")
