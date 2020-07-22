import re
import requests
from google_play_scraper import app


def _guess_store(appid):
    """
    Return either 'AppStore' or 'PlayStore' based on the string pattern
    if string pattern conforms to a known pattern.
    """

    if re.fullmatch(r"^id(\d){8,}$", appid):
        return "AppStore"
    elif re.fullmatch(r"^(\w+\.){2,}\w+$", appid):
        return "PlayStore"
    else:
        raise Exception(
            "The app id you've provided cannot be found in that country's app store."
        )


def validate_appid(appid: str, country: str):
    store = _guess_store(appid)
    assert store in ["AppStore", "PlayStore"]
    if store == "AppStore":
        url = f"http://apps.apple.com/{country}/app/{appid}"
        res = requests.get(url)
        if res.status_code == 200:
            appname = re.search('(?<="name":").*?(?=")', res.text).group(0)
            publisher = re.search(
                '(?<="author":).*("name":")(.*?)(?=")', res.text
            ).group(2)
            category = re.search(
                '(?<="applicationCategory":").*?(?=")', res.text
            ).group(0)
            return appname, store, publisher, category
        else:
            raise Exception(
                "Did not receive a valid response. Response code", res.status_code
            )

    if store == "PlayStore":
        try:
            appinfo = app(appid, country=country)
            appname = appinfo["title"]
            publisher = appinfo["developer"]
            category = appinfo["genre"]
            return appname, store, publisher, category
        except err as err:
            raise Exception("Did not receive a valid response.", err)
