import requests
import json
import time
from api.oauth import ebay_get_oauth

def get_aspects(category):
    url = "https://api.ebay.com/commerce/taxonomy/v1/category_tree/0/get_item_aspects_for_category"

    querystring = {"category_id": category}

    payload = ""
    headers = {
        "Authorization": "Bearer " + ebay_get_oauth()
    }

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

    json_obj = json.loads(response.text)

    aspects = []
    for aspect in json_obj["aspects"]:
        if aspect["aspectConstraint"]["aspectRequired"]:
            aspects.append(aspect["localizedAspectName"])


def get_category(keywords):
    url = "https://api.ebay.com/commerce/taxonomy/v1/category_tree/0/get_category_suggestions"

    querystring = {"q": keywords}

    payload = ""
    headers = {
        "Authorization": "Bearer " + ebay_get_oauth()
    }

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

    json_obj = json.loads(response.text)

    suggestion = json_obj["categorySuggestions"][0]

    # Build the category tree path
    category_path = []
    for ancestor in suggestion["categoryTreeNodeAncestors"]:
        category_path.append(ancestor["categoryName"])
    category_path.append(suggestion["category"]["categoryName"])

    # Create the category tree path string
    category_tree_str = " -> ".join(category_path)

    # Get the category id of the leaf in a list
    leaf_category_id = [suggestion["category"]["categoryId"]]

    return category_tree_str, leaf_category_id