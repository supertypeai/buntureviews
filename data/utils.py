from django.contrib.contenttypes.models import ContentType
from google_play_scraper import app
import requests, re, logging

logger = logging.getLogger(__name__)

def get_model_class(app_label, model_name):
    model = ContentType.objects.get(app_label=app_label, model=model_name)
    return model.model_class()

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

 

def create_review_data(app_id, country, store_type, app_instance):
    country, app_id, review_create_response = country.lower(), app_id[2:], False
    review_list = []
    logger.critical("started working")
    if store_type == "AppStore":
        url = f"https://itunes.apple.com/{country}/rss/customerreviews/id={app_id}/page=1/sortBy=mostRecent/json"
        res = requests.get(url)
        review_data = res.json()
        reviews = review_data["feed"]["entry"]
        first_link = review_data["feed"]["link"][2]["attributes"]["href"]
        last_link = review_data["feed"]["link"][3]["attributes"]["href"]

        for review in reviews:
            review_obj = {
                "author": review["author"]["name"]["label"],
                "version": review["im:version"]["label"],
                "rating": review["im:rating"]["label"],
                "title": review["title"]["label"],
                "content": review["content"]["label"],
                "country": country,
                "app": app_instance
            }
            AppStoreReview = get_model_class('data', 'appstorereview')
            review_list.append(AppStoreReview(**review_obj))
        AppStoreReview.objects.bulk_create(review_list)
        review_create_response = True
        
    
    return review_create_response
        

