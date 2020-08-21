from django.contrib.contenttypes.models import ContentType
from google_play_scraper import app, reviews_all, Sort
import requests, re, logging
from datetime import datetime

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
            return None

    if store == "PlayStore":
        try:
            appinfo = app(appid, country=country)
            appname = appinfo["title"]
            publisher = appinfo["developer"]
            category = appinfo["genre"]
            return appname, store, publisher, category
        except:
            return None


def fetch_data_from_app_store(country, app_id, n):
    url = f"https://itunes.apple.com/{country}/rss/customerreviews/id={app_id}/page={n}/sortBy=mostRecent/json"
    res = requests.get(url)
    review_data = res.json()

    return review_data


def create_review_data(app_id, country, store_type, app_instance):
    country, review_create_response = country.lower(), False
    review_list = []
    if store_type == "AppStore":
        app_id = app_id[2:]
        review_data = fetch_data_from_app_store(country, app_id, 1)
        if "entry" not in review_data["feed"]:
            return 404, "Review not found"
        reviews = review_data["feed"]["entry"]
        first_link = review_data["feed"]["link"][2]["attributes"]["href"]
        last_link = review_data["feed"]["link"][3]["attributes"]["href"]

        start_number = int(first_link.split("/")[6].split("=")[1])
        last_number = int(last_link.split("/")[6].split("=")[1])

        AppStoreReview = get_model_class("data", "appstorereview")

        break_review = False

        for n in range(start_number, last_number + 1):
            for review in reviews:
                review_obj = {
                    "author": review["author"]["name"]["label"],
                    "version": review["im:version"]["label"],
                    "rating": review["im:rating"]["label"],
                    "title": review["title"]["label"],
                    "content": review["content"]["label"],
                    "country": country,
                    "app": app_instance,
                }
                review_list.append(AppStoreReview(**review_obj))

                if len(review_list) >= 500:
                    break_review = True
                    break

            if break_review is True:
                break

            if n < last_number:
                review_data = fetch_data_from_app_store(country, app_id, n + 1)
                reviews = (
                    review_data["feed"]["entry"]
                    if "entry" in review_data["feed"]
                    else []
                )

        AppStoreReview.objects.bulk_create(review_list)
        review_create_response = True
    elif store_type == "PlayStore":
        PlayStoreReview = get_model_class("data", "playstorereview")
        try:
            reviews = reviews_all(app_id, country=country, sort=Sort.MOST_RELEVANT)
        except expression as identifier:
            reviews = []

        if len(reviews) <= 0:
            return 400, "Review not found"
        review_list = []
        for review in reviews:
            review_obj = {
                "author": review["userName"],
                "version": review["reviewCreatedVersion"],
                "rating": review["score"],
                "title": "",
                "content": review["content"],
                "country": country,
                "app": app_instance,
                "authorImg": review["userImage"],
                "reviewedAt": review["at"],
                "replyContent": review["replyContent"],
                "repliedAt": review["repliedAt"],
                "reviewId": review["reviewId"],
                "thumbsUpCount": review["thumbsUpCount"],
            }
            review_list.append(PlayStoreReview(**review_obj))

        PlayStoreReview.objects.bulk_create(review_list)
        review_create_response = True

    return 201, review_create_response

